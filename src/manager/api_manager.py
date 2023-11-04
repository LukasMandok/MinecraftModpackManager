import numpy as np

# modules
from ..api.modrinth_api import ModrinthAPI
from ..api.curseforge_api import CurseForgeAPI
from ..api.high_level_api import HighLevelAPI

from .. import utils
from .. import config

from ..models import formats
from ..models.constants import *

class ApiManager:
    def __init__(self):
        # Old approach with redirecting all missing requests to the api (not transparant enough)
        # If you want to go back to this, include def __getattr__ in HighLevelAPI and remove multiple inheritance from ModrinthAPI and CurseForgeAPI
        self.m_api = HighLevelAPI(ModrinthAPI())
        self.c_api = HighLevelAPI(CurseForgeAPI())
        
        # New approach using multiple inheritance and passing instance of child object (modrinth and curseforge api) to HighLevelAPI
        # self.m_api = ModrinthAPI()
        # self.c_api = CurseForgeAPI()
    
        
    def retrieve_mod(self, name, versions = None, mod_loaders = None):
        mod_m, score_m = self.m_api.find_best_matching_mod(name)
        mod_c, score_c = self.c_api.find_best_matching_mod(name)
        
        mods = [mod_m, mod_c]
        scores = np.array([score_m, score_c])
        print("scores: ", scores)
        
        # Use source with perfect match
        use_source = (scores == 1000)
        
        if not any(scores > 80):
            print("Could not find any mod")
            return None
        
        if not any(use_source):
            # get index of largest element in list
            use_source[np.argmax(scores)] = True
        
        print("Using source: ", use_source)
        
        
        score_diff = abs(score_m - score_c)
        print("score diff: ", score_diff)
        
        comparison_score = utils.match_mods(mod_m, mod_c)
        
        return comparison_score
        
            
    def get_mod_search_results(self, name, versions=None, loader=None, count=5, source = Sources.UNKNOWN):
        # search modrinth and curseforge
        
        results = None
        if source == Sources.MODRINTH:
            print("Searching in modrinth")
            results, scores = self.m_api.get_best_mods_search(name, versions, loader, count)  
            return results
        
        elif source == Sources.CURSEFORGE:
            print("Searching in curseforge")
            results, scores = self.c_api.get_best_mods_search(name, versions, loader, count)
            return results
        
        else:
            print("Searching in both")
            # TODO: combine both results
            results, scores = self.m_api.get_best_mods_search(name, versions, loader, count)  
            return results        