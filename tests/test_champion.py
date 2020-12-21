import json
import unittest
import tft_parse


class TestChampion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('tests/data/champion.json', 'r') as f:
            cls.data = json.load(f)

        cls.champion = tft_parse.Champion(cls.data['character_id'])