import dataclasses
import datetime
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, Any, Tuple, Sequence, TYPE_CHECKING, Union, Optional

import msgpack

from d4dj_utils.master.common_enums import GachaType, GachaCategory
from d4dj_utils.master.event_master import EventMaster
from d4dj_utils.master.gacha_bonus_master import GachaBonusMaster
from d4dj_utils.master.master_asset import MasterAsset


class GachaMaster:
    def __new__(cls, *args, **kwargs):
        if (
            isinstance(args[8], bool)
            and isinstance(args[9], msgpack.Timestamp)
            and isinstance(args[10], msgpack.Timestamp)
            and isinstance(args[11], int)
        ):
            return GachaMasterA(*args, **kwargs)
        elif isinstance(args[14], bool):
            return GachaMasterNew(*args, **kwargs)
        else:
            return GachaMasterLegacy(*args, **kwargs)


@dataclass
class GachaMasterA(GachaMaster, MasterAsset):
    id: int
    name: str
    table_rate_ids: Tuple[int, ...]
    table_ids: Tuple[int, ...]
    pick_up_card_ids: Tuple[int, ...]
    gacha_type_name: str
    summary_id: int
    has_specific_bg: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    detail_id: int
    note_id: int
    login_trigger_minutes: int
    show_home_animation: bool
    has_pick_up_duplicate_bonus: bool
    gacha_card_attribute: int
    ascending_sort_id: int
    category_id: int
    select_bonus_max_value: int
    select_bonus_card_ids: Tuple[int, ...]
    select_bonus_reward_ids: Tuple[int, ...]
    pick_up_duplicate_bonus_stock_ids: Tuple[int, ...]
    pick_up_duplicate_bonus_stock_amounts: Tuple[int, ...]
    gacha_type_id: int
    step_loop_count: int
    home_animation_card_ids: Any
    other_card_date: Any
    pick_up_level_max: Any = None
    share_cash_back_rate: Any = None
    random_bonus_max_value: Any = None
    random_bonus_stock_id: Any = None
    display_end_date: Any = None
    select_bonus_number: Any = None
    select_bonus_reduce_id: Any = None
    end_change_stock_item_id: Any = None
    end_change_stock_item_amount: Any = None

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __hash__(self):
        return self.id.__hash__()

    @property
    def bonus(self):
        return self.assets.gacha_bonus_master.get((self.id, True))

    @property
    def sub_bonus(self):
        return self.assets.gacha_bonus_master.get((self.id, False))

    @property
    def table_rates(self):
        return [
            self.assets.gacha_table_rate_master.get(rid) for rid in self.table_rate_ids
        ]

    @property
    def tables(self):
        cur = self.assets.db.cursor()
        return [
            [
                self.assets.gacha_table_master[gtmid[0]]
                for gtmid in cur.execute(
                    "SELECT id FROM GachaTableMaster WHERE table_id=?", [tid]
                )
            ]
            for tid in self.table_ids
        ]

    @property
    def pick_up_cards(self):
        return [self.assets.card_master.get(cid) for cid in self.pick_up_card_ids]

    @property
    def gacha_type(self):
        return GachaType(self.gacha_type_id)

    @property
    def category(self):
        return GachaCategory(self.category_id)

    @property
    def bonus_stock(self):
        return self.assets.stock_master.get(self.bonus_stock_id)

    @property
    def select_bonus_cards(self):
        return [self.assets.card_master[cid] for cid in self.select_bonus_card_ids]

    @property
    def select_bonus_rewards(self):
        return [self.assets.reward_master[rid] for rid in self.select_bonus_reward_ids]

    @property
    def pick_up_duplicate_bonus_stock(self):
        return [
            self.assets.stock_master[sid]
            for sid in self.pick_up_duplicate_bonus_stock_ids
        ]

    @property
    def draw_data(self):
        cur = self.assets.db.cursor()
        return [
            self.assets.gacha_draw_master[gdmid[0]]
            for gdmid in cur.execute(
                "SELECT id FROM GachaDrawMaster WHERE gacha_id=?", [self.id]
            )
        ]

    @cached_property
    def event(self) -> Optional[EventMaster]:
        return next(
            (
                event
                for event in self.assets.event_master.values()
                if event.start_datetime - datetime.timedelta(days=2)
                <= self.start_datetime
                <= event.end_datetime
            ),
            None,
        )

    @property
    def summary(self):
        return self.assets.gacha_summary_word_master.get(self.summary_id).text

    @property
    def banner_path(self):
        return self.assets.path / f"ondemand/gacha/top/banner/{self.id:>05}.png"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "pick_up_cards": self.pick_up_cards,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "table_rates": self.table_rates,
            "tables": self.tables,
            "pick_up_cards": self.pick_up_cards,
            "summary": self.summary,
            "has_specific_bg": self.has_specific_bg,
            "start_date": self.start_datetime,
            "end_date": self.end_datetime,
            "note": self.note,
            "detail": self.detail,
            "live_2d_bg": self.live_2d_bg,
            "login_trigger_minutes": self.login_trigger_minutes,
            "show_home_animation": self.show_home_animation,
            "has_pick_up_duplicate_bonus": self.has_pick_up_duplicate_bonus,
            "gacha_card_attribute_id": self.gacha_card_attribute_id,
            "ascending_sort_id": self.ascending_sort_id,
            "category": self.category,
            "bonus_stock": self.bonus_stock,
            "select_bonus_max_value": self.select_bonus_max_value,
            "select_bonus_cards": self.select_bonus_cards,
            "select_bonus_rewards": self.select_bonus_rewards,
            "pick_up_duplicate_bonus_stock": self.pick_up_duplicate_bonus_stock,
            "pick_up_duplicate_bonus_stock_amounts": self.pick_up_duplicate_bonus_stock_amounts,
            "gacha_type": self.gacha_type,
            "step_loop_count": self.step_loop_count,
            "draw_data": self.draw_data,
        }


