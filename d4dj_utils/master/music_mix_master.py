from dataclasses import dataclass
from typing import Dict, Any, ClassVar

from d4dj_utils.master.common_enums import ChartSectionType
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class MusicMixMaster(MasterAsset):
    music_id: int
    section_id: int
    start_time: float
    start_time_bpm: float
    end_time: float
    end_time_bpm: float
    enable_long_mix_start: bool
    enable_long_mix_end: bool

    fade_in_beats: ClassVar[int] = 4
    fade_start_gap_seconds: ClassVar[float] = 2.0

    def __hash__(self):
        return self.id.__hash__()

    @property
    def id(self):
        return self.music_id, self.section_id

    @classmethod
    def create_for_full_song(cls, asset_manager, music, length):
        cls(asset_manager=asset_manager,
            music_id=music.id,
            section_id=0,
            start_time=0,
            start_time_bpm=music.bpm,
            end_time=length,
            end_time_bpm=music.bpm,
            enable_long_mix_start=False,
            enable_long_mix_end=False)

    @property
    def section(self):
        return ChartSectionType(self.section_id)

    @property
    def music(self):
        return self.assets.music_master[self.music_id]

    @property
    def name_description(self) -> str:
        return f'({self.music_id}, {self.section.name})'

    @property
    def duration(self):
        return self.end_time - self.start_time

    def get_fade_duration(self):
        return min(self.start_time, self.fade_start_gap_seconds + 60 * self.fade_in_beats / self.start_time_bpm)

    def contains_time(self, time: float):
        return self.start_time - 60 / self.start_time_bpm / 8 <= time <= self.end_time - 60 / self.end_time_bpm / 8

    def trim_chart(self, chart, shift_time: bool = True):
        return chart.trim(self.start_time - 60 / self.start_time_bpm / 8, self.end_time - 60 / self.end_time_bpm / 8, shift_time)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'duration': self.duration
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'music': self.music,
            'section': self.section.name,
            'start_time': self.start_time,
            'start_time_bpm': self.start_time_bpm,
            'end_time': self.end_time,
            'end_time_bpm': self.end_time_bpm,
            'duration': self.duration,
            'enable_long_mix_start': self.enable_long_mix_start,
            'enable_long_mix_end': self.enable_long_mix_end,
        }
