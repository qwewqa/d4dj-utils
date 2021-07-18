from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class MissionGroupMaster(MasterAsset):
    id: int
    category_id: int
    name: str
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    reset_type_id: int
    reset_value: int
    subscription_id: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def category(self):
        return MissionCategory(self.category_id)

    @property
    def reset_type(self):
        return DateSelectCategory(self.reset_type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category.name,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'category': self.category.name,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'reset_type': self.reset_type.name,
            'reset_value': self.reset_value,
            'subscription_id': self.subscription_id
        }


class MissionCategory(Enum):
    Achievement = 0
    Tutorial = 1
    Chart = 2
    TimeLimited = 3


class DateSelectCategory(Enum):
    Nothing = 0  # None
    Daily = 1
    Weekly = 2
    Monthly = 3
