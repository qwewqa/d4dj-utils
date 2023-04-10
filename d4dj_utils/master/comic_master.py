from dataclasses import dataclass
from pathlib import Path

import msgpack

from d4dj_utils.master.master_asset import MasterAsset


@dataclass
class ComicMaster(MasterAsset):
    id: int
    title: str
    episode_number: str
    start_date: msgpack.Timestamp
    end_date: msgpack.Timestamp

    @property
    def comic_path(self) -> Path:
        return (
            self.assets.path / "ondemand" / "Comic" / "Content" / f"comic_{self.id:>07}.jpg"
        )