@dataclass
class GachaMasterNew(GachaMaster, MasterAsset):
    id: int
    name: str
    table_rate_ids: Tuple[int, ...]
    table_ids: Tuple[int, ...]
    pick_up_card_ids: Tuple[int, ...]
    summary: str
    has_specific_bg: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    note: str
    detail: str
    live_2d_bg: Sequence[str]
    login_trigger_minutes: int
    show_home_animation: bool
    has_pick_up_duplicate_bonus: bool
    gacha_card_attribute_id: int
    ascending_sort_id: int
    category_id: int
    bonus_stock_id: int
    select_bonus_max_value: int
    select_bonus_card_ids: Tuple[int, ...]
    select_bonus_reward_ids: Tuple[int, ...]
    pick_up_duplicate_bonus_stock_ids: Tuple[int, ...]
    pick_up_duplicate_bonus_stock_amounts: Tuple[int, ...]
    gacha_type_id: int
    step_loop_count: int
    unknown1: Any
    unknown2: Any
    unknown3: Any = None
    unknown4: Any = None
    unknown5: Any = None
    unknown6: Any = None
    unknown7: Any = None

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __hash__(self):
        return self.id.__hash__()

    @property
    def bonus(self):
        return self.assets.gacha_bonus_master.get((self.id, True))

    @property
    def sub_bonus(self):
        return self.assets.gacha_bonus_master.get((self.id, False))

    @property
    def table_rates(self):
        return [
            self.assets.gacha_table_rate_master.get(rid) for rid in self.table_rate_ids
        ]

    @property
    def tables(self):
        cur = self.assets.db.cursor()
        return [
            [
                self.assets.gacha_table_master[gtmid[0]]
                for gtmid in cur.execute(
                    "SELECT id FROM GachaTableMaster WHERE table_id=?", [tid]
                )
            ]
            for tid in self.table_ids
        ]

    @property
    def pick_up_cards(self):
        return [self.assets.card_master.get(cid) for cid in self.pick_up_card_ids]

    @property
    def gacha_type(self):
        return GachaType(self.gacha_type_id)

    @property
    def category(self):
        return GachaCategory(self.category_id)

    @property
    def bonus_stock(self):
        return self.assets.stock_master.get(self.bonus_stock_id)

    @property
    def select_bonus_cards(self):
        return [self.assets.card_master[cid] for cid in self.select_bonus_card_ids]

    @property
    def select_bonus_rewards(self):
        return [self.assets.reward_master[rid] for rid in self.select_bonus_reward_ids]

    @property
    def pick_up_duplicate_bonus_stock(self):
        return [
            self.assets.stock_master[sid]
            for sid in self.pick_up_duplicate_bonus_stock_ids
        ]

    @property
    def draw_data(self):
        cur = self.assets.db.cursor()
        return [
            self.assets.gacha_draw_master[gdmid[0]]
            for gdmid in cur.execute(
                "SELECT id FROM GachaDrawMaster WHERE gacha_id=?", [self.id]
            )
        ]

    @property
    def banner_path(self):
        return self.assets.path / f"ondemand/gacha/top/banner/{self.id:>05}.png"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "pick_up_cards": self.pick_up_cards,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "table_rates": self.table_rates,
            "tables": self.tables,
            "pick_up_cards": self.pick_up_cards,
            "summary": self.summary,
            "has_specific_bg": self.has_specific_bg,
            "start_date": self.start_datetime,
            "end_date": self.end_datetime,
            "note": self.note,
            "detail": self.detail,
            "live_2d_bg": self.live_2d_bg,
            "login_trigger_minutes": self.login_trigger_minutes,
            "show_home_animation": self.show_home_animation,
            "has_pick_up_duplicate_bonus": self.has_pick_up_duplicate_bonus,
            "gacha_card_attribute_id": self.gacha_card_attribute_id,
            "ascending_sort_id": self.ascending_sort_id,
            "category": self.category,
            "bonus_stock": self.bonus_stock,
            "select_bonus_max_value": self.select_bonus_max_value,
            "select_bonus_cards": self.select_bonus_cards,
            "select_bonus_rewards": self.select_bonus_rewards,
            "pick_up_duplicate_bonus_stock": self.pick_up_duplicate_bonus_stock,
            "pick_up_duplicate_bonus_stock_amounts": self.pick_up_duplicate_bonus_stock_amounts,
            "gacha_type": self.gacha_type,
            "step_loop_count": self.step_loop_count,
            "draw_data": self.draw_data,
        }


