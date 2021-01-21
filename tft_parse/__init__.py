__version__ = '0.1.0'
current_tft_set = '4.5'

from .tft_api_class import MatchDto, InfoDto, MetadataDto, UnitDto, ParticipantDto, TraitDto
from .misc import dict_add_count, route_region, regions
from .champion import Champion
from .item import Item
from .trait import Traits
