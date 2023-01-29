import heapq
import math
import struct
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, List, Optional, Union, Sequence, NamedTuple, Dict, Tuple

from d4dj_utils.chart.chart import NoteData, Chart
from d4dj_utils.master.chart_master import ChartMaster
from d4dj_utils.master.skill_master import SkillMaster

TimelineCallback = Callable[["Timeline"], None]


@dataclass
class Trigger:
    time: float
    callback: TimelineCallback
    cancelled: bool = False

    def cancel(self):
        self.cancelled = True

    def __lt__(self, other):
        return self.time < other.time


class Timeline:
    def __init__(self):
        self.time = 0
        self.active = False
        self.is_heap = False
        self._queue = []

    def add(self, time: float, callback: TimelineCallback):
        trig = Trigger(time, callback)
        if self.active:
            if not self.is_heap:
                self.is_heap = True
                heapq.heapify(self._queue)
            heapq.heappush(self._queue, trig)
        else:
            self._queue.append(trig)
        return trig

    def schedule(self, time: float, callback: TimelineCallback):
        return self.add(time + self.time, callback)

    def run(self):
        if self.active:
            return
        self.active = True
        if self.is_heap:
            heapq.heapify(self._queue)
        else:
            self._queue = sorted(self._queue)[::-1]
        while self._queue:
            if self.is_heap:
                trigger = heapq.heappop(self._queue)
            else:
                trigger = self._queue.pop()
            if not trigger.cancelled:
                trigger.callback(self)
        self.active = False


def f32(n: float) -> float:
    return struct.unpack("f", struct.pack("f", n))[0]


class ChartScoringData:
    def __init__(
        self,
        base_score: Callable[[int], float],
        fever_multiplier: float,
        data: "Dict[ScoringDataEntry, int]",
    ):
        self.base_score = base_score
        self.fever_multiplier = fever_multiplier
        self.data = data

    def score(
        self,
        power: int,
        skills: List[SkillMaster],
        fever_score_up: float = 0.0,
        passive_score_up: float = 0.0,
        auto_score_up: float = 0.0,
        enable_fever: bool = True,
        disable_soflan: bool = False,
        autoplay: bool = False,
        accuracy: float = 1.0,
        combo_bonus_multiplier: Union[float, bool] = 1.0,
    ) -> float:
        if autoplay:
            combo_bonus_multiplier = 0.0
        else:
            combo_bonus_multiplier = f32(combo_bonus_multiplier)
        base_score = self.base_score(power)
        fever_multiplier = (
            f32(self.fever_multiplier * f32(1.0 + fever_score_up))
            if enable_fever
            else 1.0
        )
        data = self.data
        total_score = 0
        for (fever_active, combo_multiplier, active_skills), count in data.items():
            active_skills = [skills[i] for i in active_skills]
            score_up_rate = sum(s.score_up_rate for s in active_skills)
            if autoplay:
                perfect_score_up_rate = 0
            else:
                perfect_score_up_rate = sum(
                    s.perfect_score_up_rate for s in active_skills
                )
            if accuracy == 1.0:
                multiplier = f32(
                    f32((score_up_rate + perfect_score_up_rate) * 0.01) + 1.0
                )
            else:
                # At this point, exact accuracy is not important, so f32 doesn't matter.
                perfect_multiplier = (
                    score_up_rate + perfect_score_up_rate
                ) * 0.01 + 1.0
                great_multiplier = (score_up_rate * 0.01 + 1.0) * 0.9
                multiplier = (
                    accuracy * perfect_multiplier + (1 - accuracy) * great_multiplier
                )
            if fever_active:
                multiplier = f32(multiplier * fever_multiplier)
            if disable_soflan:
                multiplier = f32(multiplier * disable_soflan_multiplier)
            multiplier = f32(multiplier * f32(1.0 + passive_score_up))
            if autoplay:
                multiplier = f32(
                    f32(multiplier * f32(1.0 + auto_score_up)) * autoplay_multiplier
                )
            combo_multiplier = f32(
                f32(f32(combo_multiplier - 1.0) * combo_bonus_multiplier) + 1.0
            )
            score = math.floor(f32(f32(combo_multiplier * base_score) * multiplier))
            total_score += score * count
        return total_score


autoplay_multiplier = f32(17 / 20)
disable_soflan_multiplier = f32(20 / 21)
combo_multipliers = (
    [1.0] * 20
    + [1.01] * 30
    + [1.02] * 50
    + [1.03] * 50
    + [1.04] * 50
    + [1.05] * 50
    + [1.06] * 50
    + [1.07] * 100
    + [1.08] * 100
    + [1.09] * 100
    + [1.10] * 100
    + [1.11]
)


class ScoringDataEntry(NamedTuple):
    fever_active: bool
    combo_multiplier: float
    skills: Tuple[int, ...]


