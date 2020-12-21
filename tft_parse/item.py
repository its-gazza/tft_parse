import json
import pkg_resources
from pathlib import Path
from .tft_api_class import UnitDto
from .misc import dict_add_count
from . import current_tft_set

class Item:
    def __init__(self, id: int, tft_set_number: int=current_tft_set):
        # Get item info
        items_json = Path(pkg_resources.resource_filename('tft_parse', f'data/{tft_set_number}/items.json'))
        with open(items_json, 'r') as f:
            items = json.loads(f.read())
        item = [item for item in items if item.get('id') == id]
        if len(item) == 0:
            raise ValueError(f"{id} does not exist")
        else:
            self.item = id
        # Setup values
        self.name = item[0]['name']
        self.description = item[0]['description']
        self.champion = {}
        self.item_other = {}
        self.item_combination = {}

    def from_dict(self, data: dict) -> None:
        self.champion = data['champion']
        self.item_combination = data['item_combination']

    def to_dict(self):
        output = {
            'item': self.item,
            'name': self.name,
            'description': self.description,
            'champion': self.champion,
            'item_combination': self.item_combination,
            'item_other': self.item_other,
        }

        return output

    def parse_unit(self, unit: UnitDto):
        # ==== Additional items ==== #
        # Since we're looking at additional items, we will remove the item itself
        # to reduce duplication
        items = unit.items
        items.remove(self.item)
        # Item combinations
        self.item_combination = dict_add_count(self.item_combination, str(items))
        # Item other
        for item in items:
            self.item_other = dict_add_count(self.item_other, item)

        # ==== Champion ==== #
        self.champion = dict_add_count(self.champion, unit.character_id)
