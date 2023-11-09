from .. import utils
from ..models.mod_info import SourceProjectInfo, ModInfoList

from pprint import pprint

class HighLevelAPI():
    def __init__(self, api):
        self.api = api
    
    # redirect all requests, that are not implemented in this class to the api
    def __getattr__(self, method):
        print("redirecting to api: ", method)
        return getattr(self.api, method)
    
    
    ### 
    def retrieve_versions(self, project_info: SourceProjectInfo):
        #pprint("high_level_api - retrieve_versions - project_info: ")
        id = project_info.id
        
        print("high_level_api - retrieve_versions - id: ", id)
        
        version_data, game_version_data, loader_data = self.api.get_version_info(id)
        
        
        project_info.add_version_dict(version_data)
        project_info.add_game_version_dict(game_version_data)
        
        # check if loader_data is not an empty dictionary:
        if loader_data:        
            project_info.add_loader_dict(loader_data)
        
        print("adding game versions:")
        pprint(project_info.game_version_dict)
        
        print("adding loaders:")
        pprint(project_info.loader_dict)
            
        # pprint("high_level_api - retrieve_versions - version_data: ")
        # pprint(version_data)
        # pprint("high_level_api - retrieve_versions - game_version_data: ")
        # pprint(game_version_data)
        # pprint("high_level_api - retrieve_versions - loader_data: ")
        # pprint(loader_data)

        
    ### Specific access
    def get_best_results_by_score(self, search_results : list[str], name : str, count : int = 5):
        # get the titles of the results
        titles = [item[self.api.name_tag] for item in search_results]

        # get the best matches
        indices, scores = utils.best_match(name, titles, count)
        #print("- indices : ", indices, "\n- scores : ", scores)
        
        # get list with best results from indices
        best_search = [search_results[index] for index in indices]
        
        print("best projects: ", [titles[i] for i in indices])
        
        return best_search, scores, titles, indices
    
    
    def retrieve_project_details(self, search_results):
        # get project ids from search results
        ids = [item[self.search_id_tag] for item in search_results]
        
        # make api request to retrieve mod details
        projects_info = self.api.get_projects(ids)
        
        # sort projects, if retrieved in wrong order
        ids_unsorted = [project[self.id_tag] for project in projects_info]
        sorted_projects_info = projects_info
        if ids != ids_unsorted:
            #print("projects in worng order - sorting ...")
            sorting = [ids_unsorted.index(id) for id in ids]
            sorted_projects_info = [projects_info[index] for index in sorting]
        
        return sorted_projects_info
    
    
    def convert_projects_to_mods(self, projects_info: SourceProjectInfo):
        mod_info_list = ModInfoList()
        for project_info in projects_info:
            # use api's extraction function to convert project to mod format
            full_project_info = self.api.add_missing_project_info(project_info)
            mod_info = self.api.extract_data(full_project_info)
            
            mod_info.add_api(self)
            
            # NOTE: add_version_data can be called here, maybe
            
            mod_info_list.append(mod_info)
            
        return mod_info_list
    
    
    ### USE API TO retrieve Search Results
    
    # find #count best matching mods for given name
    def get_best_mods_search(self, name, versions, loader, count = 5):
        search_results = self.api.get_mod_search_results(name, versions, loader)
        
        if search_results is None:
            print("No results found")
            return None, None
        
        best_search, scores, *_ = self.get_best_results_by_score(search_results, name, count)
        
        best_projects = self.retrieve_project_details(best_search)
        
        mod_info_list = self.convert_projects_to_mods(best_projects)
            
        return mod_info_list, scores
    
    # find best matching mod for given name
    def find_best_matching_mod(self, name):
        mod_info_list, score_list = self.get_best_mods_search(name, versions=None, loader=None, count = 1)
        
        mod_info = None
        score = None
        if mod_info_list is not None and len(mod_info_list) > 0:
            mod_info = mod_info_list[0]
            score = score_list[0]
            
        return mod_info, score