from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class CardExpMaster(MasterAsset):
    level: int
    total_exp: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def id(self):
        return self.level

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {"total_exp": self.total_exp}

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {"total_exp": self.total_exp}
