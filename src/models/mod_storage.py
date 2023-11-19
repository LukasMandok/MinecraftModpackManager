class DownloadList:    
    def __init__(self):
        # list: {name : {"categories" : list(str), "coment" : str, "scope" : str} }
        self.list = {}
        # dict: {"scope" : {scope : {"category" : {category : {"mods" : list({"name" : str, "comment" : str})} } } }
        self.dict = {}
        
    def getList(self):
        return self.list.copy()
    
    def getDict(self):
        return self.dict.copy()
        
    def _add_to_list(self, name, categories, scope, comment = None):
        self.list[name] = {"categories" : categories.copy(),
                           "comment"    : comment,
                           "scope"       : scope}
                
    def _add_to_dict(self, name, categories, scope, comment = None):
        current_dict = self.dict.setdefault("scope", {})
        current_dict = current_dict.setdefault(scope, {})
        for category in categories:
            current_dict = current_dict.setdefault("category", {})
            current_dict = current_dict.setdefault(category, {})
        current_dict = current_dict.setdefault("mods", [])
        current_dict.append({"name" : name, "comment" : comment})
        
    def add_mod(self, name, categories, scope, comment = None):
        self._add_to_list(name, categories, scope, comment)
        self._add_to_dict(name, categories, scope, comment)
        
        
    def iterate_dict(self, current_dict = None, level = 0, next = None):
        current_dict = current_dict or self.dict
        
        for key, value in current_dict.items():     
            if next == "category":
                yield level, key, None
                yield from self.iterate_dict(value, level + 1)
            elif next == "scope":
                yield level, "[" + key + "]", None
                yield from self.iterate_dict(value, level)
                
            if key == "mods":
                for mod in value:
                    yield level, mod["name"], mod["comment"]
            elif key == "category":
                yield from self.iterate_dict(value, level, next = "category")
            elif key == "scope":
                yield from self.iterate_dict(value, level, next = "scope")
            else:
                raise ValueError(f"Unknown key: {key}")

        
class ModList():
    def __init__(self):
        # lookup tables
        self.mod_ids = {}
        
        # data storage based on 
        self.data = {}
                
    def get_names(self):
        return [mod.name for mod in self.mod_names]
        
    def to_dict(self):
        return [mod.to_dict() for mod in self]       