from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class MissionPanelMaster(MasterAsset):
    id: int
    group_id: int
    banner_group: int
    step: int
    name: str
    all_complete_reward_ids: Tuple[int]

    @property
    def group(self):
        return self.assets.mission_group_master[self.group_id]

    @property
    def all_complete_rewards(self):
        return [self.assets.reward_master[rid] for rid in self.all_complete_reward_ids]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'group': self.group,
            'banner_group': self.banner_group,
            'step': self.step
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'group': self.group,
            'banner_group': self.banner_group,
            'step': self.step,
            'all_complete_rewards': '[' + ', '.join(str(r) for r in self.all_complete_rewards) + ']'
        }
