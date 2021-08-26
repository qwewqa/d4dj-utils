from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class GachaRouletteMaster(MasterAsset):
    id: int
    type_id: int
    target_id: int
    effect_value: int
    draw_limit: int

    db_fields = ['id', 'gacha_id']

    def __hash__(self):
        return self.id.__hash__()

    @property
    def type(self):
        return GachaRouletteType(self.type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'target_id': self.target_id,
            'effect_value': self.effect_value,
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'type': self.type,
            'target_id': self.target_id,
            'effect_value': self.effect_value,
            'draw_limit': self.draw_limit,
        }


class GachaRouletteType(Enum):
    PickUpUp = 1
    RarityUp = 2
    StockPresent = 3
