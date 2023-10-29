from ..api import modrinth_api as m_api
from ..api import curseforge_api as c_api

from fuzzywuzzy import process, fuzz
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
        modrinth = []
        if modrinth_search is not None:
            modrinth_titles = [hit["title"] for hit in modrinth_search["hits"]]
            print("modrinth_titles: ", modrinth_titles)
            
            indices, scores = utils.best_match(name, modrinth_titles, count)
            print("MODRINTH index: ", indices, scores)
            modrinth_best_search = [modrinth_search["hits"][index] for index in indices]

            modrinth = [hit["project_id"] for hit in modrinth_best_search]
        else:
            print("No modrinth results found")

        ## TODO: process curseforge results
        #curseforge = c_api.search_mod(name, versions, loader)
        



        # TODO:  find the best result from both

        # return the best result
        return modrinth