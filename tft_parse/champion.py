import json
import pkg_resources
from pathlib import Path
from .tft_api_class import UnitDto
from .misc import dict_add_count
from . import current_tft_set


class Champion:
    def __init__(self, championId, tft_set_number: int = current_tft_set):
        champion_json = Path(pkg_resources.resource_filename('tft_parse', f'data/{tft_set_number}/champions.json'))
        with open(champion_json) as f:
            champions = json.load(f)
        # Get champion data
        champion = [champion for champion in champions if champion.get('championId') == championId]
        # Sanity check: champion
        if len(champion) == 0:
            raise ValueError(f"{championId} does not exist")
        else:
            self.champion = champion[0]
        # Champion data
        self.championId = self.champion['championId']
        self.name = self.champion['name']
        self.cost = self.champion['cost']
        self.traits = self.champion['traits']
        # ==== Initialise values ==== #
        self.champion_occurrence = 0
        self.tier = {}
        # Items
        self.item = {}  # Log item use
        self.item_1 = {}  # Log item use at 1 tier
        self.item_2 = {}  # Log item use at 2 tier
        self.item_3 = {}  # Log item use at 3 tier
        self.item_comb = {}  # Log item combaination
        self.item_comb_1 = {}  # Log item combination at 1 tier
        self.item_comb_2 = {}  # Log item combination at 2 tier
        self.item_comb_3 = {}  # Log item combination at 3 tier
        # Chosen
        self.chosen = {}

    def from_dict(self, data: dict) -> None:
        """Parse data from previous data"""
        # Occurance
        self.champion_occurrence = data['champion_occurrence']
        self.tier = data['tier']
        # Item
        self.item = data['item']
        self.item_1 = data['item_1']
        self.item_2 = data['item_2']
        self.item_3 = data['item_3']
        # Item combinations
        self.item_comb = data['item_comb']
        self.item_comb_1 = data['item_comb_1']
        self.item_comb_2 = data['item_comb_2']
        self.item_comb_3 = data['item_comb_3']
        # Chosen
        self.chosen = data['chosen']

    def to_dict(self):
        """Convert to dict

        Return:
            Dictionary containing class info.
        """
        output = {
            'champion': self.champion,
            'championId': self.championId,
            'name': self.name,
            'cost': self.cost,
            'traits': self.traits,
            'champion_occurrence': self.champion_occurrence,
            'item': self.item,
            'item_1': self.item_1,
            'item_2': self.item_2,
            'item_3': self.item_3,
            'item_comb': self.item_comb,
            'item_comb_1': self.item_comb_1,
            'item_comb_2': self.item_comb_2,
            'item_comb_3': self.item_comb_3,
            'chosen': self.chosen,
            'tier': self.tier
        }

        return output

    def parse_unit(self, unit: UnitDto):
        """Parse UnitDto"""
        if unit.character_id != self.championId:
            raise ValueError(f"{unit.character_id} is not the same as {self.championId}")
        # ==== Item ==== #
        # Get tier level item
        item_indv_tier = self.__getattribute__(f"item_{unit.tier}")
        item_comb_tier = self.__getattribute__(f"item_comb_{unit.tier}")

        # Add item to dict
        # Inidividual items
        for item in unit.items:
            self.item = dict_add_count(self.item, item)  # champion level
            item_indv_tier = dict_add_count(item_indv_tier, item)  # tier level
        # Write tier level back to class
        self.__setattr__(f"item_{unit.tier}", item_indv_tier)

        # Item combinations
        self.item_comb = dict_add_count(self.item_comb, str(unit.items))  # champion level
        self.__setattr__(f"item_{unit.tier}_comb", dict_add_count(item_comb_tier, str(unit.items)))  # tier level

        # ==== Chosen ==== #
        # If unit chosen add to dict
        if unit.chosen != "":
            self.chosen = dict_add_count(self.chosen, unit.chosen)

        # ==== Occurance ==== #
        self.champion_occurrence += 1
        self.tier = dict_add_count(self.tier, unit.tier)
