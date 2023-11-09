class DownloadList:    
    def __init__(self):
        self.list = {}
        self.dict = {}
        
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