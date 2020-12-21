import json
from .tft_api_class import UnitDto
from .misc import dict_add_count

class Item:
    def __init__(self, id: int):
        # Get item info
        with open('./data/items.json', 'r') as f:
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
