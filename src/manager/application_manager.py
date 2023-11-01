from . import api_manager, data_manager, download_manager, project_manager

from ..types.constants import Sources

import json

class ApplicationManager:
    def __init__(self):
        self.apiManager = api_manager.ApiManager()
        self.dataManager = data_manager.DataManager()
        self.projectManager = project_manager.ProjectManager()
        self.downloadManager = download_manager.DownloadManager()

    def search_mod(self, name, source = Sources.UNKNOWN):
        # first look in the local data
        result = self.dataManager.find_mod(name)

        # if not found, search the api
        if result is None:
            result = self.apiManager.search_mod(name, source = source)

        # return result into json
        return json.dumps(result)
