import enum
from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class EventSpecificBonusMaster(MasterAsset):
    id: int
    character_ids: Tuple[int]
    attribute_id: int
    character_match_point_bonus_value: int
    attribute_match_point_bonus_value: int
    all_match_point_bonus_value: int
    character_match_parameter_bonus_id: int
    character_match_parameter_bonus_value: int
    attribute_match_parameter_bonus_id: int
    attribute_match_parameter_bonus_value: int
    all_match_parameter_bonus_id: int
    all_match_parameter_bonus_value: int

    @property
    def characters(self):
        return [self.assets.character_master[cid] for cid in self.character_ids]

    @property
    def attribute(self):
        return self.assets.attribute_master.get(self.attribute_id)

    @property
    def character_match_parameter_bonus(self) -> 'ParameterBonus':
        return ParameterBonus(self.character_match_parameter_bonus_id)

    @property
    def attribute_match_parameter_bonus(self) -> 'ParameterBonus':
        return ParameterBonus(self.attribute_match_parameter_bonus_id)

    @property
    def all_match_parameter_bonus(self) -> 'ParameterBonus':
        return ParameterBonus(self.all_match_parameter_bonus_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'characters': '[' + ' ,'.join(str(c) for c in self.characters) + ']',
            'attribute': self.attribute,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'characters': '[' + ' ,'.join(str(c) for c in self.characters) + ']',
            'attribute': self.attribute,
            'character_match_point_bonus_value': self.character_match_point_bonus_value,
            'attribute_match_point_bonus_value': self.attribute_match_point_bonus_value,
            'all_match_point_bonus_value': self.all_match_point_bonus_value,
            'character_match_parameter_bonus': self.character_match_parameter_bonus.name,
            'character_match_parameter_bonus_value': self.character_match_parameter_bonus_value,
            'attribute_match_parameter_bonus': self.attribute_match_parameter_bonus.name,
            'attribute_match_parameter_bonus_value': self.attribute_match_parameter_bonus_value,
            'all_match_parameter_bonus': self.all_match_parameter_bonus.name,
            'all_match_parameter_bonus_value': self.all_match_parameter_bonus_value,
        }


class ParameterBonus(enum.Enum):
    All = 0
    Heart = 1
    Technique = 2
    Physical = 3
