import json
import unittest
import tft_parse


class TestChampion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('tests/data/champion.json', 'r') as f:
            cls.data = json.load(f)

    def setUp(self):
        self.champion = tft_parse.Champion(self.data['character_id'], 4)

    def test_parse_from_new(self):
        """New unit and parse three data"""
        # ==== First parse ==== #
        self.champion.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        # Item
        self.assertEqual(self.champion.item, {23: 1, 11: 1})
        self.assertEqual(self.champion.item_1, {23: 1, 11: 1})
        # Combination
        self.assertEqual(self.champion.item_comb, {'[11, 23]': 1})
        self.assertEqual(self.champion.item_comb_1, {'[11, 23]': 1})
        # Occurance
        self.assertEqual(self.champion.champion_occurrence, 1)
        self.assertEqual(self.champion.tier, {1: 1})
        # Chosen
        self.assertEqual(self.champion.chosen, {})

        # ==== Second parse ==== #
        self.champion.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        # Item
        self.assertEqual(self.champion.item, {11: 1, 22: 1, 23: 2, 79: 1})
        self.assertEqual(self.champion.item_3, {22: 1, 23: 1, 79: 1})
        # Combination
        self.assertEqual(self.champion.item_comb, {'[11, 23]': 1, '[22, 23, 79]': 1})
        self.assertEqual(self.champion.item_comb_3, {'[22, 23, 79]': 1})
        # Occurance
        self.assertEqual(self.champion.champion_occurrence, 2)
        self.assertEqual(self.champion.tier, {1: 1, 3: 1})
        # Chosen
        self.assertEqual(self.champion.chosen, {'Set4_Shade': 1})

        # ==== Third parse ==== #
        # Reuse data fdrom 2nd parse
        self.champion.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        # Item
        self.assertEqual(self.champion.item, {11: 1, 22: 2, 23: 3, 79: 2})
        self.assertEqual(self.champion.item_3, {22: 2, 23: 2, 79: 2})
        # Combination
        self.assertEqual(self.champion.item_comb, {'[11, 23]': 1, '[22, 23, 79]': 2})
        self.assertEqual(self.champion.item_comb_3, {'[22, 23, 79]': 2})
        # Occurance
        self.assertEqual(self.champion.champion_occurrence, 3)
        self.assertEqual(self.champion.tier, {1: 1, 3: 2})
        # Chosen
        self.assertEqual(self.champion.chosen, {'Set4_Shade': 2})

    def test_parse_from_existing(self):
        """Existing unit and parse new data

        This test will assume test_parse_from_new works correctly
        """
        # ==== Create dummy to_dict() ==== #
        # Note below parse is the same as test_parse_from_new
        # Parse units
        self.champion.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        self.champion.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        self.champion.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        # Output
        output_dict = self.champion.to_dict()
        # Sanity check for to_dict()
        self.assertEqual(output_dict['championId'], self.data['units'][0]['character_id'])
        self.assertEqual(self.champion.item_comb, {'[11, 23]': 1, '[22, 23, 79]': 2})
        self.assertEqual(self.champion.champion_occurrence, 3)

        # ==== Parse from generated output ==== #
        champion = tft_parse.Champion(self.data['character_id'], 4)
        champion.from_dict(output_dict)
        # Check if info is parsed correctly
        self.assertEqual(champion.to_dict(), self.champion.to_dict())

        # ==== Parse unit ==== #
        champion.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        # Item
        self.assertEqual(champion.item, {11: 2, 22: 2, 23: 4, 79: 2})
        self.assertEqual(champion.item_1, {23: 2, 11: 2})
        # Combination
        self.assertEqual(champion.item_comb, {'[11, 23]': 2, '[22, 23, 79]': 2})
        self.assertEqual(champion.item_comb_1, {'[11, 23]': 2})
        # Occurance
        self.assertEqual(champion.champion_occurrence, 4)
        self.assertEqual(champion.tier, {1: 2, 3: 2})
        # Chosen
        self.assertEqual(champion.chosen, {'Set4_Shade': 2})
