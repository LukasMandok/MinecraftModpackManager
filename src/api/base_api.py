from abc import ABC, abstractmethod

import requests
import json

class BaseAPI(ABC):
    def __init__(self, api_url, download_url, headers):
        self.api_url = api_url
        self.download_url = download_url
        self.headers = headers
        
        self.name_tag = None
        
    ### General access

    def request(self, sub_url, params = None, data = None, debug = False, custom_url = None):
        url = (self.api_url if not custom_url else custom_url) + sub_url

        if data is None:
            if debug: print("GET request: ", url, "\n\tParams: ", params)
            response = requests.get(url, params = params, headers = self.headers)
        else:
            if debug: print("POST request: ", url, "\n\tParams: ", params, "\n\tData: ", data)
            response = requests.post(url, params = params, data = json.dumps(data), headers = self.headers)

        if debug: print("\tResponse: ", response.json())

        if response.status_code == 200:
            return response.json()
        else:
            return response.raise_for_status()
        
    
    # ### Declare Child Class specific variables
    
    # @property 
    # @abstractmethod
    # def name_tag(self): pass
    
    # @property
    # @abstractmethod
    # def id_tag(self): pass
    
        
    ### Client specific access - templates:
    
    @abstractmethod
    def get_project(self, id, debug = False):
        pass
    
    @abstractmethod
    def get_projects(self, ids, debug = False):
        pass
    
    @abstractmethod
    def search_project(self, params, debug = False):
        pass
    
    @abstractmethod
    def search_mod(self, name, version = None, modloader = None, count = 20, debug = False):
        pass
        
        

        
