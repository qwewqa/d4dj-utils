from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ChartDesignerMaster(MasterAsset):
    id: int
    name: str

    def __hash__(self):
        return self.id.__hash__()

    @property
    def name_description(self) -> str:
        return f"{self.id}"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {"name": self.name}
