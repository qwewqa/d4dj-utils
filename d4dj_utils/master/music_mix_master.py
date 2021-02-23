from dataclasses import dataclass
from typing import Dict, Any

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
