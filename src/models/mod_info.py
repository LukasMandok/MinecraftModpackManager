class SourceProjectInfo:
    def __init__(self, source, id, name, slug, description, categories = [], authors = [],
                 updated = "", icon = "", downloads = 0, color = None, project_type = None): #, old_project_data = None
        self.source      = source
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
        
        # TODO: remove in case this is not needed (adding information at an earlier stage)
        self.type             = project_type
        #self.old_project_data = old_project_data

        self.api              = None
        self.links            = {}
        self.long_description = None
        self.screenshots      = []

        # self.mod_loaders    = None
        self.recent_version = None
        self.client_side    = None
        self.server_side    = None

        self.version_dict       = None
        self.game_version_dict  = None
        
    # redirect access on modinfo to the api
    # def __getattr__(self, method):
    #     if self.api:
    #         return getattr(self.api, method)

    def add_api(self, api):
        self.api = api

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

    def add_version_dict(self, version_dict):
        self.version_dict = version_dict
        
    def add_game_version_dict(self, game_version_dict):
        self.game_version_dict = game_version_dict

    # def add_version(self, version, game_versions):
    #     self.version_dict[version] = {
    #         #"loaders"   : loaders,
    #         "game_versions" : game_versions
    #     }

    # def add_game_version(self, game_version, versions):
    #     self.game_version_dict[game_version] = {
    #         #"loader" : loader,
    #         "versions"   : versions
    #     }

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
            
            "versions_dict"   : self.version_dict,
            "game_versions_dict": self.game_version_dict,
        }
        
        
class SourceModInfo(SourceProjectInfo):
    def __init__(self, source, id, name, slug, description, categories = [], authors = [],
                 updated = "", icon = "", downloads = 0, color = None, project_type = "mod"): #  project_info = None
        
        self.mod_loaders    = None
        project_type        = "mod"
        self.loader_dict    = None
        
        super().__init__(source, id, name, slug, description, categories, authors, updated, icon, downloads, color, project_type)
        
    def add_details(self, mod_loaders, recent_version, client_side = None, server_side = None):
        super().add_details(recent_version, client_side, server_side)
        self.mod_loaders    = mod_loaders
        
    # def add_version(self, version, loaders, game_versions):
    #     self.version_dict[version] = {
    #         "loaders"   : loaders,
    #         "game_versions" : game_versions
    #     }

    # def add_game_version(self, game_versions, loader, versions):
    #     self.game_version_dict[game_versions] = {
    #         "loader" : loader,
    #         "versions"   : versions
    #     }
        
    def add_loader_dict(self, loader_dict):
        self.loader_dict = loader_dict
        
        
    def to_dict(self):
        dict = super().to_dict()
        dict["loaders"] = self.mod_loaders
        dict["loader_dict"] = self.loader_dict
        
        return dict


class SharedSourceModInfo:
    def __init__(self, m_mod = None, c_mod = None):
        self.m_mod = m_mod
        self.c_mod = c_mod
        
        self.mods = [self.m_mod, self.c_mod]
        
    def __str__(self):
        m_name = self.m_mod.name if self.m_mod is not None else "None"
        c_name = self.c_mod.name if self.c_mod is not None else "None"
        
        return f"SharedSourceModInfo: {m_name} | {c_name}"
    
    def __getattr__(self, method):
        return_list = []
        for mod in self.mods:
            if mod is not None:
                return_list.append(getattr(mod, method))
            else:
                return_list.append(None)
                
        return return_list



class ModInfoList(list):
    def __init__(self, mods: list = []):
        super().__init__(mods)
                
    def get_names(self):
        return [mod.name for mod in self]
        
    def to_dict(self):
        return [mod.to_dict() for mod in self]      