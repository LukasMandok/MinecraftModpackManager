import json
import os

class Config:
    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if self.config_file is None:
            # Get the directory containing the current script file:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Get the project root directory
            project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
            
            # Construct the path to the config file:
            self.config_file = os.path.join(project_dir, 'config', 'config.json')
               
        with open(self.config_file, 'r') as f:
            config = json.load(f)

        if config.get("use_relative_paths", True):
            # Get absolute path to the script directory
            config['download_dir'] = os.path.join(project_dir, config['download_dir'])
            config['database_file'] = os.path.join(project_dir, config['database_file'])
            config['download_list_file'] = os.path.join(project_dir, config['download_list_file'])
            
        return config

    @property
    def download_dir(self):
        return self.config['download_dir']

    @property
    def database_file(self):
        return self.config['database_file']
    
    @property
    def download_list_file(self):
        return self.config['download_list_file']

# Usage:
config = Config()
# print(config.download_dir)
# print(config.mod_list_file)