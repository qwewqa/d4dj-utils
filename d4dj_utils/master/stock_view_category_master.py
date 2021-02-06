from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class StockViewCategoryMaster(MasterAsset):
    id: int
    name: str

    @property
    def name_description(self) -> str:
        return str(self.id)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {'name': self.name}

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {'name': self.name}
