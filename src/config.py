import json
import os

def load_config(config_file='config/config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)

    if config.get("use_relative_paths", False):
        # Get absolute path to the scrip directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get the absolute path of the project root directory
        project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

        config['download_dir'] = os.path.join(project_dir, config['download_dir'])
        config['mod_list_file'] = os.path.join(project_dir, config['mod_list_file'])
    
    return config


with open('config/config.json', 'r') as f:
    config = load_config()

DOWNLOAD_DIR = config['download_dir']
mod_list_file = config['mod_list_file']
