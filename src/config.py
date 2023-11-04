import json
import os

def load_config(config_file = None):
    if config_file is None:
        # Get the directory containing the current script file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get the project root directory
        project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        
        # Construct the path to the config file:
        config_file = os.path.join(project_dir, 'config', 'config.json')
           
    with open(config_file, 'r') as f:
        config = json.load(f)

    if config.get("use_relative_paths", False):
        # Get absolute path to the scrip directory
        config['download_dir'] = os.path.join(project_dir, config['download_dir'])
        config['mod_list_file'] = os.path.join(project_dir, config['mod_list_file'])
    
    return config


config = load_config()

DOWNLOAD_DIR = config['download_dir']
mod_list_file = config['mod_list_file']
