import datetime
import enum
from dataclasses import dataclass
from typing import Dict, Any, Tuple

import msgpack

from d4dj_utils.master.common_enums import EventType
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class EventMaster(MasterAsset):
    id: int
    name: str
    event_type_id: int
    start_date: msgpack.Timestamp
    reception_close_date: msgpack.Timestamp
    rank_fix_start_date: msgpack.Timestamp
    result_announcement_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    stock_id: int
    entry_bonus_stock_amount: int
    stock_amount_per_use: int
    episode_character_ids: Tuple[int]
    display_card_id: int
    display_card_type_id: int
    story_unlock_date: msgpack.Timestamp
    show_exchange_button: bool
    exchange_shop_id: int
    is_d4_fes_story: bool
    top_prefab_path: str
    unknown1: bool
    unknown2: str

    @property
    def event_type(self):
        return EventType(self.event_type_id)

    @property
    def reception_close_datetime(self):
        return self.timestamp_to_jst(self.reception_close_date)

    @property
    def rank_fix_start_datetime(self):
        return self.timestamp_to_jst(self.rank_fix_start_date)

    @property
    def result_announcement_datetime(self):
        return self.timestamp_to_jst(self.result_announcement_date)

    @property
    def stock(self):
        return self.assets.stock_master.get(self.stock_id)

    @property
    def episode_characters(self):
        return [self.assets.character_master[cid] for cid in self.episode_character_ids]

    @property
    def display_card(self):
        return self.assets.card_master.get(self.display_card_id)

    @property
    def display_card_type(self):
        return CardIllustType(self.display_card_type_id)

    @property
    def story_unlock_datetime(self):
        return self.timestamp_to_jst(self.story_unlock_date)

    @property
    def images_path(self):
        return self.assets.path / 'ondemand' / 'event' / f'event_{self.id}'

    @property
    def logo_path(self):
        return self.images_path / 'title_logo.png'

    @property
    def bonus(self):
        return self.assets.event_specific_bonus_master[self.id]

    @property
    def duration(self) -> datetime.timedelta:
        return self.reception_close_datetime - self.start_datetime

    @property
    def exchange_shop(self):
        return self.assets.exchange_master.get(self.exchange_shop_id) if self.exchange_shop_id else None

    def state(self, time=None):
        if not time:
            time = datetime.datetime.now(datetime.timezone.utc)

        if time < self.start_datetime:
            return EventState.Upcoming
        elif time < self.reception_close_datetime:
            return EventState.Open
        elif time < self.rank_fix_start_datetime:
            return EventState.Closing
        elif time < self.result_announcement_datetime:
            return EventState.Ranks_Fixed
        elif time < self.end_datetime:
            return EventState.Results
        else:
            return EventState.Ended

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type,
            'start_date': self.start_datetime,
            'end_date': self.end_date,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type.name,
            'start_date': self.start_datetime,
            'reception_close_date': self.reception_close_datetime,
            'rank_fix_start_date': self.rank_fix_start_datetime,
            'result_announcement_date': self.result_announcement_datetime,
            'end_date': self.end_datetime,
            'stock': self.stock,
            'entry_bonus_stock_amount': self.entry_bonus_stock_amount,
            'stock_amount_per_use': self.stock_amount_per_use,
            'episode_characters': '[' + ' ,'.join(str(c) for c in self.episode_characters) + ']',
            'display_card': self.display_card,
            'display_card_type': self.display_card_type.name,
            'story_unlock_date': self.story_unlock_datetime,
            'show_exchange_button': self.show_exchange_button,
            'exchange_shop': self.exchange_shop,
            'is_d4_fes_story': self.is_d4_fes_story,
            'top_prefab_path': self.top_prefab_path,
            'unknown1': self.unknown1,
            'unknown2': self.unknown2,
        }


class CardIllustType(enum.Enum):
    Normal = 0
    LimitBreak = 1
    MaxLimitBreak = 2


class EventState(int, enum.Enum):
    Upcoming = 1
    Open = 2
    Closing = 3
    Ranks_Fixed = 4
    Results = 5
    Ended = 6
