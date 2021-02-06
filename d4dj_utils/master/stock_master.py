from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class StockMaster(MasterAsset):
    id: int
    name: str
    category_id: int
    view_id: int
    summary: str
    attribute_id: int
    rarity: int
    exp: int
    buff_character_id: int
    recovery_amount: int
    consume_amount: int
    max_amount: int
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    is_appropriate_sales: bool

    @property
    def category(self):
        return StockCategory(self.category_id)

    @property
    def view(self):
        return self.assets.stock_view_category_master.get(self.view_id)

    @property
    def attribute(self):
        return self.assets.attribute_master.get(self.attribute_id)

    @property
    def buff_character(self):
        return self.assets.character_master.get(self.buff_character_id)

    FreeDiamondId = 1
    PaidDiamondId = 2
    CoverMusicMedalId = 701
    CoverOwnMusicMedalId = 702
    InstMusicMedalId = 703
    InstOwnMusicMedalId = 704
    CoinId = 9901
    SoundShellId = 9902
    BuffSkillExpMultiplier = 5
    BuffExpMultiplier = 25

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category.name if self.category else None,
            'summary': self.summary
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'category': self.category.name if self.category else None,
            'view': self.view,
            'summary': self.summary,
            'attribute': self.attribute,
            'rarity': self.rarity,
            'exp': self.exp,
            'buff_character': self.buff_character,
            'recovery_amount': self.recovery_amount,
            'consume_amount': self.consume_amount,
            'max_amount': self.max_amount,
            'start_date': self.start_datetime,
            'end_date': self.end_datetime,
            'is_appropriate_sales': self.is_appropriate_sales
        }


class StockCategory(Enum):
    Diamond = 0
    Fragment = 1
    Exp = 2
    SkillExp = 3
    LimitBreak = 4
    VoltageRecovery = 5
    Boost = 6
    MusicShop = 7
    Event = 8
    GachaTicket = 9
    Random = 10
    Point = 99
