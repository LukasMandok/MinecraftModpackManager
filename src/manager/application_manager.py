from . import api_manager, data_manager, download_manager, project_manager, file_manager

from ..models.constants import Sources

import json

class ApplicationManager:
    def __init__(self):
        self.projectManager = project_manager.ProjectManager()
        self.apiManager = api_manager.ApiManager()
        self.fileManager = file_manager.FileManager()
        self.downloadManager = download_manager.DownloadManager(self.apiManager)
        self.dataManager = data_manager.DataManager(self.fileManager, self.downloadManager)

    def get_mod_search_results(self, name, source = Sources.UNKNOWN):
        # first look in the local data
        mods = self.dataManager.find_mod(name)

        # if not found, search the api
        if mods is None:
            mods = self.apiManager.get_mod_search_results(name, source = source)

        if mods is None:
            return None

        mods_dict = mods.to_dict()
        
        # return result into json
        return json.dumps(mods_dict, default=str)
