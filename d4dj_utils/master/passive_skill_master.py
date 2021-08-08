from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class PassiveSkillMaster(MasterAsset):
    id: int
    type_id: int
    min_value: float
    max_value: float
    sub_value: float

    def __hash__(self):
        return self.id.__hash__()

    @property
    def type(self):
        return PassiveSkillType(self.type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'sub_value': self.sub_value,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'sub_value': self.sub_value,
        }

    @classmethod
    def default(cls, assets):
        return {0: cls(assets, 0, 0, 0.0, 0.0, 0.0)}


class PassiveSkillType(Enum):
    Nothing = 0
    FeverBonus = 1
    FeverSupport = 2
    ScoreUpWithDamage = 3
    AutoScoreUp = 4
