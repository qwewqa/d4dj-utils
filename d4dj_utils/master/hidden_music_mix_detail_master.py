from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset
from d4dj_utils.master.music_mix_master import MusicMixMaster


@dataclass
class HiddenMusicMixDetailMaster(MasterAsset):
    mix: int
    order: int
    start_time: float
    start_time_bpm: float
    end_time: float
    end_time_bpm: float
    enable_long_mix_start: bool
    enable_long_mix_end: bool

    @property
    def id(self):
        return self.mix, self.order

    def __hash__(self):
        return self.id.__hash__()

    def apply_to(self, music_mix_master: MusicMixMaster):
        return MusicMixMaster(
            self.assets,
            music_id=music_mix_master.music_id,
            section_id=music_mix_master.section_id,
            start_time=self.start_time,
            start_time_bpm=self.start_time_bpm,
            end_time=self.end_time,
            end_time_bpm=self.end_time_bpm,
            enable_long_mix_start=self.enable_long_mix_start,
            enable_long_mix_end=self.enable_long_mix_end,
        )
