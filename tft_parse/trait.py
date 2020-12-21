import json
import pkg_resources
from pathlib import Path
from . import current_tft_set


class Traits:
    def __init__(self, tft_set_number: int = current_tft_set):
        # Get data path
        data_path = Path(pkg_resources.resource_filename('tft_parse', f'data/{tft_set_number}'))
        # Open trait files
        with open(data_path.joinpath('traits.json')) as f:
            self.data = json.load(f)
        self.style_map = {0: 'none', 1: 'bronze', 2: 'silver', 3: 'gold', 4: 'chromatic'}
        # Loop each trait and append to class
        for trait_info in self.data:
            self.__setattr__(trait_info['key'], Trait(trait_info))

    def get_trait_style(self, trait: str, style: int):
        """Return trait style as one str (e.g. Cultist3)"""
        trait_info = self.__getattribute__(trait)
        return trait_info.get_trait_style(style)


class Trait:
    def __init__(self, data: dict):
        self.key = data['key']
        self.name = data["name"]
        self.description = data["description"]
        self.type = data["type"]
        for trait_set in data['sets']:
            self.__setattr__(trait_set['style'], trait_set)

    def get_trait_style(self, style: int):
        """Return str like Cultist"""
        if style == 0:
            return None
        style_map = {0: 'none', 1: 'bronze', 2: 'silver', 3: 'gold', 4: 'chromatic'}
        style_name = style_map[style]
        style_min = self.__getattribute__(style_name)['min']

        return f'{self.key}_{style_min}'