def get_chart_scoring_data(
    chart: Chart, skill_durations: Sequence[float]
) -> ChartScoringData:
    tl = Timeline()
    tl.active_skills = set()
    tl.combo = 0
    tl.fever_active = False

    def base_score(power: int):
        return f32(
            f32(1 + f32(0.01 * f32(f32(chart.info.level) - 5)))
            * f32(power * 3)
            / len(chart.notes)
        )

    data = defaultdict(int)

    def add_skill_callback(index: int, time: float):
        def start_cb(_tl):
            tl.active_skills.add(index)

        def end_cb(_tl):
            tl.active_skills.remove(index)

        tl.add(time, start_cb)
        tl.add(time + skill_durations[index], end_cb)

    skill_bars = chart.info.skill_times
    for index, skill_bar in enumerate(skill_bars):
        add_skill_callback(index, skill_bar)

    def enable_fever_cb(_tl):
        tl.fever_active = True

    def disable_fever_cb(_tl):
        tl.fever_active = False

    tl.add(chart.info.fever_start, enable_fever_cb)
    tl.add(chart.info.fever_end, disable_fever_cb)

    fever_multiplier = 1.0
    if n_fever_notes := sum(
        1
        for n in chart.notes
        if chart.info.fever_start <= n.time < chart.info.fever_end
    ):
        fever_note_fraction = f32(n_fever_notes / len(chart.notes))
        fever_multiplier = f32(f32(0.28 / fever_note_fraction) ** 0.6)
        fever_multiplier = f32(max(1.1, min(2 * fever_multiplier, 5.0)))

    def add_note_callback(note: NoteData):
        def note_cb(_tl):
            combo_multiplier = combo_multipliers[min(tl.combo, 700)]
            entry = ScoringDataEntry(
                fever_active=tl.fever_active,
                combo_multiplier=combo_multiplier,
                skills=tuple(sorted(tl.active_skills)),
            )
            data[entry] += 1
            tl.combo += 1

        tl.add(note.time, note_cb)

    for note in chart.notes:
        add_note_callback(note)

    tl.run()
    return ChartScoringData(base_score, fever_multiplier, data)


def calculate_score(
    chart: Union[Chart, ChartMaster],
    power: int,
    skills: List[SkillMaster],
    enable_fever: bool = True,
    accuracy: float = 1.0,
    disable_soflan: bool = False,
    autoplay: bool = False,
    enable_combo_bonus: bool = True,
) -> Optional[float]:
    if isinstance(chart, ChartMaster):
        chart = chart.load_chart_data()

    if not chart.info:
        return None

    if autoplay:
        enable_combo_bonus = False

    timeline = Timeline()
    timeline.active_skill_index = -1
    timeline.score = 0
    timeline.combo = 0
    timeline.fever_active = False
    timeline.fever_multiplier = 1.0

    base_score = (1 + 0.01 * (chart.info.level - 5)) * power * 3 / len(chart.notes)

    def add_skill_callback(index: int, time: float):
        def start_cb(_tl):
            timeline.active_skill_index = index

        def end_cb(_tl):
            if timeline.active_skill_index == index:
                timeline.active_skill_index = -1

        timeline.add(time, start_cb)
        timeline.add(time + skills[index].max_seconds, end_cb)

    skill_bars = chart.info.skill_times
    for index, skill_bar in enumerate(skill_bars):
        add_skill_callback(index, skill_bar)

    if enable_fever:

        def enable_fever_cb(_tl):
            timeline.fever_active = True

        def disable_fever_cb(_tl):
            timeline.fever_active = False

        timeline.add(chart.info.fever_start, enable_fever_cb)
        timeline.add(chart.info.fever_end, disable_fever_cb)

        if n_fever_notes := sum(
            1
            for n in chart.notes
            if chart.info.fever_start <= n.time < chart.info.fever_end
        ):
            fever_note_fraction = n_fever_notes / len(chart.notes)
            fever_multiplier = (0.28 / fever_note_fraction) ** 0.6
            fever_multiplier = max(1.1, min(2 * fever_multiplier, 5.0))
            timeline.fever_multiplier = fever_multiplier

    base_multiplier = 1
    if disable_soflan:
        base_multiplier *= disable_soflan_multiplier
    if autoplay:
        base_multiplier *= autoplay_multiplier

    def add_note_callback(note: NoteData):
        def note_cb(_tl):
            multiplier = base_multiplier

            if enable_combo_bonus:
                multiplier *= combo_multipliers[min(timeline.combo, 700)]

            if timeline.fever_active:
                multiplier *= timeline.fever_multiplier

            if autoplay:
                if timeline.active_skill_index != -1:
                    skill = skills[timeline.active_skill_index]
                    timeline.score += math.floor(
                        multiplier * (1 + skill.score_up_rate / 100) * base_score
                    )
                else:
                    timeline.score += math.floor(multiplier * base_score)
            else:
                if timeline.active_skill_index != -1:
                    skill = skills[timeline.active_skill_index]
                    timeline.score += accuracy * math.floor(
                        base_score
                        * multiplier
                        * (
                            1
                            + skill.perfect_score_up_rate / 100
                            + skill.score_up_rate / 100
                        )
                    )
                    timeline.score += (1 - accuracy) * math.floor(
                        0.9 * base_score * multiplier * (1 + skill.score_up_rate / 100)
                    )
                else:
                    timeline.score += accuracy * math.floor(base_score * multiplier)
                    timeline.score += (1 - accuracy) * math.floor(
                        0.9 * base_score * multiplier
                    )
            if not autoplay:
                timeline.combo += 1

        timeline.add(note.time, note_cb)

    for note in chart.notes:
        add_note_callback(note)

    timeline.run()
    return timeline.score
