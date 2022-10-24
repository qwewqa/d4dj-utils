import datetime
import enum
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, Any, Tuple, Optional

import msgpack
import pytz

from d4dj_utils.master.common_enums import GachaType, GachaCategory
from d4dj_utils.master.event_master import EventMaster
from d4dj_utils.master.gacha_master import GachaMaster
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
    passive_skill_id: int
    max_parameters: Tuple[int]
    gacha_message: str
    cloth_card_id: int
    debut_order: int
    head_y: Tuple[int]
    head_x: Tuple[int]
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    gacha_card_attribute: int = 0
    can_use_common_card_stack_stock: bool = False

    @classmethod
    def new(cls, *args, **kwargs):
        if isinstance(args[8], tuple):
            args = [*args]
            args.insert(8, args[-2])
            del args[-2]
        return cls(*args, **kwargs)

    def __hash__(self):
        return self.id.__hash__()

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
    def passive_skill(self):
        return self.assets.passive_skill_master[self.passive_skill_id]

    initial_card_cutoff = pytz.timezone('Asia/Tokyo').localize(datetime.datetime(year=2020, month=10, day=1))

    @cached_property
    def gacha(self) -> Optional[GachaMaster]:
        return next((gacha for gacha in self.assets.gacha_master.values()
                     if self in gacha.pick_up_cards and
                     '★4' not in gacha.name), None)

    @cached_property
    def event(self) -> Optional[EventMaster]:
        return None
        return next((event for event in self.assets.event_master.values()
                     if abs((event.start_datetime - self.start_datetime).total_seconds()) <= 86400 and
                     (event.bonus.attribute == self.attribute or not event.bonus.attribute) and
                     (self.character in event.bonus.characters or not event.bonus.characters)), None)

    @cached_property
    def availability(self):
        if self.start_datetime < self.initial_card_cutoff:
            return CardAvailability.Permanent
        if gacha := self.gacha:
            if gacha.category == GachaCategory.Birthday:
                return CardAvailability.Birthday
            elif any(n in gacha.summary for n in ['コラボ限定', 'collaboration only']):
                return CardAvailability.Collab
            elif any(n in gacha.summary for n in ['期間限定', 'limited time']):
                return CardAvailability.Limited
            else:
                return CardAvailability.Permanent
        elif self.event:
            return CardAvailability.Welfare
        return CardAvailability.Unknown

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
            'head_y': self.head_y,
            'passive_skill': self.passive_skill,
            'gacha_card_attribute': self.gacha_card_attribute,
        }


class CardAvailability(enum.IntEnum):
    Unknown = enum.auto()
    Permanent = enum.auto()
    Limited = enum.auto()
    Collab = enum.auto()
    Birthday = enum.auto()
    Welfare = enum.auto()
