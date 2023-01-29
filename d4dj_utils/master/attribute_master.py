from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset

attribute_translations = {
    "ストリート": "street",
    "パーティー": "party",
    "キュート": "cute",
    "クール": "cool",
    "エレガント": "elegant",
}


@dataclass
class AttributeMaster(MasterAsset):
    id: int
    name: str

    def __hash__(self):
        return self.id.__hash__()

    @property
    def en_name(self) -> str:
        return attribute_translations.get(self.name, self.name)

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {"en_name": self.en_name}

    @property
    def extended_description_items(self) -> Dict[str, str]:
        return {"en_name": self.en_name}
