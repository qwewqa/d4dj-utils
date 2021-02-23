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
    reward_category_id: int
    reward_id: int
    reward_amount: int
    exchange_count: int
    reset_type_id: int
    reset_value: int
    recommended: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    required_stock_id_1: int
    required_stock_amount_1: int
    required_stock_id_2: int
    required_stock_amount_2: int
    required_stock_id_3: int
    required_stock_amount_3: int
    required_stock_id_4: int
    required_stock_amount_4: int

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
    def required_stock_1(self):
        return self.assets.stock_master.get(self.required_stock_id_1)
    
    @property
    def required_stock_2(self):
        return self.assets.stock_master.get(self.required_stock_id_2)
    
    @property
    def required_stock_3(self):
        return self.assets.stock_master.get(self.required_stock_id_3)
    
    @property
    def required_stock_4(self):
        return self.assets.stock_master.get(self.required_stock_id_4)
    
    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'exchange': self.exchange,
            'reward': self.reward_name,
            'reward_amount': self.reward_amount,
            'exchange_count': self.exchange_count,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'exchange': self.exchange,
            'reward': self.reward_name,
            'reward_amount': self.reward_amount,
            'exchange_count': self.exchange_count,
            'reset_type': self.reset_type.name,
            'reset_value': self.reset_value,
            'recommended': self.recommended,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'required_stock_1': self.required_stock_1,
            'required_stock_amount_1': self.required_stock_amount_1,
            'required_stock_2': self.required_stock_2,
            'required_stock_amount_2': self.required_stock_amount_2,
            'required_stock_3': self.required_stock_3,
            'required_stock_amount_3': self.required_stock_amount_3,
            'required_stock_4': self.required_stock_4,
            'required_stock_amount_4': self.required_stock_amount_4,
        }
