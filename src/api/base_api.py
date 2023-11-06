from abc import ABC, abstractmethod

import requests
import json

from ..models.formats import GameVersion

class BaseAPI(ABC):
    def __init__(self, api_url, download_url, headers):
        self.api_url = api_url
        self.download_url = download_url
        self.headers = headers
        
    ### General access

    def request(self, sub_url, params = None, data = None, debug = False, custom_url = None):
        url = (self.api_url if not custom_url else custom_url) + sub_url

        if data is None:
            if debug: print("GET request: ", url, "\n\tParams: ", params)
            response = requests.get(url, params = params, headers = self.headers)
        else:
            if debug: print("POST request: ", url, "\n\tParams: ", params, "\n\tData: ", data)
            response = requests.post(url, params = params, data = json.dumps(data, default=str), headers = self.headers)

        if debug: print("\tResponse: ", response.json())

        if response.status_code == 200:
            return response.json()
        else:
            return response.raise_for_status()
        
    
    # ### Declare Child Class specific variables
    
    @property 
    @abstractmethod
    def name_tag(self): pass
    
    @property
    @abstractmethod
    def id_tag(self): pass
    
    @property
    @abstractmethod
    def search_id_tag(self): pass
    
        
    ### basic api requests
    
    @abstractmethod
    def get_project(self, id, debug = False):
        pass
    
    @abstractmethod
    def get_projects(self, ids, debug = False):
        pass
    
    @abstractmethod
    def get_project_versions(self, ids, debug = False):
        pass
    
    @abstractmethod
    def search_project(self, params, debug = False):
        pass
    
    ### a bit more high level
    
    @abstractmethod
    def get_mod_search_results(self, name, version = None, modloader = None, count = 20, debug = False):
        pass
    
    
    ### retrieve Mod Data
    
    @abstractmethod
    def add_missing_project_info(self, project):
        pass


    # use the data from project_info saved in mod to fill in version data
    @abstractmethod
    def decode_version_info(self, version_info):
        pass
    
    # Complete Project/Mod Information    
    def get_version_info(self, project_id):
        
        project_version_info = self.get_project_versions(project_id)
        
        if not project_version_info:
            print("No version data found for project:", project_id)
            return None
        
        version_data      = {}
        game_version_data = {}
        loader_data       = {}
        
        for version_info in project_version_info:
            version_id, version_num, version_date, dependencies, file_url, game_versions, loaders = self.decode_version_info(version_info)
            
            # write version into dict:
            version_data[version_id] = {
                "version_number" : version_num,
                "version_date"   : version_date,
                "dependencies"   : dependencies,
                "file_url"       : file_url,
                "game_versions"  : game_versions,
                "loaders"        : loaders,
            }
            
            # TODO: put this into a commun function in base_api
            
            # if project has loader information:
            if loaders:
                # write game version dict
                for game_version in game_versions:
                        game_version_data.setdefault(game_version, {})
                        for loader in loaders:
                            game_version_data[game_version].setdefault(loader, []).append(version_id)
                    
                # write loader dict
                for loader in loaders:
                    loader_data.setdefault(loader, {})
                    # TODO: in the case it was previously thought, that there is not mod-loader and it was initialized with a list
                    for game_version in game_versions:
                        loader_data[loader].setdefault(game_version, []).append(version_id)
            
            # if project has no loader information    
            elif not game_version_data[game_version]:
                for game_version in game_versions:
                    game_version_data.setdefault(game_version, []).append(version_id)
                
            else:
                print("version:", version_id, "is missing loader")
        #print("modrinth_api - get_version_info - version_data:", version_data)
        return version_data, game_version_data, loader_data
        
    
    @staticmethod
    @abstractmethod
    def extract_data(data):
        pass
        
        

        
