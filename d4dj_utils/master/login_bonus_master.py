from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple, Sequence

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class LoginBonusMaster(MasterAsset):
    id: int
    login_bonus_type_id: int
    title: str
    order: int
    loop: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    subscription_id: int
    background_image: str
    foreground_image: str
    date_positions: Sequence[int]
    limit_days: int

    @property
    def login_bonus_type(self):
        return LoginBonusType(self.login_bonus_type_id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'login_bonus_type': self.login_bonus_type,
            'start_date': self.start_date,
        }

    @property
    def image_path(self):
        return self.assets.path / f'ondemand/loginBonus/loginBonus_{str(self.id).zfill(4)}.jpg'

    @property
    def items(self):
        cur = self.assets.db.cursor()
        return [self.assets.login_bonus_item_master[lbimid]
                for lbimid in
                cur.execute('SELECT login_bonus_id, sequence FROM LoginBonusItemMaster WHERE login_bonus_id=?', [self.id])]

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'login_bonus_type': self.login_bonus_type,
            'order': self.order,
            'loop': self.loop,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'subscription_id': self.subscription_id,
            'background_image': self.background_image,
            'foreground_image': self.foreground_image,
            'date_positions': self.date_positions,
            'limit_days': self.limit_days,
            'items': self.items,
        }


class LoginBonusType(Enum):
    Common = 0
    Campaign = 1
    Subscription = 2
    VipBronze = 3
    VipSilver = 4
    VipGold = 5
    VipPlatinum = 6
