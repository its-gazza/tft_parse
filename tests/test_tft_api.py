import tft_parse
import datetime
import unittest
import json


class TestMatch(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open('tests/data/tft_api/match.json', 'r') as f:
            self.data = json.load(f)
        self.match = tft_parse.MatchDto(self.data)

    def test_parse(self):
        """Test parse info is correct"""
        self.assertIs(type(self.match), tft_parse.MatchDto)
        self.assertEqual(self.match.data, self.data)

    def test_to_dict(self):
        """Test to_dict()"""
        output = self.match.to_dict()
        self.assertEqual(self.match.metadata.region, output['region'])
        self.assertEqual(self.match.info.patch, output['patch'])
        self.assertEqual(self.match.info.queue, output['queue'])


class TestMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open('tests/data/tft_api/metadata.json', 'r') as f:
            data = json.load(f)['metadata']
        self.metadata = tft_parse.MetadataDto(data)

    def test_parse(self):
        """Test parse info is correct"""
        self.assertIs(type(self.metadata), tft_parse.MetadataDto)

    def test_get_region(self):
        """Test get_region()"""
        self.assertEqual(self.metadata.get_region(), 'OC1')

    def test_route_region(self):
        """Test route_region()"""
        self.assertEqual(self.metadata.get_route_region(), 'AMERICAS')


class TestInfo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open('tests/data/tft_api/info.json', 'r') as f:
            data = json.load(f)['info']
        self.info = tft_parse.InfoDto(data)

    def test_parse(self):
        """Test parse info is correct"""
        self.assertIs(type(self.info), tft_parse.InfoDto)

    def test_get_patch(self):
        """Test get_patch()"""
        self.assertEqual(self.info.get_patch(), '10.20')

    def test_get_queue(self):
        """Test get_queue()"""
        self.assertEqual(self.info.get_queue(), 'Rank')

    def test_get_game_date(self):
        """Test get_game_date()"""
        self.assertIs(type(self.info.get_game_date()), datetime.datetime)

    def test_eliminations_norm(self):
        """Test eliminations (Normal)"""
        elim = self.info.eliminations()
        # Test type
        self.assertIs(type(elim), dict)
        # Each elim time must be less than game_lenght
        for k, v in elim.items():
            self.assertLessEqual(v, self.info.game_length)

    def test_eliminations_pct(self):
        """Test eliminations (Percentage)"""
        elim = self.info.eliminations(pct=True)
        # Test type
        self.assertIs(type(elim), dict)
        # Each elim time must be less than game_lenght
        for k, v in elim.items():
            self.assertLessEqual(v, 1)

    def test_palcements(self):
        """Test placements()"""
        placement = [k for k, v in self.info.placements().items()]
        expected = set([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(set(placement), set(expected))

    def test_players_units(self):
        """Test players_units()"""
        players_units = self.info.players_units()
        for player_units in players_units:
            self.assertIs(type(player_units), tft_parse.UnitDto)

    def test_players_traits(self):
        """Test players_traits()"""
        players_traits = self.info.players_traits()
        for player_traits in players_traits:
            self.assertIs(type(player_traits), str)


class TestParticipant(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open('tests/data/tft_api/participant.json', 'r') as f:
            data = json.load(f)
        self.participants = tft_parse.ParticipantDto(data)

    def test_parse(self):
        """Test parse info is correct"""
        self.assertIs(type(self.participants), tft_parse.ParticipantDto)
        # Check traits
        for i in self.participants.traits:
            self.assertIs(type(i), tft_parse.TraitDto)
        # Check units
        for i in self.participants.units:
            self.assertIs(type(i), tft_parse.UnitDto)


class TestTrait(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        with open('tests/data/tft_api/trait.json', 'r') as f:
            data = json.load(f)
        self.trait = tft_parse.TraitDto(data)

    def test_parse(self):
        """Test parse info is correct"""
        self.assertIs(type(self.trait), tft_parse.TraitDto)

    def test_trait_tier(self):
        """Test trait tier"""
        self.assertIs(type(self.trait.tier_name), str)
        self.assertEqual(self.trait.tier_name, 'Cultist_6')


class TestUnit(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Non-chosen
        with open('tests/data/tft_api/unit.json', 'r') as f:
            data = json.load(f)
        self.unit = tft_parse.UnitDto(data)
        # Chosen
        with open('tests/data/tft_api/unit_chosen.json', 'r') as f:
            data = json.load(f)
        self.unit_chosen = tft_parse.UnitDto(data)

    def test_parse(self):
        """Test parse info is correct"""
        self.assertIs(type(self.unit), tft_parse.UnitDto)
        self.assertIs(type(self.unit_chosen), tft_parse.UnitDto)
        # Chosen name
        self.assertEqual(self.unit.chosen, "")
        self.assertEqual(self.unit_chosen.chosen, "Cultist")

    def test_is_chosen(self):
        """Test is_chosen()"""
        self.assertFalse(self.unit.is_chosen())
        self.assertTrue(self.unit_chosen.is_chosen())


if __name__ == "__main__":
    unittest.main()
