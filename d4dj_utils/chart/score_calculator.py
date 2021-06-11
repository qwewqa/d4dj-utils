import heapq
import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Union

from d4dj_utils.chart.chart import NoteData, NoteType, Chart
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


class Timer:
    def __init__(self, timeline: 'Timeline', callback: TimelineCallback):
        def cb(tl):
            callback(tl)
            self.reset()

        self.timeline = timeline
        self._duration = 0
        self._callback = cb
        self._ongoing_time_remaining = None
        self._trigger = None

    @property
    def running(self):
        return self._trigger is not None

    @property
    def duration(self):
        return self._duration

    def start(self):
        if self.running:
            return
        if self._duration <= 0:
            raise RuntimeError('Timer not set.')
        if self._ongoing_time_remaining is not None:
            self._trigger = self.timeline.schedule(self._ongoing_time_remaining, self._callback)
        else:
            self._trigger = self.timeline.schedule(self._duration, self._callback)

    def pause(self):
        if self.running:
            self._ongoing_time_remaining = self._trigger.time - self.timeline.time
            self._trigger.cancel()
            self._trigger = None

    def reset(self):
        if self.running:
            self._trigger.cancel()
            self._trigger = None
        self._ongoing_time_remaining = None

    def set(self, duration):
        if self.running:
            self.reset()
            self._duration = duration
            self.start()
        else:
            self._duration = duration
        return self


class Timeline:
    def __init__(self):
        self.time = 0
        self._queue = []

    def add(self, time: float, callback: TimelineCallback):
        trig = Trigger(time, callback)
        heapq.heappush(self._queue, trig)
        return trig

    def schedule(self, time: float, callback: TimelineCallback):
        return self.add(time + self.time, callback)

    def run(self):
        while self._queue:
            trigger = heapq.heappop(self._queue)
            if not trigger.cancelled:
                trigger.callback(self)


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

    autoplay_multiplier = 17 / 20
    disable_soflan_multiplier = 20 / 21
    combo_multipliers = ([1.0] * 20 + [1.01] * 30 + [1.02] * 50 + [1.03] * 50 + [1.04] * 50 + [1.05] * 50 +
                         [1.06] * 50 + [1.07] * 100 + [1.08] * 100 + [1.09] * 100 + [1.10] * 100 + [1.11])

    accuracy_applicable_note_types = {NoteType.Tap1, NoteType.Tap2}

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
                    timeline.score += (0.9 * (1 - accuracy) *
                                       math.floor(base_score * multiplier *
                                                  (1 + skill.score_up_rate / 100)))
                else:
                    timeline.score += accuracy * math.floor(base_score * multiplier)
                    timeline.score += 0.9 * (1 - accuracy) * math.floor(base_score * multiplier)
            if not autoplay:
                timeline.combo += 1

        timeline.add(note.time, note_cb)

    for note in chart.notes:
        add_note_callback(note)

    timeline.run()
    return timeline.score
