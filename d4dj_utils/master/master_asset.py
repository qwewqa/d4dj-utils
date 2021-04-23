import abc
import dataclasses
import datetime
import textwrap
from pathlib import Path
from typing import Dict, Any, Iterable, TypeVar, MutableMapping, Optional

import msgpack
import pytz as pytz

import d4dj_utils.master.asset_manager as am

try:
    import d4dj_utils.extended.tools.tools as tools
except (ImportError, ModuleNotFoundError):
    tools = None

KT = TypeVar('KT')
VT = TypeVar('VT')


@dataclasses.dataclass
class MasterAsset(abc.ABC):
    asset_manager: 'dataclasses.InitVar[am.AssetManager]'
    db_fields = {}

    def __post_init__(self, asset_manager):
        self.assets = asset_manager

    def __str__(self):
        if self.one_line_description_items:
            return f'{self.name_description} ({self.one_line_description()})'
        else:
            return self.name_description

    @property
    def name_description(self) -> str:
        if hasattr(self, 'id'):
            if hasattr(self, 'name'):
                return f'{self.name} ({self.id})'
            elif hasattr(self, 'title'):
                return f'{self.title} ({self.id})'
            else:
                return f'{self.id}'
        raise NotImplementedError

    def one_line_description(self):
        def format_desc(desc):
            if isinstance(desc, (tuple, list)):
                return '[' + ', '.join(str(v) for v in desc) + ']'
            else:
                return str(desc)
        return ', '.join(f'{k}: {format_desc(v)}' for k, v in self.one_line_description_items.items())

    def extended_description(self) -> str:
        def gen_lines():
            for key, desc in self.extended_description_items.items():
                if isinstance(desc, (tuple, list)):
                    if len(desc) > 2:
                        join_str = ",\n"
                        yield f'{key}: [\n{textwrap.indent(join_str.join(str(item) for item in desc), "    ")}\n]'
                    else:
                        yield f'{key}: [{", ".join(str(item) for item in desc)}]'
                else:
                    desc = str(desc)
                    if '\n' in desc:
                        yield f'{key}:\n{textwrap.indent(desc, "   |")}'
                    else:
                        yield f'{key}: {desc}'

        return '\n'.join(gen_lines())

    @property
    @abc.abstractmethod
    def one_line_description_items(self) -> Dict[str, Any]:
        return {}

    @property
    @abc.abstractmethod
    def extended_description_items(self) -> Dict[str, Any]:
        return {}

    @property
    def is_released(self):
        return self.start_datetime is None or self.start_datetime < datetime.datetime.now(datetime.timezone.utc)

    @property
    def is_available(self):
        return self.start_datetime is None or self.start_datetime < datetime.datetime.now(
            datetime.timezone.utc) < self.end_datetime

    @staticmethod
    def timestamp_to_jst(timestamp: msgpack.Timestamp):
        return pytz.timezone('Asia/Tokyo').localize(timestamp.to_datetime().replace(tzinfo=None))

    @property
    def start_datetime(self) -> Optional[datetime.datetime]:
        if hasattr(self, 'start_date') and isinstance(self.start_date, msgpack.Timestamp):
            return self.timestamp_to_jst(self.start_date)
        return None

    @property
    def end_datetime(self) -> Optional[datetime.datetime]:
        if hasattr(self, 'end_date') and isinstance(self.end_date, msgpack.Timestamp):
            return self.timestamp_to_jst(self.end_date)
        return None

    def as_tuple(self):
        return dataclasses.astuple(self)


class MasterDict(dict, MutableMapping[KT, VT]):
    def __init__(self, base: Dict[Any, MasterAsset], name: str, path: Path):
        self.path = path
        self.name = name
        super().__init__(base)

    def formatted(self, filter_function=None, sort_key=None):
        values: Iterable[MasterAsset]
        if filter_function:
            values = [v for v in self.values() if filter_function(v)]
        else:
            values = self.values()

        if sort_key:
            values = sorted(values, key=sort_key)

        return '\n'.join(f'{v.name_description}:\n{textwrap.indent(v.extended_description(), "    ")}' for v in values)

    def save(self, encrypt=True):
        with self.path.open('wb+') as f:
            msgpack.dump({k: v.as_tuple() for k, v in self.items()}, f)
        if encrypt:
            tools.encrypt_asset(self.path)
