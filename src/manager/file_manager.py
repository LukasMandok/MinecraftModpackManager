import json
import os

from ..config import config 

class FileManager:
    def __init__(self):
        self.mod_list_file = config.mod_list_file
        self.download_list_file = config.get_download_list_file
        self.data = None

        self._load_mod_list()
        self._load_download_list()
        
    ### private functions
        
    # Json Mod List
    def _load_mod_list(self):
        # create the file if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"mods": {}}, f)


        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        return data


    def _save_mod_list(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)
            
            

    # Txt download List
    def _load_download_list(self):
        with open(self.download_list_file, 'r') as file:
            lines = file.readlines()
        
        
    
    def _save_download_list(self, data):
        pass
    
    @staticmethod
    def parse_file(lines):
        current_categories = []
        previous_indentation = 0
        previous_line = None
        mods = {}
        intendation_steps = None
        
        def add_mod(name, categories):
            mods[name] = categories.copy()
        
        for line in lines:
            line = line.rstrip() # remove trailing whitespace
            
            # TODO: more preciise way to determine indentation (separate tabs from spaces)
            indentation = len(line) - len(line.lstrip())
            line = line.strip()
            
            # ignore comments and emtpy lines
            if line.startswith("#") or line is None or line == "":
                continue
            
            # ignore comment part of not-empty lines and strip again
            line = line.split("#")[0].strip()
            
            # calculate intendation difference to previous line and normalize to 1
            diff = indentation - previous_indentation
            if intendation_steps is None:
                if diff > 0:
                    intendation_steps = diff
            else:
                diff //= intendation_steps
                
            if previous_line:
                if diff > 0:
                    # previous line was a category
                    current_categories.append(previous_line)
                    
                elif diff < 0:
                    # prvious line was a mod
                    add_mod(previous_line, current_categories)
                    # remove |diff| number of categories
                    current_categories = current_categories[:diff]
                    
                elif diff == 0:
                    # add mod:
                    add_mod(previous_line, current_categories)
                    
            previous_line = line
            previous_indentation = indentation
            
        # Process the last line of the file
        if previous_line:
            add_mod(previous_line, current_categories)