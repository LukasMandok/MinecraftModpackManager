import json
import os

from ..config import config

# Create a Class for the DataManager that contains the functinos above:
class DataManager:
    def __init__(self, fileManager, downloadManager):
        self.data = None
        self.fileManager = fileManager
        self.downloadManager = downloadManager
        
        self.download_list_file_list = {}
        self.download_list_file_dict = {}
        
        self.download_list_folder_list = {}
        self.download_list_folder_dict = {}


    ### private functions
    
    def _add_mod_to_list(self, mod_list, name, categories, comment = None):
        mod_list[name] = {"categories"   : categories.copy(),
                            "comment"      : comment}
        
    def _add_mod_to_dict(self, mod_dict, name, categories, comment = None):
        current_dict = mod_dict
        #categories = categories or [None]
        for category in categories:
            current_dict = current_dict.setdefault("category", {})
            current_dict = current_dict.setdefault(category, {})
        current_dict = current_dict.setdefault("mods", [])
        current_dict.append({"name" : name, "comment" : comment})


    def _load_download_list_from_file(self):
        for mod_info in self.fileManager.load_download_list():
            print("adding:", mod_info)
            self._add_mod_to_list(self.download_list_file_list, *mod_info)
            self._add_mod_to_dict(self.download_list_file_dict, *mod_info)
        
    def _load_download_list_from_folder(self):
        for mod_info in self.downloadManager.load_download_list():
            self._add_mod_to_list(self.download_list_folder_list, *mod_info)
            self._add_mod_to_dict(self.download_list_folder_dict, *mod_info)
        

    ### public functions

    def get_projects(self, type):
        return self.data[type]

    def get_project(self, type, id):
        return self.get_projects(type)[id]


    def find_project(self, type, name):
        return next((project for project in self.data[type] if project['name'] == name), None)

    def add_project(self, type, project):
        id = project.getID()
        self.data[type].append()
        self._save_mod_list()

    # mod specific funtions

    def get_mods(self):
        return self.get_projects("mods")

    def get_mod(self, id):
        return self.get_project("mods", id)


    def find_mod(self, name):
        return self.find_project("mods", name)

    def add_mod(self, mod):
        self.add_project("mods", mod)
