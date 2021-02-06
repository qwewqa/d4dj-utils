from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple

from d4dj_utils.master.common_enums import EventType
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class AchievementMaster(MasterAsset):
    id: int
    group_id: int
    sequence: int
    title: str
    description: str
    condition_id: int
    condition_values: Tuple[int]
    reward_ids: Tuple[int]
    command_id: int
    event_type_id: int
    is_hidden: bool
    notify_type_id: int

    @property
    def rewards(self):
        return [self.assets.reward_master[reward_id] for reward_id in self.reward_ids]

    @property
    def command(self):
        return self.assets.command_master[self.command_id]

    @property
    def event_type(self):
        return EventType(self.event_type_id)

    @property
    def notify_type(self):
        return AchievementNotifyType(self.notify_type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'description': self.description,
            'is_hidden': self.is_hidden,
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'group': self.group_id,
            'sequence': self.sequence,
            'description': self.description,
            'condition': self.condition_id,
            'condition_values': '[' + ', '.join(str(v) for v in self.condition_values) + ']',
            'rewards': '[' + ', '.join(str(r) for r in self.rewards) + ']',
            'command': self.command,
            'event_type': self.event_type.name,
            'is_hidden': self.is_hidden,
            'notify_type': self.notify_type.name
        }


class AchievementNotifyType(Enum):
    Default = 0
    PokerHand = 1
    BingoCard = 2
