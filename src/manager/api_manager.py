from ..api.modrinth_api import ModrinthAPI
from ..api.curseforge_api import CurseForgeAPI
from ..api.high_level_api import HighLevelAPI

from fuzzywuzzy import process, fuzz
from pprint import pprint

# modules
from .. import utils
from .. import config

from ..types import formats
from ..types import constants

class ApiManager:
    def __init__(self):
        self.m_api = HighLevelAPI(ModrinthAPI())
        self.c_api = HighLevelAPI(CurseForgeAPI())
        
    def search_mod(self, name, versions=None, loader=None, count=5):
        # search modrinth and curseforge
        
        ## process modrinth restults
        modrinth_search = self.m_api.search_mod(name, versions, loader)

        modrinth = []
        if modrinth_search is not None:
            modrinth_titles = [item["title"] for item in modrinth_search]
            print("modrinth_titles: ", modrinth_titles)
            
            indices, scores = utils.best_match(name, modrinth_titles, count)
            print("MODRINTH index: ", indices, scores)
            modrinth_best_search = [modrinth_search[index] for index in indices]

            modrinth_ids = [item["project_id"] for item in modrinth_best_search]
            modrinth_projects = self.m_api.get_projects(modrinth_ids)

            for project in modrinth_projects:
                mod = formats.extract_modrinth_data(project)
                modrinth.append(mod.to_dict())
                

            print("best modrinth projects: ", [modrinth_titles[i] for i in indices])

        else:
            print("No modrinth results found")

        ## TODO: process curseforge results
        #curseforge = c_api.search_mod(name, versions, loader)
        curseforge_search = self.c_api.search_mod(name)
        
        curseforge = []
        if curseforge_search is not None:
            curseforge_titles = [item["name"] for item in curseforge_search]
            print("curseforge_titles: ", curseforge_titles)
            
            indices, scores = utils.best_match(name, curseforge_titles, count)
            print("CURSEFORGE index: ", indices, scores)
            curseforge_best_search = [curseforge_search[index] for index in indices]

            curseforge_ids = [item["id"] for item in curseforge_best_search]
            curseforge_projects = self.c_api.get_projects(curseforge_ids)

            pprint(curseforge_projects)

            print("best curseforge projects: ", [curseforge_titles[i] for i in indices])

            for project in curseforge_projects:
                mod = formats.extract_curseforge_data(project)
                curseforge.append(mod.to_dict())

        # TODO:  find the best result from both

        # return the best result
        return curseforge