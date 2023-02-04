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
    story_unlock_date: msgpack.Timestamp
    show_exchange_button: bool
    exchange_shop_id: int
    top_prefab_path: str
    show_mission_button: bool
    bgm_path: str
    episode_type_id: int
    box_gacha_id: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def event_type(self):
        return EventType(self.event_type_id)

    @property
    def reception_close_datetime(self):
        return self.convert_timestamp(self.reception_close_date)

    @property
    def rank_fix_start_datetime(self):
        return self.convert_timestamp(self.rank_fix_start_date)

    @property
    def result_announcement_datetime(self):
        return self.convert_timestamp(self.result_announcement_date)

    @property
    def stock(self):
        return self.assets.stock_master.get(self.stock_id)

    @property
    def episode_characters(self):
        return [self.assets.character_master[cid] for cid in self.episode_character_ids]

    @property
    def story_unlock_datetime(self):
        return self.convert_timestamp(self.story_unlock_date)

    @property
    def images_path(self):
        return self.assets.path / "ondemand" / "event" / f"event_{self.id}"

    @property
    def logo_path(self):
        return self.images_path / "title_logo.png"

    @property
    def bonus(self):
        return self.assets.event_specific_bonus_master.get(self.id)

    @property
    def duration(self) -> datetime.timedelta:
        return self.reception_close_datetime - self.start_datetime

    @property
    def exchange_shop(self):
        return (
            self.assets.exchange_master.get(self.exchange_shop_id)
            if self.exchange_shop_id
            else None
        )

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
            "event_type": self.event_type,
            "start_date": self.start_datetime,
            "end_date": self.end_date,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return self.one_line_description_items


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
