from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset

@dataclass
class GachaSummaryWordMaster(MasterAsset):
    id: int
    text: str

    def __hash__(self):
        return self.id.__hash__()

    @classmethod
    def default(cls, assets) -> Dict:
        return {
            0: GachaSummaryWordMaster(id=0, text=""),
        }
