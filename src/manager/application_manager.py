from . import api_manager, data_manager, project_manager

from ..models.constants import Sources

import json
from pprint import pprint
import asyncio

class ApplicationManager:
    def __init__(self, app):
        self.app = app
        self.projectManager = project_manager.ProjectManager()
        self.apiManager = api_manager.ApiManager()
        # self.DatabaseManager = await database_manager.DatabaseManager()
        # self.downloadManager = await download_manager.DownloadManager(self.apiManager)
        self.dataManager = data_manager.DataManager(self.apiManager)   #self.DatabaseManager, self.downloadManager

    def get_mod_search_results(self, name, source = Sources.UNKNOWN):
        # first look in the local data
        #mods = self.dataManager.find_mod(name)
        mods = None

        # if not found, search the api
        if mods is None:
            mods = self.apiManager.get_mod_search_results(name, source = source)

        if mods is None:
            return None

        mods_dict = mods.to_dict()
        
        # return result into json
        return json.dumps(mods_dict, default=str)
    
    
    def create_download_list(self):
        download_list = self.dataManager.get_download_list()
        print("Downlaod List - List:")
        pprint(download_list.list)
        print("Downlaod List - Dict:")
        pprint(download_list.dict)
        
        self.app.send_download_list(download_list.getList())