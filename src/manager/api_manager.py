import numpy as np

# modules
from ..api.modrinth_api import ModrinthAPI
from ..api.curseforge_api import CurseForgeAPI
from ..api.high_level_api import HighLevelAPI

from .. import utils
from ..config import config

from ..models.mod_info import SourceModInfo, SharedSourceModInfo
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
        
    
        
    def retrieve_mod(self, name: str):
        shared_mod_info = self.find_shared_mod(name)
        
        pass
        
    
        
    def find_shared_mod(self, name: str) -> list:
        mod_info_m, score_m = self.m_api.find_best_matching_mod(name)
        mod_info_c, score_c = self.c_api.find_best_matching_mod(name)
        
        mods_info = np.array([mod_info_m, mod_info_c])
        scores = np.array([score_m, score_c])
        # print("scores: ", scores)
        
        # Use source with perfect match
        use_source = (scores >= 100)
        
        if not any(scores > 90):
            print("Could not find any mod")
            return None
        
        #score_diff = abs(score_m - score_c)
        # print("score diff: ", score_diff)
        
        score_diff_threshold = 5
        if not any(use_source):
            # get index of largest element in list
            max_score = np.max(scores)
            use_source[max_score - scores < score_diff_threshold] = True
        
        # print("Using source: ", use_source)
    
        #comparison_score = utils.match_mods(mod_m, mod_c)
        # print("comparison score: ", comparison_score)
        
        # Add missing mod versions to the mod_info
        for mod_info in mods_info[use_source]:
            print("mod info:", mod_info)
            mod_info.api.retrieve_versions(mod_info)
        
        shared_mod_info = SharedSourceModInfo(*mods_info[use_source])
        
        return shared_mod_info
    
    
            
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