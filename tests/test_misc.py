import unittest
import tft_parse

class TestDictAdd(unittest.TestCase):   
    def test_dict_add_count(self):
        """Test dict_add_count()
        
        Test inserting `0` once , `1` twice
        """
        output = {}
        # Add `1`
        output = tft_parse.dict_add_count(output, '1')
        self.assertEqual(output, {'1': 1})

        # Add `0`
        output = tft_parse.dict_add_count(output, '0')
        self.assertEqual(output, {'0': 1, '1': 1})

        # Add `1`
        output = tft_parse.dict_add_count(output, '1')
        self.assertEqual(output, {'0': 1, '1': 2})


class TestRouteRegions(unittest.TestCase):
    def test_route_americas(self):
        regions = ['NA1', 'BR1', 'LA1', 'LA2', 'OC1']
        for region in regions:
            with self.subTest(f"{region}"):
                self.assertEqual(tft_parse.route_region(region), 'AMERICAS')
    
    def test_route_asia(self):
        regions = ['KR', 'JP1']
        for region in regions:
            with self.subTest(f"{region}"):
                self.assertEqual(tft_parse.route_region(region), 'ASIA')

    def test_route_europe(self):
        regions = ['EUN1', 'EUW1', 'TR1', 'RU']
        for region in regions:
            with self.subTest(f"{region}"):
                self.assertEqual(tft_parse.route_region(region), 'EUROPE')

    def test_incorrect_input(self):
        with self.assertRaises(ValueError):
            tft_parse.route_region('something weired')