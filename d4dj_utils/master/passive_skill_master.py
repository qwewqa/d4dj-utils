from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple, Optional

from d4dj_utils.master.character_master import CharacterMaster
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class PassiveSkillMaster(MasterAsset):
    id: int
    type_id: int
    min_value: float
    max_value: float
    sub_value: float
    bonus_character_id: int = -1

    def __hash__(self):
        return self.id.__hash__()

    @property
    def type(self):
        return PassiveSkillType(self.type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "sub_value": self.sub_value,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "sub_value": self.sub_value,
        }

    @property
    def bonus_character(self) -> Optional[CharacterMaster]:
        return self.assets.character_master.get(self.bonus_character_id)

    @classmethod
    def default(cls, assets):
        return {0: cls(assets, 0, 0, 0.0, 0.0, 0.0, 0)}


class PassiveSkillType(Enum):
    Nothing = 0
    FeverBonus = 1
    FeverSupport = 2
    ScoreUpWithDamage = 3
    AutoScoreUp = 4
    ManualScoreUp = 5
    SupportableScoreUp = 11
    SupportableSkillLonger = 12
    Sympathy = 13
