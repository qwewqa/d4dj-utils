from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class GachaTableMaster(MasterAsset):
    id: int
    table_id: int
    card_id: int
    rate: int

    @property
    def card(self):
        return self.assets.card_master.get(self.card_id)

    @property
    def rate_value(self):
        return self.rate / 1000

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'card': self.card,
            'rate': self.rate_value
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'table_id': self.table_id,
            'card': self.card,
            'rate': self.rate_value
        }
