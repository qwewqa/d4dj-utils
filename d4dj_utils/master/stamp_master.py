import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class StampMaster(MasterAsset):
    id: int
    category_id: int
    name: str
    description: str
    has_voice: bool

    def __hash__(self):
        return self.id.__hash__()

    @property
    def is_released(self):
        return (self.id <= 10036 or
                (10036 < self.id < 20000 and
                 (self.id - 10000) in self.assets.event_master and
                 self.assets.event_master[self.id - 10000].is_released) or
                (20000 < self.id < 30000 and self.id <= 20026) or  # Hardcoding these two until a better way is found
                (30000 < self.id < 40000 and self.id <= 30001))

    @property
    def quote(self):
        if quote := re.search(r'[「"](.*)[」"]', self.description):
            return str(quote.group(1))
        return None

    @property
    def audio_path(self):
        return self.assets.path / 'plain' / 'voice' / f'Stamp_{self.id}.wav'

    @property
    def category(self):
        return StampCategory(self.category_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category,
            'has_voice': self.has_voice,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category,
            'description': self.description,
            'has_voice': self.has_voice,
        }


class StampCategory(Enum):
    Common = 0
    Rare = 1
    Collab = 2
