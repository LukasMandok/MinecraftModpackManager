from . import api_manager as api

import json
import os

from ..config import config

# This class should be created to 
class DownloadManager:
    def __init__(self, api_manager):
        self.api_manager = api_manager
        
        self.download_dir = config.download_dir
    
    # create a generator which ready in the datastructure in download_dir:
    def load_download_list(self):
        print("initialize load download list function")
        for root, dirs, files in os.walk(self.download_dir):
            for name in files:
                relative_root = os.path.relpath(root, self.download_dir)
                
                loader, version, scope, *categories = relative_root.split(os.path.sep)
                
                # split name at the first "-" if there is one
                name = name.split("-", 1)[0]
                
                yield name, categories, scope, None