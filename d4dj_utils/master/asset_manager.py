import logging
import textwrap
from pathlib import Path
from typing import Type, Dict, Tuple

import msgpack

import d4dj_utils.master.master_asset as ma
from d4dj_utils.chart.chart import load_chart


class AssetManager:
    def __init__(self, path):
        self.logger = logging.getLogger(__name__)
        self.path = Path(path)
        self.masters: Dict[str, ma.MasterDict] = {}
        from d4dj_utils.master.achievement_master import AchievementMaster
        self.achievement_master: ma.MasterDict[int, AchievementMaster] = self._load_master(AchievementMaster)
        from d4dj_utils.master.attribute_master import AttributeMaster
        self.attribute_master: ma.MasterDict[int, AttributeMaster] = self._load_master(AttributeMaster)
        from d4dj_utils.master.card_exp_master import CardExpMaster
        self.card_exp_master: ma.MasterDict[int, CardExpMaster] = self._load_master(CardExpMaster)
        from d4dj_utils.master.card_master import CardMaster
        self.card_master: ma.MasterDict[int, CardMaster] = self._load_master(CardMaster)
        from d4dj_utils.master.character_master import CharacterMaster
        self.character_master: ma.MasterDict[int, CharacterMaster] = self._load_master(CharacterMaster)
        from d4dj_utils.master.chart_designer_master import ChartDesignerMaster
        self.chart_designer_master: ma.MasterDict[int, ChartDesignerMaster] = self._load_master(ChartDesignerMaster)
        from d4dj_utils.master.chart_master import ChartMaster
        self.chart_master: ma.MasterDict[int, ChartMaster] = self._load_master(ChartMaster)
        from d4dj_utils.master.chart_note_count_master import ChartNoteCountMaster
        self.chart_note_count_master: ma.MasterDict[Tuple[int, int], ChartNoteCountMaster] = self._load_master(
            ChartNoteCountMaster)
        from d4dj_utils.master.command_master import CommandMaster
        self.command_master: ma.MasterDict[int, CommandMaster] = self._load_master(CommandMaster)
        from d4dj_utils.master.condition_master import ConditionMaster
        self.condition_master: ma.MasterDict[int, ConditionMaster] = self._load_master(ConditionMaster)
        from d4dj_utils.master.event_master import EventMaster
        self.event_master: ma.MasterDict[int, EventMaster] = self._load_master(EventMaster)
        from d4dj_utils.master.event_specific_bonus_master import EventSpecificBonusMaster
        self.event_specific_bonus_master: ma.MasterDict[int, EventSpecificBonusMaster] = self._load_master(
            EventSpecificBonusMaster)
        from d4dj_utils.master.exchange_item_master import ExchangeItemMaster
        self.exchange_item_master: ma.MasterDict[int, ExchangeItemMaster] = self._load_master(ExchangeItemMaster)
        from d4dj_utils.master.exchange_master import ExchangeMaster
        self.exchange_master: ma.MasterDict[int, ExchangeMaster] = self._load_master(ExchangeMaster)
        from d4dj_utils.master.mission_group_master import MissionGroupMaster
        self.mission_group_master: ma.MasterDict[int, MissionGroupMaster] = self._load_master(MissionGroupMaster)
        from d4dj_utils.master.mission_detail_master import MissionDetailMaster
        self.mission_detail_master: ma.MasterDict[int, MissionDetailMaster] = self._load_master(MissionDetailMaster)
        from d4dj_utils.master.mission_panel_master import MissionPanelMaster
        self.mission_panel_master: ma.MasterDict[int, MissionPanelMaster] = self._load_master(MissionPanelMaster)
        from d4dj_utils.master.music_master import MusicMaster
        self.music_master: ma.MasterDict[int, MusicMaster] = self._load_master(MusicMaster)
        from d4dj_utils.master.music_mix_master import MusicMixMaster
        self.music_mix_master: ma.MasterDict[Tuple[int, int], MusicMixMaster] = self._load_master(MusicMixMaster)
        from d4dj_utils.master.rarity_master import RarityMaster
        self.rarity_master: ma.MasterDict[int, RarityMaster] = self._load_master(RarityMaster)
        from d4dj_utils.master.reward_master import RewardMaster
        self.reward_master: ma.MasterDict[int, RewardMaster] = self._load_master(RewardMaster)
        from d4dj_utils.master.skill_master import SkillMaster
        self.skill_master: ma.MasterDict[int, SkillMaster] = self._load_master(SkillMaster)
        from d4dj_utils.master.stock_master import StockMaster
        self.stock_master: ma.MasterDict[int, StockMaster] = self._load_master(StockMaster)
        from d4dj_utils.master.stock_view_category_master import StockViewCategoryMaster
        self.stock_view_category_master: ma.MasterDict[int, StockViewCategoryMaster] = self._load_master(
            StockViewCategoryMaster)
        from d4dj_utils.master.unit_master import UnitMaster
        self.unit_master: ma.MasterDict[int, UnitMaster] = self._load_master(UnitMaster)
        master_paths = set(sorted(path for path in self.get_master_paths()))
        loaded_master_paths = {master.path for master in self.masters.values()}
        for path in sorted(master_paths.difference(loaded_master_paths)):
            self.logger.debug(f'Unknown master file not loaded "{path}".')

    def __getitem__(self, item):
        return self.masters.__getitem__(item)

    def save_masters(self, encrypt=True):
        for value in self.masters.values():
            value.save(encrypt)

    def get_master_paths(self):
        return (self.path / 'Master').glob('*Master.msgpack')

    def _load_master(self, cls: Type) -> ma.MasterDict:
        name = cls.__name__
        asset_path = self.path / f'Master/{name}.msgpack'
        with asset_path.open('rb') as f:
            data = msgpack.load(f, strict_map_key=False, use_list=False)
        master_dict = ma.MasterDict({k: cls(self, *v) for k, v in data.items()}, name, asset_path)
        self.masters[name] = master_dict
        return master_dict

    def formatted_masters(self):
        return '\n\n'.join((f'{k}:\n' + textwrap.indent(v.formatted(), '    ') for k, v in self.masters.items()))

    def dump_formatted_masters(self):
        for master in self.masters.values():
            with master.path.with_suffix('.txt').open('w', encoding='utf-8') as f:
                f.write(master.formatted())
                self.logger.info(f'Dumped master {master.name}')

    def render_charts_by_master(self):
        """
        Renders charts based on values within charts master.
        This includes mix data but may miss some chart files that have been released without being added to masters.
        """
        for chart_mas in self.chart_master.values():
            chart = chart_mas.load_chart_data()
            image_path = chart_mas.image_path
            mix_path = chart_mas.mix_path
            mix_sections = chart_mas.load_sections()
            if image_path.exists() and (mix_path.exists() or not mix_sections):
                self.logger.debug(f'Chart already processed at "{image_path}".')
                continue
            chart.render().save(image_path)
            self.logger.info(f'Chart rendered at "{image_path}".')
            if mix_sections:
                chart_mas.render_sections(mix_sections).save(mix_path)
                self.logger.info(f'Mix rendered at "{mix_path}".')

    def render_charts_by_file(self):
        charts_path = self.path / 'ondemand' / 'chart'
        for path in charts_path.glob('chart_*[1-4]'):
            out_path = path.with_suffix('.png')
            if out_path.exists():
                self.logger.debug(f'Chart already processed at "{path}".')
                continue
            with path.open('rb') as f:
                chart = load_chart(f)
            chart.render().save(out_path)
            self.logger.info(f'Chart rendered at "{path}".')
