from .base_api import BaseAPI

from .. import utils

class HighLevelAPI():
    def __init__(self, api):
        self.api = api
    
    # redirect all requests, that are not implemented in this class to the api
    # def __getattr__(self, method):
    #     return getattr(self.api, method)
        
    ### Specific access
    
    def get_search_results(self, name, versions, loader, count = 5):

        search_results = self.search_mod(name, versions, loader)
        
        results = []
        if search_results is not None:
            # get the titles of the results
            titles = [item[self.name_tag] for item in search_results]
            print("titles: ", titles)
            
            # get the best matches
            indices, scores = utils.best_match(name, titles, count)
            print("index: ", indices, scores)
            best_search = [search_results[index] for index in indices]

            ids = [item[self.id_tag] for item in best_search]
            projects = self.get_projects(ids)

            for project in projects:
                mod = formats.extract_modrinth_data(project)
                results.append(mod.to_dict())
                
            print("best projects: ", [titles[i] for i in indices])

        else:
            print("No results found")