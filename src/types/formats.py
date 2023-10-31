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



def extract_modrinth_data(data):
    source      = Sources.MODRINTH 
    id          = data['id']
    name        = data['title']
    slug        = data['slug']
    description = data['description']
    categories  = data['categories']

    # Assuming 'team' refers to the author. 
    author      = data['team']
    updated     = data['updated']
    icon        = data['icon_url']
    downloads   = data['downloads']
    color       = data.get('color', None)

    mod = Mod(source, id, name, slug, description, categories, author, updated, icon, downloads, color)
            
    # Initializing additional details if available in the data


    mod.add_details(
        mod_loaders    = data.get('loaders', []),
        recent_version = data['game_versions'][0] if data['game_versions'] else None,
        client_side    = data.get('client_side', None),
        server_side    = data.get('server_side', None)
    )

    mod.add_links(
        source   = data.get('source_url', None),
        website  = None,
        issues   = data.get('issues_url', None),
        wiki     = data.get('wiki_url', None),
        donation = data['donation_urls'][0] if data['donation_urls'] else None
    )

    mod.add_long_desc(
        data['body']
    )

    for screenshot in data['gallery']:
        mod.add_screenshot(
            url   = screenshot['url'],
            title = screenshot['title'],
            desc  = screenshot['description']
        )

    return mod


def extract_curseforge_data(data):
    source      = Sources.CURSEFORGE  # Assuming CURSEFORGE is a constant you've defined
    id          = data['id']
    name        = data['name']
    slug        = data['slug']
    description = data['summary']
    color       = None

    categories  = [category['name'] for category in data['categories']]

    # Extracting authors
    author      = [author['name'] for author in data['authors']]
    updated     = data['dateModified']
    icon        = data['logo']['url'] if 'logo' in data and data['logo'] else None
    downloads   = data['downloadCount']
    
    # Creating the Mod object
    mod = Mod(source, id, name, slug, description, categories, author, updated, icon, downloads, color)

    # Extracting additional details
    mod.add_details(
        # TODO: add mod_loader from gameVersions or latestFilesIndexes (sometimes missing) + need to be converted
        mod_loaders    = data['latestFilesIndexes'][0]['modLoader'] if data['latestFilesIndexes'] and 'modLoader' in data['latestFilesIndexes'][0] else None,
        recent_version = data['latestFilesIndexes'][0]['gameVersion'] if data['latestFilesIndexes'] and 'gameVersion' in data['latestFilesIndexes'][0] else None,
        client_side    = None, 
        server_side    = data['latestFiles'][0]['isServerPack']
    )

    mod.add_links(
        source   = data.get('sourceUrl', None),
        website  = data.get('websiteUrl', None),
        issues   = data.get('issuesUrl', None),
        wiki     = data.get('wikiUrl', None),
        donation = None
    )

    for screenshot in data['screenshots']:
        mod.add_screenshot(
            url   = screenshot['url'],
            title = screenshot['title'],
            desc  = screenshot['description']
        )

    return mod
