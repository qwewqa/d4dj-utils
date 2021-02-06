from dataclasses import dataclass
from typing import Dict, Any, Tuple

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class CardMaster(MasterAsset):
    id: int
    rarity_id: int
    name: str
    attribute_id: int
    character_id: int
    skill_id: int
    skill_name: str
    max_parameters: Tuple[int]
    gacha_message: str
    cloth_card_id: int
    debut_order: int
    head_y: Tuple[int]
    head_x: Tuple[int]
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp

    @property
    def attribute(self):
        return self.assets.attribute_master[self.attribute_id]

    @property
    def character(self):
        return self.assets.character_master[self.character_id]

    @property
    def rarity(self):
        return self.assets.rarity_master[self.rarity_id]

    @property
    def max_power(self):
        return sum(self.max_parameters)

    @property
    def max_parameters_with_limit_break(self):
        return [self.rarity.total_limit_break_bonus + param for param in self.max_parameters]

    @property
    def max_power_with_limit_break(self):
        return sum(self.max_parameters_with_limit_break)

    @property
    def skill(self):
        return self.assets.skill_master[self.skill_id]

    def art_path(self, limit_break):
        return self.assets.path / f'ondemand/card_chara/card_chara_{str(self.id).zfill(9)}_{1 if limit_break else 0}.jpg'

    def icon_path(self, limit_break):
        return self.assets.path / f'ondemand/card_icon/card_icon_{str(self.id).zfill(9)}_{1 if limit_break else 0}.jpg'

    @property
    def name_description(self) -> str:
        return f'{self.name} {self.character.first_name_english} ({self.id})'

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'rarity': self.rarity,
            'attribute': self.attribute,
            'max_power_with_limit_break': self.max_power_with_limit_break,
            'skill': self.skill,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'character': self.character,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'rarity': self.rarity,
            'attribute': self.attribute,
            'max_parameters': self.max_parameters,
            'max_parameters_with_limit_break': self.max_parameters_with_limit_break,
            'max_power_with_limit_break': self.max_power_with_limit_break,
            'skill_name': self.skill_name,
            'skill': self.skill,
            'gacha_message': self.gacha_message,
            'cloth_card_id': self.cloth_card_id,
            'debut_order': self.debut_order,
            'head_x': self.head_x,
            'head_y': self.head_y
        }