@dataclass
class GachaMasterLegacy(GachaMaster, MasterAsset):
    id: int
    name: str
    table_rate_ids: Tuple[int, ...]
    table_ids: Tuple[int, ...]
    pick_up_card_ids: Tuple[int, ...]
    summary: str
    has_specific_bg: bool
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp
    note: str
    detail: str
    live_2d_bg: Sequence[str]
    bonus_max_value: int
    bonus_table_rate_id: int
    bonus_table_ids: Tuple[int, ...]
    login_trigger_minutes: int
    show_home_animation: bool
    has_pick_up_duplicate_bonus: bool
    is_tutorial: bool
    ascending_sort_id: int
    gacha_type_id: int
    bonus_stock_id: int
    bonus_selectable_cards_max_value: int = 0
    bonus_selectable_card_ids: Tuple[int, ...] = dataclasses.field(
        default_factory=lambda: []
    )
    select_bonus_reward_ids: Tuple[int, ...] = dataclasses.field(
        default_factory=lambda: []
    )
    pick_up_duplicate_bonus_stock_ids: Tuple[int, ...] = dataclasses.field(
        default_factory=lambda: []
    )
    pick_up_duplicate_bonus_stock_amounts: Tuple[int, ...] = dataclasses.field(
        default_factory=lambda: []
    )
    sub_bonus_max_value: int = 0
    sub_bonus_table_rate_id: int = 0
    sub_bonus_table_ids: Tuple[int, ...] = ()
    main_bonus_frame_text: str = ""
    sub_bonus_frame_text: str = ""

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __hash__(self):
        return self.id.__hash__()

    @property
    def bonus(self):
        if not self.bonus_max_value:
            return None
        return GachaBonusMaster(
            self.assets,
            self.id,
            True,
            self.bonus_max_value,
            self.bonus_table_rate_id,
            self.bonus_table_ids,
            self.main_bonus_frame_text,
        )

    @property
    def sub_bonus(self):
        if not self.sub_bonus_max_value:
            return None
        return GachaBonusMaster(
            self.assets,
            self.id,
            False,
            self.sub_bonus_max_value,
            self.sub_bonus_table_rate_id,
            self.sub_bonus_table_ids,
            self.sub_bonus_frame_text,
        )

    @property
    def table_rates(self):
        return [
            self.assets.gacha_table_rate_master.get(rid) for rid in self.table_rate_ids
        ]

    @property
    def tables(self):
        cur = self.assets.db.cursor()
        return [
            [
                self.assets.gacha_table_master[gtmid[0]]
                for gtmid in cur.execute(
                    "SELECT id FROM GachaTableMaster WHERE table_id=?", [tid]
                )
            ]
            for tid in self.table_ids
        ]

    @property
    def pick_up_cards(self):
        return [self.assets.card_master.get(cid) for cid in self.pick_up_card_ids]

    @property
    def bonus_table_rate(self):
        return self.assets.gacha_table_rate_master.get(self.bonus_table_rate_id)

    @property
    def bonus_tables(self):
        cur = self.assets.db.cursor()
        return [
            [
                self.assets.gacha_table_master[gtmid[0]]
                for gtmid in cur.execute(
                    "SELECT id FROM GachaTableMaster WHERE table_id=?", [tid]
                )
            ]
            for tid in self.bonus_table_ids
        ]

    @property
    def sub_bonus_table_rate(self):
        return self.assets.gacha_table_rate_master.get(self.sub_bonus_table_rate_id)

    @property
    def sub_bonus_tables(self):
        cur = self.assets.db.cursor()
        return [
            [
                self.assets.gacha_table_master[gtmid[0]]
                for gtmid in cur.execute(
                    "SELECT id FROM GachaTableMaster WHERE table_id=?", [tid]
                )
            ]
            for tid in self.sub_bonus_table_ids
        ]

    @property
    def gacha_type(self):
        return GachaType.Normal

    @property
    def category(self):
        return GachaCategory(self.gacha_type_id)

    @property
    def bonus_stock(self):
        return self.assets.stock_master.get(self.bonus_stock_id)

    @property
    def bonus_selectable_cards(self):
        return [self.assets.card_master[cid] for cid in self.bonus_selectable_card_ids]

    @property
    def select_bonus_cards(self):
        return self.bonus_selectable_cards

    @property
    def select_bonus_max_value(self):
        return self.bonus_selectable_cards_max_value

    @property
    def pick_up_duplicate_bonus_stock(self):
        return [
            self.assets.stock_master[sid]
            for sid in self.pick_up_duplicate_bonus_stock_ids
        ]

    @property
    def draw_data(self):
        cur = self.assets.db.cursor()
        return [
            self.assets.gacha_draw_master[gdmid[0]]
            for gdmid in cur.execute(
                "SELECT id FROM GachaDrawMaster WHERE gacha_id=?", [self.id]
            )
        ]

    @property
    def event(self):
        return self.pick_up_cards[0].event if self.pick_up_cards else None

    @property
    def banner_path(self):
        return self.assets.path / f"ondemand/gacha/top/banner/{self.id:>05}.png"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "pick_up_cards": self.pick_up_cards,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "table_rates": self.table_rates,
            "tables": self.tables,
            "pick_up_cards": self.pick_up_cards,
            "summary": self.summary,
            "has_specific_bg": self.has_specific_bg,
            "start_date": self.start_datetime,
            "end_date": self.end_datetime,
            "note": self.note,
            "detail": self.detail,
            "live_2d_bg": self.live_2d_bg,
            "bonus_max_value": self.bonus_max_value,
            "bonus_table_rate": self.bonus_table_rate,
            "bonus_tables": self.bonus_tables,
            "login_trigger_minutes": self.login_trigger_minutes,
            "show_home_animation": self.show_home_animation,
            "has_pick_up_duplicate_bonus": self.has_pick_up_duplicate_bonus,
            "is_tutorial": self.is_tutorial,
            "ascending_sort_id": self.ascending_sort_id,
            "category": self.category,
            "bonus_stock": self.bonus_stock,
            "bonus_selectable_cards_max_value": self.bonus_selectable_cards_max_value,
            "bonus_selectable_cards": self.bonus_selectable_cards,
            "select_bonus_reward_ids": self.select_bonus_reward_ids,
            "pick_up_duplicate_bonus_stock": self.pick_up_duplicate_bonus_stock,
            "pick_up_duplicate_bonus_stock_amounts": self.pick_up_duplicate_bonus_stock_amounts,
            "draw_data": self.draw_data,
            "sub_bonus_max_value": self.sub_bonus_max_value,
            "sub_bonus_table_rate": self.sub_bonus_table_rate,
            "sub_bonus_tables": self.sub_bonus_tables,
            "main_bonus_frame_text": self.main_bonus_frame_text,
            "sub_bonus_frame_text": self.sub_bonus_frame_text,
        }


if TYPE_CHECKING:
    GachaMaster = Union[GachaMasterNew, GachaMasterLegacy]
