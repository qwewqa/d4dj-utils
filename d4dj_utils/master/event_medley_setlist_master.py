from dataclasses import dataclass, field
from dataclasses import dataclass
from typing import Dict, Any, Sequence, Tuple

import msgpack

from d4dj_utils.master.event_specific_bonus_master import ParameterBonus
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class EventMedleySetlistMaster(MasterAsset):
    id: int
    name: str
    music_ids: Sequence[int]
    required_point: int
    start_date: msgpack.Timestamp = msgpack.Timestamp(0)
    end_date: msgpack.Timestamp = msgpack.Timestamp(31536000)
    order: int = 0
    specific_bonus_character_ids: Tuple[int, ...] = ()
    character_match_parameter_bonus_id: int = 0
    character_match_parameter_bonus_value: int = 0

    def __hash__(self):
        return self.id.__hash__()

    @property
    def specific_bonus_characters(self):
        return [
            self.assets.character_master.get(cid)
            for cid in self.specific_bonus_character_ids
        ]

    @property
    def character_match_parameter_bonus(self):
        return ParameterBonus(self.character_match_parameter_bonus_id)

    @property
    def music(self):
        return [self.assets.music_master.get(mid) for mid in self.music_ids]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "music": self.music,
            "required_point": self.required_point,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "music": self.music,
            "start_date": self.start_datetime,
            "end_date": self.end_datetime,
            "order": self.order,
            "specific_bonus_characters": self.specific_bonus_characters,
            "character_match_parameter_bonus": self.character_match_parameter_bonus,
            "character_match_parameter_bonus_value": self.character_match_parameter_bonus_value,
        }
