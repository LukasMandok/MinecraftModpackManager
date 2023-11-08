import json
import os

from ..config import config 

class FileManager:
    def __init__(self):
        self.mod_list_file = config.mod_list_file
        self.download_list_file = config.download_list_file

        
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
    def save_download_list(self, mod_list):
        lines = self.generate_download_file(mod_list)
        with open(self.download_list_file, 'w') as file:
            file.writelines(lines)
            
    def load_download_list(self):
        with open(self.download_list_file, 'r') as file:
            yield from self.parse_download_file(file)
    
    
    @staticmethod
    def parse_download_file(file):    
        current_categories = []
        indentation = 0
        mod = None
        intendation_steps = None
        comment = None
        
        def parse_lines(lines):
            for line in lines:
                line = line.rstrip()  # remove trailing whitespace
                indentation = len(line) - len(line.lstrip())
                line = line.strip()

                # ignore comments and empty lines
                if line.startswith("#") or not line:
                    continue

                # ignore comment part of not-empty lines and strip again
                line, *comment = line.split("#", 1)
                mod = line.strip()
                comment = comment[0].strip() if comment else None

                yield mod, indentation, comment
            
        for next_mod, next_indentation, next_comment in parse_lines(file):
            
            # calculate intendation difference to previous line and normalize to 1
            diff = next_indentation - indentation
            if intendation_steps is None:
                if diff > 0:
                    intendation_steps = diff
            else:
                diff //= intendation_steps
                
            if mod:
                if diff > 0:
                    # previous line was a category
                    current_categories.append(mod)
                    
                elif diff < 0:
                    # prvious line was a mod
                    yield mod, current_categories, comment
                    # remove |diff| number of categories
                    current_categories = current_categories[:diff]
                    
                elif diff == 0:
                    # yield mod info
                    yield mod, current_categories, comment
                    
            mod = next_mod
            indentation = next_indentation
            comment = next_comment
            
        # Process the last line of the file
        if mod:
            yield mod, current_categories, next_comment
            

    
    
    # parse 
    def generate_download_file(mods):        
        def get_spaces(intendation):
            return " " * intendation * 4
    
        # iterator over the mod_dict
        def iterate_dict(current_dict, level = 0):
            for key, value in current_dict.items():
                if key == "mods":
                    for mod in value:
                        yield level, mod["name"], mod["comment"]
                elif key == "category":
                    yield from iterate_dict(value, level)
                else:
                    yield level, key, None
                    yield from iterate_dict(value, level + 1)
                    
        
        lines = []
        for level, name, comment in iterate_dict(mods):
            line = get_spaces(level) + name
            if comment:
                line += " # " + comment
            lines.append(line)

        
        return lines