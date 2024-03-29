import math
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from PIL import Image, ImageDraw

from d4dj_utils.chart.chart import Chart, ChartCommonData
from d4dj_utils.master.common_enums import ChartSectionType
from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ChartMaster(MasterAsset):
    id: int
    music_id: int
    difficulty_id: int
    level: float
    achieve_id: int
    trends: Tuple[float]
    override_level: str
    chart_designer_id: Any

    def __hash__(self):
        return self.id.__hash__()

    @property
    def display_level(self):
        return self.override_level or str(math.floor(self.level)) + (
            "+" if self.level % 1 == 0.5 else ""
        )

    @property
    def music(self):
        return self.assets.music_master[self.music_id]

    @property
    def mix_info(self):
        return self.music.mix_info

    @property
    def difficulty(self):
        return ChartDifficulty(self.difficulty_id)

    @property
    def designer(self):
        return self.assets.chart_designer_master[self.chart_designer_id]

    @property
    def one_line_description_items(self) -> Dict[str, Any]:
        return {
            "music": self.music,
            "difficulty": self.difficulty.name,
            "level": self.level,
            "override_level": self.override_level,
        }

    @property
    def extended_description_items(self) -> Dict[str, Any]:
        return {
            "music": self.music,
            "difficulty": self.difficulty.name,
            "level": self.level,
            "override_level": self.override_level,
            "achieve_id": self.achieve_id,
            "trends": self.trends,
            "note_counts": "("
            + ", ".join(
                f"{k.name}: {v.count if v else None}"
                for k, v in self.note_counts.items()
            )
            + ")",
            "chart_designer": self.designer.name,
        }

    @property
    def note_counts(self):
        note_count_master = self.assets.chart_note_count_master
        return {
            ChartSectionType.Full: note_count_master.get(
                (self.id, ChartSectionType.Full.value)
            ),
            ChartSectionType.Begin: note_count_master.get(
                (self.id, ChartSectionType.Begin.value)
            ),
            ChartSectionType.Middle: note_count_master.get(
                (self.id, ChartSectionType.Middle.value)
            ),
            ChartSectionType.End: note_count_master.get(
                (self.id, ChartSectionType.End.value)
            ),
        }

    @property
    def chart_path(self) -> Path:
        return (
            self.assets.path / "ondemand" / "chart" / f"chart_{str(self.id).zfill(8)}"
        )

    @property
    def common_data_path(self) -> Path:
        return (
            self.assets.path
            / "ondemand"
            / "chart"
            / f"chart_{str(self.id).zfill(8)[:-1]}0"
        )

    @property
    def image_path(self) -> Path:
        return self.chart_path.with_suffix(".png")

    @property
    def mix_path(self) -> Path:
        return self.chart_path.with_suffix(".mix.png")

    def load_chart_data(self):
        with self.chart_path.open("rb") as f:
            try:
                with self.common_data_path.open("rb") as cdf:
                    info = ChartCommonData.from_msgpack(cdf.read()).get_chart_info(self)
            except FileNotFoundError:
                if self.music.duration:
                    info = ChartCommonData.get_default_for_chart(self).get_chart_info(
                        self
                    )
                else:
                    info = None
            return Chart.from_msgpack(f.read(), info)

    def load_common_data(self):
        try:
            with self.common_data_path.open("rb") as cdf:
                return ChartCommonData.from_msgpack(cdf.read())
        except FileNotFoundError:
            if self.music.duration:
                return ChartCommonData.get_default_for_chart(self)
            else:
                return None

    def load_sections(self) -> Optional[List[Chart]]:
        if not self.mix_info:
            return None
        chart = self.load_chart_data()
        return [
            chart.trim(
                mi.start_time - 60 / mi.start_time_bpm / 8,
                mi.end_time - 60 / mi.end_time_bpm / 8,
            )
            for mi in self.mix_info.values()
        ]

    def load_section(self, section) -> Optional[List[Chart]]:
        if not self.mix_info:
            return None
        chart = self.load_chart_data()
        mi = self.mix_info[section]
        return chart.trim(
            mi.start_time - 60 / mi.start_time_bpm / 8,
            mi.end_time - 60 / mi.end_time_bpm / 8,
        )

    @staticmethod
    def render_sections(sections: List[Chart]) -> Image:
        padding = 80
        separator_width = 11

        images = [chart.render() for chart in sections]
        width = sum(image.width for image in images) + (len(images) - 1) * padding
        height = max(image.height for image in images)

        combined = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(combined)

        x_offset = 0
        for image in images:
            if x_offset:
                separator_x = x_offset - padding / 2
                draw.line(
                    (separator_x, 0, separator_x, height),
                    fill=(78, 43, 219),
                    width=separator_width,
                )
            combined.paste(image, (x_offset, 0))
            x_offset += image.width + padding

        return combined


class ChartDifficulty(int, Enum):
    Nothing = 0  # None
    Easy = 1
    Normal = 2
    Hard = 3
    Expert = 4
