from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class GachaBonusMaster(MasterAsset):
    gacha_id: int
    is_main: bool
    max_value: int
    table_rate_id: int
    table_ids: Tuple[int, ...]
    text: str

    def __hash__(self):
        return self.id.__hash__()

    @property
    def id(self):
        return self.gacha_id, self.is_main

    @property
    def gacha(self):
        return self.assets.gacha_master[self.gacha_id]

    @property
    def table_rate(self):
        return self.assets.gacha_table_rate_master.get(self.table_rate_id)

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
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "gacha": self.gacha,
            "is_main": self.is_main,
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            "gacha": self.gacha,
            "is_main": self.gacha,
            "max_value": self.max_value,
            "table_rate": self.table_rate,
            "tables": self.tables,
            "text": self.text,
        }

    @classmethod
    def default(cls, assets) -> Dict:
        return {}
