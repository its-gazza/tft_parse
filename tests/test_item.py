import json
import unittest
import tft_parse

class TestItem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('tests/data/item.json', 'r') as f:
            cls.data = json.load(f)

    def setUp(self):
        self.item = tft_parse.Item(11, 4)

    def test_parse_from_new(self):
        """New item and parse three data"""
        # ==== First parse ==== #
        self.item.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        # Item
        self.assertEqual(self.item.item_combination, {'[23]': 1})
        self.assertEqual(self.item.item_other, {23: 1})
        # Champion
        self.assertEqual(self.item.champion, {'TFT4_Zed': 1})

        # ==== Second parse ==== #
        self.item.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        # Item
        self.assertEqual(self.item.item_combination, {'[23]': 1, '[36, 46]': 1})
        self.assertEqual(self.item.item_other, {23: 1, 36: 1, 46: 1})
        # Champion
        self.assertEqual(self.item.champion, {'TFT4_Zed': 1, 'TFT4_XinZhao': 1})

        # ==== Third parse ==== #
        self.item.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        # Item
        self.assertEqual(self.item.item_combination, {'[23]': 2, '[36, 46]': 1})
        self.assertEqual(self.item.item_other, {23: 2, 36: 1, 46: 1})
        # Champion
        self.assertEqual(self.item.champion, {'TFT4_Zed': 2, 'TFT4_XinZhao': 1})

    def test_parse_from_existing(self):
        """Existing item and parse new data

        This test will assume test_parse_from_new works correctly
        """
        # ==== Create dummy to_dict() ==== # 
        # Note below parse is the same as test_parse_from_new
        # Parse units
        self.item.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        self.item.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        self.item.parse_unit(tft_parse.UnitDto(self.data['units'][1]))
        # Output
        output_dict = self.item.to_dict()
        # Sanity check for to_dict()
        self.assertEqual(output_dict['item'], 11)
        self.assertEqual(output_dict['item_other'], {23: 1, 36: 2, 46: 2})
        self.assertEqual(output_dict['item_combination'], {'[23]': 1, '[36, 46]': 2})

        # ==== Parse from generated output ==== #
        item = tft_parse.Item(11, 4)
        item.from_dict(output_dict)
        # Check if info is parsed correctly
        self.assertEqual(item.to_dict(), self.item.to_dict())

        # ==== Parse unit ==== #
        item.parse_unit(tft_parse.UnitDto(self.data['units'][0]))
        # Champion
        self.assertEqual(item.champion, {'TFT4_Zed': 2, 'TFT4_XinZhao': 2})
        # Item combination
        self.assertEqual(item.item_combination, {'[23]': 2, '[36, 46]': 2})
        # Item other
        self.assertEqual(item.item_other, {23: 2, 36: 2, 46: 2})
