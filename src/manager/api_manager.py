from ..api import modrinth_api as m_api
from ..api import curseforge_api as c_api

from fuzzywuzzy import process, fuzz
from pprint import pprint

# modules
from .. import utils
from .. import config

class ApiManager:
    def __init__(self):
        pass

    def search_mod(self, name, versions=None, loader=None, count=5):
        # search modrinth and curseforge
        
        ## process modrinth restults
        modrinth_search = m_api.search_mod(name, versions, loader)

        if modrinth_search is not None:
            modrinth_titles = [item["title"] for item in modrinth_search]
            print("modrinth_titles: ", modrinth_titles)
            
            indices, scores = utils.best_match(name, modrinth_titles, count)
            print("MODRINTH index: ", indices, scores)
            modrinth_best_search = [modrinth_search[index] for index in indices]

            modrinth_ids = [item["project_id"] for item in modrinth_best_search]
            modrinth_projects = m_api.get_projects(modrinth_ids)

            print("best modrinth projects: ", [modrinth_titles[i] for i in indices])

        else:
            print("No modrinth results found")

        ## TODO: process curseforge results
        #curseforge = c_api.search_mod(name, versions, loader)
        curseforge_search = c_api.search_mod(name)
            
        if curseforge_search is not None:
            curseforge_titles = [item["name"] for item in curseforge_search]
            print("curseforge_titles: ", curseforge_titles)
            
            indices, scores = utils.best_match(name, curseforge_titles, count)
            print("CURSEFORGE index: ", indices, scores)
            curseforge_best_search = [curseforge_search[index] for index in indices]

            curseforge_ids = [item["id"] for item in curseforge_best_search]
            curseforge_projects = c_api.get_projects(curseforge_ids)

            print("best curseforge projects: ", [curseforge_titles[i] for i in indices])


        # TODO:  find the best result from both

        # return the best result
        return modrinth_projects