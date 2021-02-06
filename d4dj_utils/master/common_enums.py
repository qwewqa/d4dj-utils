from enum import Enum
from typing import Optional

from d4dj_utils.master.asset_manager import AssetManager
from d4dj_utils.master.master_asset import MasterAsset


class EventType(int, Enum):
    Nothing = 0  # None
    Bingo = 1
    Medley = 2
    Poker = 3
    Raid = 4


class ChartSectionType(int, Enum):
    Full = 0
    Begin = 1
    Middle = 2
    End = 3
    Unknown1 = 4


class DateSelectCateogry(int, Enum):
    Nothing = 0  # None
    Daily = 1
    Weekly = 2
    Monthly = 3


class RewardCategory(int, Enum):
    Stock = 1
    Card = 2
    ClubItem = 3
    Music = 4
    Stamp = 5
    Honor = 6
    Episode = 7
    Movies = 8

    def get_value(self, reward_id: int, manager: AssetManager) -> Optional[MasterAsset]:
        if self == self.Stock:
            return manager.stock_master[reward_id]
        elif self == self.Card:
            return manager.card_master[reward_id]
        elif self == self.ClubItem:
            return None
        elif self == self.Music:
            return manager.music_master[reward_id]
        elif self == self.Stamp:
            return None
        elif self == self.Honor:
            return None
        elif self == self.Episode:
            return None
        elif self == self.Movies:
            return None

    def get_name(self, reward_id: int, manager: AssetManager):
        value = self.get_value(reward_id, manager)
        if value:
            return f'{self.name} - {value}'
        return f'{self.name} #{reward_id}'
