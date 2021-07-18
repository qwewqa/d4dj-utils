from dataclasses import dataclass
from typing import Dict, Any

from d4dj_utils.master.common_enums import ChartSectionType
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ChartNoteCountMaster(MasterAsset):
    chart_id: int
    section_id: int
    count: int

    def __hash__(self):
        return self.id.__hash__()

    @property
    def id(self):
        return self.chart_id, self.section_id

    @property
    def section(self):
        return ChartSectionType(self.section_id)

    @property
    def chart(self):
        return self.assets.chart_master.get(self.chart_id)

    @property
    def name_description(self) -> str:
        return f'({self.chart_id}, {self.section.name})'

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {'count': self.count}

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            'count': self.count,
            'chart': self.chart
        }
