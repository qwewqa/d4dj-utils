from dataclasses import dataclass
from typing import Dict, Any, Tuple

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class SkillMaster(MasterAsset):
    id: int = 0
    min_recovery_value: int = 0
    max_recovery_value: int = 0
    combo_support_count: int = 0
    score_up_rate: int = 0
    min_seconds: float = 0
    max_seconds: float = 0
    perfect_score_up_rate: int = 0
    group_bonus_character_ids: Tuple[int, ...] = ()
    group_bonus_rates: Tuple[int, ...] = ()

    def __hash__(self):
        return self.id.__hash__()

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'max_recovery_value': self.max_recovery_value,
            'combo_support_count': self.combo_support_count,
            'score_up_rate': self.score_up_rate,
            'perfect_score_up_rate': self.score_up_rate,
            'max_seconds': self.max_seconds
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'min_recovery_value': self.min_recovery_value,
            'max_recovery_value': self.max_recovery_value,
            'combo_support_count': self.combo_support_count,
            'score_up_rate': self.score_up_rate,
            'perfect_score_up_rate': self.perfect_score_up_rate,
            'min_seconds': self.min_seconds,
            'max_seconds': self.max_seconds
        }
