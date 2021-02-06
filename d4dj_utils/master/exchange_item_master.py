from dataclasses import dataclass
from typing import Dict, Any

import msgpack

from d4dj_utils.master.common_enums import RewardCategory
from d4dj_utils.master.master_asset import MasterAsset
from d4dj_utils.master.mission_group_master import DateSelectCategory


@dataclass
class ExchangeItemMaster(MasterAsset):
    id: int
    exchange_id: int
    price: int
    reward_category_id: int
    reward_id: int
    reward_amount: int
    exchange_count: int
    reset_type_id: int
    reset_value: int
    recommended: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    unknown1: int
    unknown2: int
    unknown3: int
    unknown4: int
    unknown5: int
    unknown6: int
    unknown7: int
    unknown8: int

    @property
    def exchange(self):
        return self.assets.exchange_master.get(self.exchange_id)

    @property
    def reward_category(self) -> 'RewardCategory':
        return RewardCategory(self.reward_category_id)

    @property
    def reward(self):
        return self.reward_category.get_value(self.reward_id, self.assets)

    @property
    def reward_name(self):
        return self.reward_category.get_name(self.reward_id, self.assets)

    @property
    def reset_type(self):
        return DateSelectCategory(self.reset_type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'exchange': self.exchange,
            'price': self.price,
            'reward': self.reward_name,
            'reward_amount': self.reward_amount,
            'exchange_count': self.exchange_count,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'exchange': self.exchange,
            'price': self.price,
            'reward': self.reward_name,
            'reward_amount': self.reward_amount,
            'exchange_count': self.exchange_count,
            'reset_type': self.reset_type.name,
            'reset_value': self.reset_value,
            'recommended': self.recommended,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'unknown1': self.assets.stock_master.get(self.unknown1),
            'unknown2': self.unknown2,
            'unknown3': self.unknown3,
            'unknown4': self.unknown4,
            'unknown5': self.unknown5,
            'unknown6': self.unknown6,
            'unknown7': self.unknown7,
            'unknown8': self.unknown8,
        }
