import heapq
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, List, Optional, Union, Sequence, NamedTuple, Dict, Tuple

from d4dj_utils.chart.chart import NoteData, Chart
from d4dj_utils.master.chart_master import ChartMaster
from d4dj_utils.master.skill_master import SkillMaster

TimelineCallback = Callable[['Timeline'], None]


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


class ChartScoringData:
    def __init__(self, data: 'Dict[ScoringDataType, Dict[ScoringDataEntry, int]]'):
        self.data = data

    def score(self,
              power: int,
              skills: List[SkillMaster],
              enable_fever: bool = True,
              accuracy: float = 1.0,
              disable_soflan: bool = False,
              autoplay: bool = False,
              enable_combo_bonus: bool = True) -> float:
        if autoplay:
            enable_combo_bonus = False
        data = self.data[ScoringDataType(fever=enable_fever, combo=enable_combo_bonus)]
        multiplier = power
        if disable_soflan:
            multiplier *= disable_soflan_multiplier
        if autoplay:
            multiplier *= autoplay_multiplier
        total_score = 0
        for entry, count in data.items():
            score = entry.score * multiplier
            if entry.skills:
                active_skills = [skills[i] for i in entry.skills]
                score_up_rate = sum(s.score_up_rate for s in active_skills)
                perfect_score_up_rate = sum(s.perfect_score_up_rate for s in active_skills)
                if autoplay:
                    score = math.floor(score * (1 + score_up_rate / 100))
                else:
                    score = (accuracy * math.floor(score * (1 + score_up_rate / 100 +
                                                            perfect_score_up_rate / 100)) +
                             (1 - accuracy) * math.floor(0.9 * score * (1 + score_up_rate / 100)))
            else:
                score = accuracy * math.floor(score) + (1 - accuracy) * math.floor(0.9 * score)
            total_score += score * count
        return total_score


autoplay_multiplier = 17 / 20
disable_soflan_multiplier = 20 / 21
combo_multipliers = ([1.0] * 20 + [1.01] * 30 + [1.02] * 50 + [1.03] * 50 + [1.04] * 50 + [1.05] * 50 +
                     [1.06] * 50 + [1.07] * 100 + [1.08] * 100 + [1.09] * 100 + [1.10] * 100 + [1.11])


class ScoringDataEntry(NamedTuple):
    score: float
    skills: Tuple[int, ...]


class ScoringDataType(NamedTuple):
    fever: bool
    combo: bool


def get_chart_scoring_data(chart: Chart,
                           skill_durations: Sequence[float],
                           fever_multiplier: float = 1.0) -> ChartScoringData:
    tl = Timeline()
    tl.active_skills = set()
    tl.combo = 0
    tl.fever_active = False

    base_score = (1 + 0.01 * (chart.info.level - 5)) * 3 / len(chart.notes)

    data = {
        ScoringDataType(True, True): defaultdict(lambda: 0),
        ScoringDataType(True, False): defaultdict(lambda: 0),
        ScoringDataType(False, True): defaultdict(lambda: 0),
        ScoringDataType(False, False): defaultdict(lambda: 0),
    }

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

    tl.fever_multiplier = fever_multiplier
    if n_fever_notes := sum(1 for n in chart.notes if chart.info.fever_start <= n.time < chart.info.fever_end):
        fever_note_fraction = n_fever_notes / len(chart.notes)
        fever_multiplier = (0.28 / fever_note_fraction) ** 0.6
        fever_multiplier = max(1.1, min(2 * fever_multiplier, 5.0))
        tl.fever_multiplier *= fever_multiplier

    def add_note_callback(note: NoteData):
        def note_cb(_tl):
            fever_multiplier = tl.fever_multiplier if tl.fever_active else 1.0
            combo_multiplier = combo_multipliers[min(tl.combo, 700)]
            data[ScoringDataType(fever=True, combo=True)][
                ScoringDataEntry(score=base_score * fever_multiplier * combo_multiplier,
                                 skills=tuple(tl.active_skills))] += 1
            data[ScoringDataType(fever=True, combo=False)][
                ScoringDataEntry(score=base_score * fever_multiplier,
                                 skills=tuple(tl.active_skills))] += 1
            data[ScoringDataType(fever=False, combo=True)][
                ScoringDataEntry(score=base_score * combo_multiplier,
                                 skills=tuple(tl.active_skills))] += 1
            data[ScoringDataType(fever=False, combo=False)][
                ScoringDataEntry(score=base_score,
                                 skills=tuple(tl.active_skills))] += 1
            tl.combo += 1

        tl.add(note.time, note_cb)

    for note in chart.notes:
        add_note_callback(note)

    tl.run()
    return ChartScoringData(data)


def calculate_score(chart: Union[Chart, ChartMaster],
                    power: int,
                    skills: List[SkillMaster],
                    enable_fever: bool = True,
                    accuracy: float = 1.0,
                    disable_soflan: bool = False,
                    autoplay: bool = False,
                    enable_combo_bonus: bool = True) -> Optional[float]:
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

        if n_fever_notes := sum(1 for n in chart.notes if chart.info.fever_start <= n.time < chart.info.fever_end):
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
                    timeline.score += math.floor(multiplier * (1 + skill.score_up_rate / 100) * base_score)
                else:
                    timeline.score += math.floor(multiplier * base_score)
            else:
                if timeline.active_skill_index != -1:
                    skill = skills[timeline.active_skill_index]
                    timeline.score += (accuracy *
                                       math.floor(base_score * multiplier *
                                                  (1 + skill.perfect_score_up_rate / 100 +
                                                   skill.score_up_rate / 100)))
                    timeline.score += ((1 - accuracy) *
                                       math.floor(0.9 * base_score * multiplier *
                                                  (1 + skill.score_up_rate / 100)))
                else:
                    timeline.score += accuracy * math.floor(base_score * multiplier)
                    timeline.score += (1 - accuracy) * math.floor(0.9 * base_score * multiplier)
            if not autoplay:
                timeline.combo += 1

        timeline.add(note.time, note_cb)

    for note in chart.notes:
        add_note_callback(note)

    timeline.run()
    return timeline.score
