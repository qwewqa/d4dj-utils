import enum
from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.common_enums import ParameterBonus
from d4dj_utils.master.master_asset import MasterAsset
from d4dj_utils.master.parameter_bonus_master import ParameterBonusMaster


@dataclass
class EventSpecificBonusMaster(MasterAsset):
    id: int = -1
    character_ids: Tuple[int] = ()
    attribute_id: int = 0
    character_match_point_bonus_value: int = 0
    attribute_match_point_bonus_value: int = 0
    all_match_point_bonus_value: int = 0
    character_match_parameter_bonus_id: int = 0
    attribute_match_parameter_bonus_id: int = 0
    all_match_parameter_bonus_id: int = 0
    event_point_parameter_bonus_id: int = 0
    event_point_parameter_bonus_rate: int = 0
    event_point_parameter_bonus_value: int = 0
    event_point_parameter_base_value: int = 0

    def __hash__(self):
        return self.id.__hash__()

    @property
    def characters(self):
        return [self.assets.character_master[cid] for cid in self.character_ids]

    @property
    def attribute(self):
        return self.assets.attribute_master.get(self.attribute_id)

    @property
    def character_match_parameter_bonus(self) -> ParameterBonusMaster:
        return self.assets.parameter_bonus_master.get(self.character_match_parameter_bonus_id)

    @property
    def attribute_match_parameter_bonus(self) -> ParameterBonusMaster:
        return self.assets.parameter_bonus_master.get(self.attribute_match_parameter_bonus_id)

    @property
    def all_match_parameter_bonus(self) -> ParameterBonusMaster:
        return self.assets.parameter_bonus_master.get(self.all_match_parameter_bonus_id)

    @property
    def event_point_parameter_bonus(self) -> ParameterBonusMaster:
        return self.assets.parameter_bonus_master.get(self.event_point_parameter_bonus_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "characters": "[" + " ,".join(str(c) for c in self.characters) + "]",
            "attribute": self.attribute,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return self.one_line_description_items
