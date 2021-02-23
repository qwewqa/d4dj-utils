from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class SkillMaster(MasterAsset):
    id: int
    min_recovery_value: int
    max_recovery_value: int
    combo_support_count: int
    score_up_rate: int
    min_seconds: float
    max_seconds: float
    perfect_score_up_rate: int

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
            'perfect_score_up_rate': self.score_up_rate,
            'min_seconds': self.min_seconds,
            'max_seconds': self.max_seconds
        }
