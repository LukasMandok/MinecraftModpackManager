from . import api_manager as api

import json
import os

from ..config import config

# This class should be created to 
class DownloadManager:
    def __init__(self, api_manager):
        self.api_manager = api_manager
        
        self.download_dir = config.download_dir
    
    