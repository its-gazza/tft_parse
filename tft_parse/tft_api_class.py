import re
from datetime import datetime
from itertools import chain
from .misc import route_region
from .trait import Traits
from . import current_tft_set


class MatchDto:

    def __init__(self, match: dict):
        self.data = match
        self.metadata = MetadataDto(match['metadata'])
        self.info = InfoDto(match['info'])

    def to_dict(self):
        data = self.data
        # Add other data
        data['region'] = self.metadata.region
        data['patch'] = self.info.patch
        data['queue'] = self.info.queue
        data['placements'] = self.info.placements()

        return data


class MetadataDto:

    def __init__(self, data: dict):
        self.data_version = data['data_version']
        self.match_id = data['match_id']
        self.participants = data['participants']
        self.region = self.get_region()
        self.route_region = self.get_route_region()

    def get_region(self):
        """Get region from match_id"""
        region_regex = re.findall(r'(.*?)_', self.match_id)
        if len(region_regex) > 0:
            return region_regex[0]
        else:
            raise ValueError(f"Unable to regex match {self.match_id}")

    def get_route_region(self):
        """Get routing region from match_id"""
        return route_region(self.region)


class InfoDto:

    def __init__(self, data: dict):
        self.game_datetime = data['game_datetime']
        self.game_length = data['game_length']
        self.game_version = data['game_version']
        self.queue_id = data['queue_id']
        # Parse
        self.patch = self.get_patch()
        self.queue = self.get_queue()
        self.tft_set_number = self.check_set_number(data['tft_set_number'], self.patch)
        self.participants = [ParticipantDto(participant, self.tft_set_number) for participant in data['participants']]

    @staticmethod
    def check_set_number(set_number, patch):
        """Update set number to 4.5"""
        # Set number for patch 4.5 is still 4, so need to manually override
        if set_number == 4 and patch >= '11.2':
            return '4.5'
        else:
            return set_number

    def get_patch(self):
        """Get patch number"""
        patch_regex = re.findall(r'<Releases/(.*?)>', self.game_version)
        if len(patch_regex) > 0:
            return patch_regex[0]
        else:
            raise ValueError(f"Unable to regex match {self.game_version}")

    def get_queue(self):
        """Parse game's type"""
        queue_id = int(self.queue_id)
        queue_dict = {
            1090: 'Normal',
            1100: 'Rank',
            1111: 'Test',
            1110: 'Tutorial'
        }
        return queue_dict[queue_id]

    def get_game_date(self):
        """Get game's datetime"""
        # gae_datetime contains milliseconds, divide by 1000 to convert to normal seconds
        return datetime.utcfromtimestamp(int(self.game_datetime)/1000)

    def eliminations(self, pct=False):
        """Return a dict of containing all players elimination time

        Args:
            pct (bool): Return value as percentage
        """
        max_elim = 0
        output = {}
        # Loop each participants
        for participant in self.participants:
            output[participant.puuid] = participant.time_eliminated
            # For calculating percentage
            if participant.time_eliminated > max_elim:
                max_elim = participant.time_eliminated

        # Calcualte percentage
        if pct:
            output = {k: v/max_elim for k, v in output.items()}

        return output

    def placements(self):
        """Players placement"""
        output = {}
        for participant in self.participants:
            output[participant.placement] = participant.puuid

        return output

    def players_units(self):
        """Return a list of UnitDto

        Use for parsing all unit info

        """
        output = []
        # For each participants append units
        for participant in self.participants:
            output.append(participant.units)
        # Unnest list
        return list(chain.from_iterable(output))

    def players_traits(self):
        """List of player's trait"""
        output = {}
        # Get player's trait tier
        for participant in self.participants:
            part_traits = []
            for trait in participant.traits:
                if trait.trait_tier() is not None:
                    part_traits.append(trait.trait_tier())
            output[participant.puuid] = part_traits

        return output


class ParticipantDto:

    def __init__(self, data: dict, tft_set_number: int = current_tft_set):
        self.data = data
        self.companion = data['companion']
        self.gold_left = data["gold_left"]
        self.last_round = data["last_round"]
        self.level = data["level"]
        self.placement = data["placement"]
        self.players_eliminated = data["players_eliminated"]
        self.puuid = data["puuid"]
        self.time_eliminated = data["time_eliminated"]
        self.total_damage_to_players = data["total_damage_to_players"]
        self.traits = [TraitDto(trait, tft_set_number) for trait in data['traits']]
        self.units = [UnitDto(unit) for unit in data['units']]


class TraitDto:
    """TraitDto

    name:	      Trait name.
    num_units:    Number of units with this trait.
    style:        Current style for this trait. (0 = No style, 1 = Bronze, 2 = Silver, 3 = Gold, 4 = Chromatic)
    tier_current: Current active tier for the trait.
    tier_total:	  Total tiers for the trait.
    """

    def __init__(self, data: dict, tft_set_number: int = current_tft_set):
        self.name = data["name"]
        self.num_units = data["num_units"]
        self.style = data["style"]
        self.tier_current = data["tier_current"]
        self.tier_total = data["tier_total"]
        self.set_number = tft_set_number
        self.tier_name = self.trait_tier()

    def trait_tier(self):
        """Trait level"""
        return Traits(self.set_number).get_trait_style(self.name, self.style)


class UnitDto:
    """UnitDto class

    tier: star
    rarity: unit rarity
    """

    def __init__(self, data: dict):
        self.items = sorted(data['items'])
        self.character_id = data['character_id']
        self.chosen = data['chosen'] if 'chosen' in data else ""
        self.rarity = data['rarity']
        self.tier = data['tier']

    def is_chosen(self) -> bool:
        """Determine if unit is chosen"""
        # Check if info is passed
        if self.chosen is None:  # pragma: no cover
            raise ValueError("self.chosen is None")

        if self.chosen == "":
            return False
        else:
            return True
