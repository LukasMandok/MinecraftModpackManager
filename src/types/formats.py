from .constants import *

class SharedMod:
    def __init__(self, modrinth_mod, curseforge_mod):
        self.modrinth_mod   = modrinth_mod
        self.curseforge_mod = curseforge_mod

class Mod:
    def __init__(self, source, id, name, slug, description, categories = [], author = "",
                 updated = "", icon = "", downloads = 0, color = None):
        self.source      = source
        self.id          = str(id)
        self.name        = name
        self.slug        = slug
        self.description = description
        self.categories  = categories
        self.author      = author
        self.updated     = updated
        self.icon        = icon
        self.downloads   = downloads
        self.color       = color

        self.links            = {}
        self.long_description = None
        self.screenshots      = []

        self.mod_loaders    = None
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

    def add_details(self, mod_loaders, recent_version, client_side = None, server_side = None):
        self.mod_loaders    = mod_loaders
        self.recent_version = recent_version
        self.client_side    = client_side
        self.server_side    = server_side

    def add_version(self, version, mod_loaders, game_versions):
        self.versions[version] = {
            "mod_loaders"   : mod_loaders,
            "game_versions" : game_versions
        }

    def add_game_version(self, game_versions, mod_loader, version):
        self.game_versions[game_versions] = {
            "mod_loader" : mod_loader,
            "version"    : version
        }

    def to_dict(self):
        return {
            "source"          : self.source.value,
            "id"              : self.id,
            "name"            : self.name,
            "slug"            : self.slug,
            "description"     : self.description,
            "categories"      : self.categories,
            "links"           : self.links,
            "author"          : self.author,
            "updated"         : self.updated,
            "icon"            : self.icon,
            "downloads"       : self.downloads,
            "color"           : self.color,
            "long_description": self.long_description,
            "screenshots"     : self.screenshots,
            "mod_loaders"     : self.mod_loaders,
            "recent_version"  : self.recent_version,
            "client_side"     : self.client_side,
            "server_side"     : self.server_side,
            "versions"        : self.versions,
            "game_versions"   : self.game_versions,
        }

