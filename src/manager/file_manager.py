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

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # the file is corrupt, so we'll just start fresh
            data = {"mods": {}}
        
        return data


    def _save_mod_list(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)
            f.flush()
            os.fsync(f.fileno())
            
            

    # Txt download List
    def save_download_list(self, mod_list):
        lines = self.generate_download_file(mod_list)
        try:
            with open(self.download_list_file, 'w') as file:
                file.writelines(lines)
        except Exception as e:
            print(f'Error saving download list: {e}')
        
            
    def load_download_list(self):
        try:
            with open(self.download_list_file, 'r') as file:
                yield from self.parse_download_file(file)
        except OSError as error:
            print(f'Error: {error}')
            exit(1)
    
    
    @staticmethod
    def parse_download_file(file):    
        current_categories = []
        indentation = 0
        mod = None
        intendation_steps = None
        comment = None
        scope = None
        next_scope = None
        
        def parse_lines(lines):
            nonlocal next_scope
            for line in lines:
                # remove trailing whitespace
                line = line.rstrip()
                # get the indentation
                indentation = len(line) - len(line.lstrip())
                # remove whitespace from the line also on the left
                line = line.strip()
                
                # ignore comments and empty lines
                if line.startswith("#") or not line:
                    continue

                # ignore comment part of not-empty lines and strip again
                line, *comment = line.split("#", 1)
                line = line.strip()
                comment = comment[0].strip() if comment else None

                if line.startswith("[") and line.endswith("]"): 
                    next_scope = line[1:-1].lower()
                    continue

                yield line, indentation, comment
            
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
                    yield mod, current_categories, scope, comment
                    # remove |diff| number of categories
                    current_categories = current_categories[:diff]
                    
                elif diff == 0:
                    # yield mod info
                    yield mod, current_categories, scope, comment
                    
            mod = next_mod
            indentation = next_indentation
            comment = next_comment
            scope = next_scope
            
        # Process the last line of the file
        if mod:
            yield mod, current_categories, scope, next_comment
            
    
    
    # parse 
    def generate_download_file(mods):        
        def get_spaces(intendation):
            return " " * intendation * 4
    
        # iterator over the mod_dict
        def iterate_dict(current_dict, level = 0, next = None):
            for key, value in current_dict.items():     
                if next == "category":
                    yield level, key, None
                    yield from iterate_dict(value, level + 1)
                elif next == "scope":
                    yield level, "[" + key + "]", None
                    yield from iterate_dict(value, level)
                    
                if key == "mods":
                    for mod in value:
                        yield level, mod["name"], mod["comment"]
                elif key == "category":
                    yield from iterate_dict(value, level, next = "category")
                elif key == "scope":
                    yield from iterate_dict(value, level, next = "scope")
                else:
                    raise ValueError(f"Unknown key: {key}")
        
        lines = []
        for level, name, comment in iterate_dict(mods):
            line = get_spaces(level) + name
            if comment:
                line += " # " + comment
            lines.append(line)

        
        return lines