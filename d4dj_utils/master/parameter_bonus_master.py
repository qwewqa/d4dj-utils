from dataclasses import dataclass

from d4dj_utils.master.common_enums import ParameterBonus
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ParameterBonusMaster(MasterAsset):
    id: int
    target_id: int
    value: int

    def __hash__(self):
        return hash(self.id)

    @property
    def target(self) -> ParameterBonus:
        return ParameterBonus(self.target_id)
