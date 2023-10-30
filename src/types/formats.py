from .constants import *

class SharedMod:
    def __init__(self, modrinth_mod, curseforge_mod):
        self.modrinth_mod = modrinth_mod
        self.curseforge_mod = curseforge_mod

class Mod:
    def __init__(self, source, id, name, slug, description, long_description = "", categories = [],
                 links = {}, author = "", updated = "", icon = "", downloads = 0):
        self.source = source
        self.id = str(id)
        self.name = name
        self.slug = slug
        self.description = description
        self.long_description = long_description
        self.categories = categories
        self.links = links
        self.author = author
        self.updated = updated
        self.icon = icon
        self.downloads = downloads

    def init_details(self, mod_loaders, recent_version, client_side = None, server_side = None):
        self.mod_loaders = mod_loaders
        self.recent_version = recent_version
        self.client_side = client_side
        self.server_side = server_side

    def add_version(self, version, mod_loaders, game_versions):
        self.versions[version] = {
            "mod_loaders" : mod_loaders,
            "game_versions" : game_versions
        }

    def add_game_version(self, game_versions, mod_loader, version):
        self.game_versions[game_versions] = {
            "mod_loader" : mod_loader,
            "version" : version
        }


