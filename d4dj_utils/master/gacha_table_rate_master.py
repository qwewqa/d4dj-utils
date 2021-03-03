from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class GachaTableRateMaster(MasterAsset):
    id: int
    rates: Tuple[int]
    tab_name: str
    description: str

    @property
    def normalized_rates(self):
        rate_sum = sum(self.rates)
        return [rate / rate_sum for rate in self.rates]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'tab_name': self.tab_name
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'rates': self.rates,
            'normalized_rates': self.normalized_rates,
            'tab_name': self.tab_name,
            'description': self.description,
        }
