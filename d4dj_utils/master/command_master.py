from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class CommandMaster(MasterAsset):
    id: int
    title: str
    command: str

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {'command': self.command}

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {'command': self.command}

