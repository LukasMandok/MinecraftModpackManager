import json
import os

from ..config import config

from . import database_manager, download_manager
from ..models.mod_storage import DownloadList

# Create a Class for the DataManager that contains the functinos above:
class DataManager:
    def __init__(self, apiManager):   #DatabaseManager, downloadManager
        self.DatabaseManager = database_manager.DatabaseManager()
        self.downloadManager = download_manager.DownloadManager(apiManager)
        
        self.data = self.DatabaseManager() #.load_mod_list()
        
        self.downloadList_file   = DownloadList()
        self.downloadList_folder = DownloadList()
        
        self._load_download_list_from_file()
        self._load_download_list_from_folder()


    ## load download data

    def _load_download_list_from_file(self):
        for mod_info in self.DatabaseManager.load_download_list():
            self.downloadList_file.add_mod(*mod_info)
            
        
    def _load_download_list_from_folder(self):
        for mod_info in self.downloadManager.load_download_list():
            self.downloadList_folder.add_mod(*mod_info)

    ### public functions
    
    def get_download_list(self):
        return self.downloadList_file
    
    def get_folder_list(self):
        return self.downloadList_folder

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
