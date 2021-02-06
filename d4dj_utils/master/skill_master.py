from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class SkillMaster(MasterAsset):
    id: int
    min_recovery_value: int
    max_recovery_value: int
    judge_expand_value: int
    score_up_rate: int
    min_seconds: float
    max_seconds: float

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            'max_recovery_value': self.max_recovery_value,
            'judge_expand_value': self.judge_expand_value,
            'score_up_rate': self.score_up_rate,
            'max_seconds': self.max_seconds
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'min_recovery_value': self.min_recovery_value,
            'max_recovery_value': self.max_recovery_value,
            'judge_expand_value': self.judge_expand_value,
            'score_up_rate': self.score_up_rate,
            'min_seconds': self.min_seconds,
            'max_seconds': self.max_seconds
        }
