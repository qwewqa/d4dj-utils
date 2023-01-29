from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ConditionMaster(MasterAsset):
    id: int
    category_id: int
    value: Tuple[int]

    def __hash__(self):
        return self.id.__hash__()

    @property
    def category(self) -> "ConditionCategory":
        return ConditionCategory(self.category_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {"category": self.category.name, "value": self.value}

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {"category": self.category.name, "value": self.value}


class ConditionCategory(Enum):
    Nothing = 0  # None
    UserLevel = 1
    UnitLevel = 2
    ClubItem = 3
    Story = 4
    EventPoint = 5
    CharacterRank = 6
    Unreleased = 99
