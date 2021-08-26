from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class GachaTableRateMaster(MasterAsset):
    id: int
    rates: Tuple[int]
    rarity_ids: Tuple[int]
    tab_name: str
    description: str

    def __hash__(self):
        return self.id.__hash__()

    def __init__(self, *args):
        self.assets = args[0]
        args = args[1:]
        if len(args) == 5:
            self.id = args[0]
            self.rates = args[1]
            self.rarity_ids = args[2]
            self.tab_name = args[3]
            self.description = args[4]
        elif len(args) == 4:
            self.id = args[0]
            self.rates = args[1]
            self.rarity_ids = ()
            self.tab_name = args[2]
            self.description = args[3]
        else:
            raise NotImplementedError()

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
            'rarity_ids': self.rarity_ids,
        }
