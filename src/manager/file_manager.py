import json
import os

from ..config import config 

class FileManager:
    def __init__(self):
        self.mod_list_file = config.mod_list_file
        self.download_list_file = config.download_list_file

        #self.mod_list = self._load_mod_list()
        #self.download_mod_list, self.download_mod_dict = self._load_download_list()
    
        
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
            #lines = file.readlines()
        #return self.parse_download_file(lines)      
    
    
    @staticmethod
    def parse_download_file(file):
        mod_dict = {}
        mod_list = {}
                
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
        
        # def add_mod(name, categories, comment = None):
        #     mod_list[name] = {"categories"   : categories.copy(),
        #                        "comment"      : comment}

        #     current_dict = mod_dict
        #     #categories = categories or [None]
        #     for category in categories:
        #         current_dict = current_dict.setdefault("category", {})
        #         current_dict = current_dict.setdefault(category, {})
        #     current_dict = current_dict.setdefault("mods", [])
        #     current_dict.append({"name" : name, "comment" : comment})
                    
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
                    #add_mod(line, current_categories, comment)
                    yield mod, current_categories, comment
                    # remove |diff| number of categories
                    current_categories = current_categories[:diff]
                    
                elif diff == 0:
                    # add mod:
                    #add_mod(mod, current_categories, comment)
                    yield mod, current_categories, comment
                    
            mod = next_mod
            indentation = next_indentation
            comment = next_comment
            
        # Process the last line of the file
        if mod:
            #add_mod(mod, current_categories, next_comment)
            yield mod, current_categories, next_comment
            
        #return mod_dict, mod_list
    
    
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
        
        # def compare_categories(categories1, categories2):
        #     if categories1 == categories2:
        #         return False
        #     mask = [c1 == c2 for c1, c2 in zip(categories1, categories2)]
        #     intendation =  mask.index(False) if False in mask else sum(mask)
        #     return intendation
        
            
        # for mod, mod_info in mod_dict.items():
        #     categories = mod_info["categories"]
        #     intendation = compare_categories(current_categories, categories)
            
        #     # Add mod with the same indentation as the last category
        #     mod_line = ' ' * (len(mod_info["categories"]) * 4) + mod
        #     # Add comment if it exists
        #     if mod_info["comment"]:
        #         mod_line += "  # " + mod_info["comment"]
        #     lines.append(mod_line)
        # return lines