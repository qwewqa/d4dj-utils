import contextlib
import json
import wave
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Dict, Any, Tuple, Optional

import msgpack

from d4dj_utils.master.chart_master import ChartDifficulty
from d4dj_utils.master.common_enums import ChartSectionType
from d4dj_utils.master.master_asset import MasterAsset

try:
    from d4dj_utils.extended.tools.tools import vgmstream
except (ImportError, ModuleNotFoundError):
    vgmstream = None


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
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    has_movie: bool
    purchase_bonus_ids: Tuple[int]
    is_hidden: bool
    exclude_challenge: bool

    def __hash__(self):
        return self.id.__hash__()

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

    @cached_property
    def duration(self) -> Optional[float]:
        try:
            with open(self.audio_path.with_name(self.audio_path.name + '.json'), 'r', encoding='utf-8') as f:
                audio_data = json.load(f)
                return audio_data['sampleCount'] / audio_data['sampleRate']
        except:
            return None

    def decode_audio(self):
        # This doesn't decrypt, but we only need durations from the resulting wav
        vgmstream(self.audio_path)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category.name,
            'unit': self.unit,
            'chart_levels': self.chart_levels,
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
            'chart_levels': self.chart_levels,
            'default_order': self.default_order,
            'bpm': self.bpm,
            'open_key': self.open_key,
            'section_trend': self.section_trend.name,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'has_movie': self.has_movie,
            # 'purchase_bonus'
            'is_hidden': self.is_hidden,
            'exclude_challenge': self.exclude_challenge,
            'mix_info': '(' + ', '.join(f'{k.name}: {v}' for k, v in self.mix_info.items()) + ')',
        }


class MusicCategory(Enum):
    Nothing = 0  # None
    Original = 1
    Cover = 2
    Game = 3
    Instrumental = 4
    Collab = 5
