from .constants import *
    
### Mod stuff
        
class ModList(list):
    def __init__(self, mods: list = []):
        super().__init__(mods)
                
    def get_names(self):
        return [mod.name for mod in self]
        
    def to_dict(self):
        return [mod.to_dict() for mod in self]        
        
        
class SourceProjectInfo:
    def __init__(self, source, project_type, id, name, slug, description, categories = [], authors = [],
                 updated = "", icon = "", downloads = 0, color = None):
        self.source      = source
        self.type        = project_type
        self.id          = str(id)
        self.name        = name
        self.slug        = slug
        self.description = description
        self.categories  = categories
        self.authors     = authors
        self.updated     = updated
        self.icon        = icon
        self.downloads   = downloads
        self.color       = color

        self.links            = {}
        self.long_description = None
        self.screenshots      = []

        # self.mod_loaders    = None
        self.recent_version = None
        self.client_side    = None
        self.server_side    = None

        self.versions       = {}
        self.game_versions  = {}

    def add_long_desc(self, long_description):
        self.long_description = long_description

    def add_screenshot(self, url, title, desc):
        screenshot = {
            "url"   : url,
            "title" : title,
            "desc"  : desc
        }
        self.screenshots.append(screenshot)

    def add_links(self, source, website=None, issues=None, wiki=None, donation=None):
        self.links = {
            'source'   : source,
            'website'  : website,
            'issues'   : issues,
            'wiki'     : wiki,
            'donation' : donation
        }

    def add_details(self, recent_version, client_side = None, server_side = None):
        # self.mod_loaders    = mod_loaders
        self.recent_version = recent_version
        self.client_side    = client_side
        self.server_side    = server_side

    def add_version(self, version, game_versions):
        self.versions[version] = {
            #"mod_loaders"   : mod_loaders,
            "game_versions" : game_versions
        }

    def add_game_version(self, game_version, versions):
        self.game_versions[game_version] = {
            #"mod_loader" : mod_loader,
            "versions"   : versions
        }

    def to_dict(self):
        return {
            "source"          : self.source.value,
            "type"            : self.type,
            "id"              : self.id,
            "name"            : self.name,
            "slug"            : self.slug,
            "description"     : self.description,
            "categories"      : self.categories,
            "links"           : self.links,
            "author"          : self.authors,
            "updated"         : self.updated,
            "icon"            : self.icon,
            "downloads"       : self.downloads,
            "color"           : self.color,
            "long_description": self.long_description,
            "screenshots"     : self.screenshots,
            # "mod_loaders"     : self.mod_loaders,
            "recent_version"  : self.recent_version,
            "client_side"     : self.client_side,
            "server_side"     : self.server_side,
            "versions"        : self.versions,
            "game_versions"   : self.game_versions,
        }
        
class SourceModInfo(SourceProjectInfo):
    def __init__(self, source, id, name, slug, description, categories = [], authors = [],
                 updated = "", icon = "", downloads = 0, color = None):
        
        self.mod_loaders    = None
        
        super().__init__(source, "mod", id, name, slug, description, categories, authors, updated, icon, downloads, color)
        
    def add_details(self, mod_loaders, recent_version, client_side = None, server_side = None):
        super().add_details(recent_version, client_side, server_side)
        self.mod_loaders    = mod_loaders
        
    def add_version(self, version, mod_loaders, game_versions):
        self.versions[version] = {
            "mod_loaders"   : mod_loaders,
            "game_versions" : game_versions
        }

    def add_game_version(self, game_versions, mod_loader, versions):
        self.game_versions[game_versions] = {
            "mod_loader" : mod_loader,
            "versions"   : versions
        }
        
    def to_dict(self):
        dict = super().to_dict()
        dict["mod_loaders"] = self.mod_loaders
        
        return dict

class SharedSourceModInfo:
    def __init__(self, modrinth_mod, curseforge_mod):
        self.modrinth_mod   = modrinth_mod
        self.curseforge_mod = curseforge_mod
        


### GameVersion

class GameVersion:
    def __init__(self, text: str):
        self.text = text
        self.v0, self.v1, self.v2 = self._convert_to_version()
         
    def _convert_to_version(self):
        split_text = self.text.split(".")
        if (len(split_text) < 2 or len(split_text) > 3):
            raise ValueError(f"Invalid game version, needs format 'x.x' or 'x.x.x', got '{self.text}")
        
        v0, v1 = map(int, split_text[:2])
        v2 = int(split_text[2]) if len(split_text) == 3 else 0
        
        return v0, v1, v2
    
    def __hash__(self):
        return hash(self.text)
        
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return f"GameVersion('{self.text}')"
    
    # equal
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 == __value.v0 and self.v1 == __value.v1 and self.v2 == __value.v2)
        
        elif isinstance(__value, str):
            cond = (self.text == __value)
            if cond: return True
            
            # maybe this is not such a good because it will take much time to compute:
            print("compare: " + self.text + " with " + __value + " , not identical text")
            converted = self.__class__(__value)
            return self.__eq__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__} or str")
    
    # greater than
    def __gt__(self, __value: object) -> bool:
        cond1 = False
        cond2 = False
        cond3 = False
        
        if isinstance(__value, type(self)):
            cond1 = (self.v0 > __value.v0)
            if cond1: return True
            
            cond2 = (self.v0 >= __value.v0 and self.v1 > __value.v1)
            if cond2: return True
            
            cond3 = (self.v0 >= __value.v0 and self.v1 >= __value.v1 and self.v2 > __value.v2)
            return cond3
        
        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__gt__(converted)      
              
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__} or str")
    
    
    # greater equal
    def __ge__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 >= __value.v0 and self.v1 >= __value.v1 and self.v2 >= __value.v2)

        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__ge__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__}")

        
    # less than
    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            cond1 = (self.v0 < __value.v0)
            if cond1: return True
            cond2 = (self.v0 <= __value.v0 and self.v1 < __value.v1)
            if cond2: return True
            cond3 = (self.v0 <= __value.v0 and self.v1 <= __value.v1 and self.v2 < __value.v2)
            if cond3: return True
        
        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__lt__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__}")

    # less equal
    def __le__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 <= __value.v0 and self.v1 <= __value.v1 and self.v2 <= __value.v2)
        
        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__le__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__}")


    ### Class Methods
        
    @classmethod
    def find_latest(cls, game_versions: list) -> "GameVersion":
        latest = None
        for game_version in game_versions:
            try:
                game_version = cls(game_version)
            except ValueError:
                print("GameVersion: " + game_version + " is not supported")
                continue
            if latest is None or game_version > latest:
                latest = game_version
                
        return latest