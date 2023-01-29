from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class CharacterMaster(MasterAsset):
    id: int
    full_name: str
    first_name: str
    first_name_english: str
    unit_id: int
    profile_answers: Tuple[str]
    full_name_english: str
    color_code: str

    def __hash__(self):
        return self.id.__hash__()

    @property
    def unit(self):
        return self.assets.unit_master[self.unit_id]

    @property
    def name_description(self) -> str:
        return f"{self.full_name} ({self.id})"

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "full_name_english": self.full_name_english,
            "unit": self.unit,
            "color_code": self.color_code,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "first_name": self.first_name,
            "full_name": self.full_name,
            "first_name_english": self.first_name_english,
            "full_name_english": self.full_name_english,
            "unit": self.unit,
            "color_code": self.color_code,
            "profile_answers": self.profile_answers,
        }
