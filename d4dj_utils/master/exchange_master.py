from dataclasses import dataclass
from typing import Dict, Any

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ExchangeMaster(MasterAsset):
    id: int
    name: str
    stock_id: int
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    # is_tab_visible: bool
    visible_only_have_target_item: bool

    @property
    def stock(self):
        return self.assets.stock_master.get(self.stock_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'stock': self.stock
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'stock': self.stock,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            # 'is_tab_visible': self.is_tab_visible,
            'visible_only_have_target_item': self.visible_only_have_target_item,
        }
