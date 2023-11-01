from ..api.modrinth_api import ModrinthAPI
from ..api.curseforge_api import CurseForgeAPI
from ..api.high_level_api import HighLevelAPI

from fuzzywuzzy import process, fuzz
from pprint import pprint

# modules
from .. import utils
from .. import config

from ..types import formats
from ..types.constants import *

class ApiManager:
    def __init__(self):
        # Old approach with redirecting all missing requests to the api (not transparant enough)
        # If you want to go back to this, include def __getattr__ in HighLevelAPI and remove multiple inheritance from ModrinthAPI and CurseForgeAPI
        self.m_api = HighLevelAPI(ModrinthAPI())
        self.c_api = HighLevelAPI(CurseForgeAPI())
        
        # New approach using multiple inheritance and passing instance of child object (modrinth and curseforge api) to HighLevelAPI
        # self.m_api = ModrinthAPI()
        # self.c_api = CurseForgeAPI()
        
    def search_mod(self, name, versions=None, loader=None, count=5, source = Sources.UNKNOWN):
        # search modrinth and curseforge
        
        results = None
        if source == Sources.MODRINTH:
            print("Searching in modrinth")
            results = self.m_api.get_best_mods_search(name, versions, loader, count)  
            return results
        
        elif source == Sources.CURSEFORGE:
            print("Searching in curseforge")
            results = self.c_api.get_best_mods_search(name, versions, loader, count)
            return results
        
        else:
            print("Searching in both")
            # TODO: combine both results
            results = self.m_api.get_best_mods_search(name, versions, loader, count)  
            return results        