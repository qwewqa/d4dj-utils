from dataclasses import dataclass
from typing import Dict, Any

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ExchangeMaster(MasterAsset):
    id: int
    name: str
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    is_tab_visible: bool
    is_polling_place: bool
    category_name: str = ''
    order: int = 0

    def __hash__(self):
        return self.id.__hash__()

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'start_date': self.start_datetime
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'is_tab_visible': self.is_tab_visible,
            'is_polling_place': self.is_polling_place,
            'category_name': self.category_name,
            'order': self.order,
        }
