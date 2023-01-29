from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class RarityMaster(MasterAsset):
    id: int
    max_levels: Tuple[int]
    max_level_parameter_rates: Tuple[int]
    limit_break_bonuses: Tuple[int]
    seal_amount: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def max_level(self):
        return max(self.max_levels)

    @property
    def total_limit_break_bonus(self):
        return sum(self.limit_break_bonuses)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "max_level": self.max_level,
            "total_limit_break_bonus": self.total_limit_break_bonus,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "max_levels": self.max_levels,
            "max_level_parameter_rates": self.max_level_parameter_rates,
            "limit_break_bonuses": self.limit_break_bonuses,
            "total_limit_break_bonus": self.total_limit_break_bonus,
            "seal_amount": self.seal_amount,
        }
