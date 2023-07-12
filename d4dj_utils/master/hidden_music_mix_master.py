from dataclasses import dataclass
from typing import Dict, Any, Tuple, List

from d4dj_utils.master.hidden_music_mix_detail_master import HiddenMusicMixDetailMaster
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class HiddenMusicMixMaster(MasterAsset):
    id: int
    trigger_music_ids: Tuple[int]

    def __hash__(self):
        return self.id.__hash__()

    @property
    def details(self) -> List[HiddenMusicMixDetailMaster]:
        return [
            self.assets.hidden_music_mix_detail_master[self.id, i]
            for i in range(4)
        ]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {"trigger_music_ids": self.trigger_music_ids}

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            "trigger_music_ids": self.trigger_music_ids,
        }
