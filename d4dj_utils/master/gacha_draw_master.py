from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class GachaDrawMaster(MasterAsset):
    id: int
    gacha_id: int
    draw_amounts: Tuple[int]
    stock_id: int
    stock_amount: int
    draw_limit: int
    is_reset_limit_every_day: bool
    roulette_targets_id: Tuple[int, ...] = ()
    roulette_rates: Tuple[int, ...] = ()

    db_fields = ["id", "gacha_id"]

    def __hash__(self):
        return self.id.__hash__()

    @property
    def gacha(self):
        return self.assets.gacha_master.get(self.gacha_id)

    @property
    def stock(self):
        return self.assets.stock_master.get(self.stock_id)

    @property
    def roulette_targets(self):
        return [
            self.assets.gacha_roulette_master[rid] for rid in self.roulette_targets_id
        ]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "gacha": self.gacha,
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            "gacha": self.gacha,
            "draw_amounts": self.draw_amounts,
            "stock": self.stock,
            "stock_amount": self.stock_amount,
            "draw_limit": self.draw_limit,
            "is_reset_limit_every_day": self.is_reset_limit_every_day,
            "roulette_targets": self.roulette_targets,
            "roulette_rates": self.roulette_rates,
        }
