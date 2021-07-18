from dataclasses import dataclass
from dataclasses import dataclass
from typing import Dict, Any, Sequence

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class EventMedleySetlistMaster(MasterAsset):
    id: int
    name: str
    music_ids: Sequence[int]
    required_point: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def music(self):
        return [self.assets.music_master.get(mid) for mid in self.music_ids]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'music': self.music,
            'required_point': self.required_point,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'music': self.music,
            'required_point': self.required_point,
        }
