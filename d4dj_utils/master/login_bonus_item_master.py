from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple, Sequence

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class LoginBonusItemMaster(MasterAsset):
    login_bonus_id: int
    sequence: int
    reward_ids: Sequence[int]
    positions: Sequence[int]

    db_fields = ["login_bonus_id", "sequence"]

    def __hash__(self):
        return self.id.__hash__()

    @property
    def id(self):
        return self.login_bonus_id, self.sequence

    @property
    def login_bonus(self):
        return self.assets.login_bonus_master[self.login_bonus_id]

    @property
    def rewards(self):
        return [self.assets.reward_master[rid] for rid in self.reward_ids]

    @property
    def name_description(self) -> str:
        return f"({self.login_bonus_id}, {self.sequence})"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "rewards": self.rewards,
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            "login_bonus": self.login_bonus,
            "sequence": self.sequence,
            "rewards": self.rewards,
            "positions": self.positions,
        }


class LoginBonusType(Enum):
    Common = 0
    Campaign = 1
    Subscription = 2
    VipBronze = 3
    VipSilver = 4
    VipGold = 5
    VipPlatinum = 6
    EventBingo = 101
    EventMedley = 102
    EventPoker = 103
    EventRaid = 104
    EventSlot = 105
    EventGrow = 106
    EventRave = 107
