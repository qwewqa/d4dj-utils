from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class MissionDetailMaster(MasterAsset):
    id: int
    panel_id: int
    sequence: int
    title: str
    description: str
    condition_id: int
    condition_values: Tuple[int]
    reward_ids: Tuple[int]
    command_id: int
    home_priority: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def panel(self):
        return self.assets.mission_panel_master[self.panel_id]

    @property
    def rewards(self):
        return [self.assets.reward_master[rid] for rid in self.reward_ids]

    @property
    def command(self):
        return self.assets.command_master[self.command_id]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'description': self.description
        }

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {
            'panel': self.panel,
            'sequence': self.sequence,
            'description': self.description,
            'condition_id': self.condition_id,
            'condition_values': self.condition_values,
            'rewards': '[' + ', '.join(str(r) for r in self.rewards) + ']',
            'command': self.command,
            'home_priority': self.home_priority
        }
