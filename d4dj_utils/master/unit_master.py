from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class UnitMaster(MasterAsset):
    id: int
    name: str
    can_training: bool
    summary: str
    main_color_code: str
    sub_color_code: str
    short_name: str
    init_deck_character_ids: Tuple[int]

    def __hash__(self):
        return self.id.__hash__()

    @property
    def init_deck_characters(self):
        return [
            self.assets.character_master[cid] for cid in self.init_deck_character_ids
        ]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {"short_name": self.short_name or "none"}

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "can_training": self.can_training,
            "summary": self.summary,
            "main_color_code": self.main_color_code,
            "sub_color_code": self.sub_color_code,
            "short_name": self.short_name,
            "init_deck_characters": "["
            + ", ".join(str(c) for c in self.init_deck_characters)
            + "]",
        }
