from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple

import msgpack

from d4dj_utils.master.chart_master import ChartDifficulty
from d4dj_utils.master.common_enums import ChartSectionType
from d4dj_utils.master.master_asset import MasterAsset
from d4dj_utils.extended.tools.tools import vgmstream


@dataclass
class MusicMaster(MasterAsset):
    id: int
    name: str
    read_name: str
    lyricist: str
    composer: str
    arranger: str
    special_unit_name: str
    category_id: int
    unit_id: int
    default_order: int
    bpm: int
    open_key: int
    section_trend_id: int
    enable_long_mix: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    has_movie: bool
    purchase_bonus_ids: Tuple[int]
    trigger_music_ids: Tuple[int]
    exclude_challenge: bool
    is_tutorial: bool

    @property
    def category(self) -> 'MusicCategory':
        return MusicCategory(self.category_id)

    @property
    def section_trend(self) -> ChartSectionType:
        return ChartSectionType(self.section_trend_id)

    @property
    def unit(self):
        return self.assets.unit_master[self.unit_id]

    @property
    def trigger_music(self):
        return [self.assets.music_master[mid] for mid in self.trigger_music_ids]

    @property
    def charts(self):
        charts = self.assets.chart_master
        return {ChartDifficulty(d): charts[self.id * 10 + d] for d in range(1, 5) if (self.id * 10 + d) in charts}

    @property
    def chart_levels(self):
        return [chart.level for chart in self.charts.values()]

    @property
    def jacket_path(self):
        return self.assets.path / f'music_jacket/music_jacket_{str(self.id).zfill(7)}.jpg'

    @property
    def audio_path(self):
        return self.assets.path / f'plain/music/music_{str(self.id).zfill(7)}.acb'

    def decode_audio(self):
        # This doesn't decrypt, but we only need durations from the resulting wav
        vgmstream(self.audio_path)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category.name,
            'unit': self.unit,
        }

    @property
    def mix_info(self):
        return {ChartSectionType(section): self.assets.music_mix_master[(self.id, section)] for section in range(1, 4)
                if (self.id, section) in self.assets.music_mix_master}

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'read_name': self.read_name,
            'lyricist': self.lyricist,
            'composer': self.composer,
            'arranger': self.arranger,
            'special_unit_name': self.special_unit_name,
            'category': self.category.name,
            'unit': self.unit,
            'chart_levels': '[' + ', '.join(str(c) for c in self.chart_levels) + ']',
            'default_order': self.default_order,
            'bpm': self.bpm,
            'open_key': self.open_key,
            'section_trend': self.section_trend.name,
            'enable_long_mix': self.enable_long_mix,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'has_movie': self.has_movie,
            # purchase bonus
            'trigger_music': '[' + ', '.join(str(m) for m in self.trigger_music) + ']',
            'exclude_challenge': self.exclude_challenge,
            'is_tutorial': self.is_tutorial,
            'mix_info': '(' + ', '.join(f'{k.name}: {v}' for k, v in self.mix_info.items()) + ')',
        }


class MusicCategory(Enum):
    Nothing = 0  # None
    Original = 1
    Cover = 2
    Game = 3
    Instrumental = 4
    Collab = 5
