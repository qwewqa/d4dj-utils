from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.common_enums import RewardCategory
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class RewardMaster(MasterAsset):
    id: int
    reward_category_id: int
    reward_id: int
    amount: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def reward_category(self) -> "RewardCategory":
        return RewardCategory(self.reward_category_id)

    def get_friendly_description(self):
        return f"{self.amount}x {self.reward_category.get_friendly_name(self.reward_id, self.assets)}"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "reward": self.reward_category.get_name(self.reward_id, self.assets),
            "amount": self.amount,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "reward": self.reward_category.get_name(self.reward_id, self.assets),
            "amount": self.amount,
        }
