# Import modules and packages:  
import json

# packages
from ..types.formats import *
from ..types.constants import *

from .base_api import BaseAPI
from .high_level_api import HighLevelAPI


class CurseForgeAPI(BaseAPI): #, HighLevelAPI
    def __init__(self):
        self.name = "CurseForge API"
        self.api_url_search = "https://www.curseforge.com/api/v1"

        self.loader_types = {
            None : 0,
            Modloader.FORGE : 1,
            Modloader.FABRIC : 4,
            Modloader.QUILT : 5,
            Modloader.NEOFORGE : 6
        }

        api_url = "https://api.curseforge.com/v1"
        download_url = "https://api.curseforge.com/v1"
        api_key = "$2a$10$IGsBR6CXosB.y2eYiS6eQu7a6CCDKGDBeLOeqMcIeLnSCAJBOiAee"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': api_key
        }

        super().__init__(api_url, download_url, headers)

        #BaseAPI.__init__(self, api_url, download_url, headers)
        # TODO: I am not sure if this implementation if ok
        #HighLevelAPI.__init__(self, self)
        
    ### Declare Class specific variables
    @property
    def name_tag(self): return "name"
    @property
    def id_tag(self): return "id"
    @property
    def search_id_tag(self): return "id"

    ### General API Access

    # get all games on curseforge
    def get_games(self, debug = False):
        sub_url = f"/games"

        return self.request(sub_url, debug = debug)


    # get all categories for a game on curseforge
    def get_categories(self, gameId = 432, debug = False):
        sub_url = f"/categories"

        params = {"gameId" : gameId}
        
        return self.request(sub_url, params, debug = debug)


    # get project details from a project id
    def get_project(self, id, debug = False):
        sub_url = f"/mods/{id}"

        return self.request(sub_url, debug = debug)


    def get_projects(self, ids, debug = False):
        sub_url = "/mods"
        
        body = {
            "modIds": list(ids),
            "filterPcOnly": True
        }

        result = self.request(sub_url, None, body, debug = debug)

        if result is None:
            return None
        
        return result["data"]

    # params:
    # gameId (int), classId (int), categoryId (int), categoryIds (string), gameVersion (string)
    # searchFilter (string), sortField (ModsSearchSortField), sortOrder (SortOrder), 
    # modLoaderType (ModLoaderType), modLoaderTypes (sting), gameVersionTypeID (int), 
    # authorId (int), primaryAuthorId (int)
    # 
    # slug (string), index (int), pageSize (int) 
    def search_project(self, params, debug = False):
        sub_url = f"/mods/search"
        return self.request(sub_url, params, custom_url = self.api_url_search, debug = debug)


    ### Specific access:

    # help functions
    def get_modloader_type(self, name):
        return self.loaders[name]


    # search for a mod
    def search_mod(self, name, version = None, modloader = None, count = 50, debug = False):
        params = {
            "filterText" : name,
            "gameId" : 432, # Minecraft
            "gameVersion" : version,
            "sortField" : 1,
            "pageSize" : count,
            "index" : 0
        }
        
        # old parameters (for normal search API)
        # params = {"searchFilter" : name,
        #           "gameId" : 432,
        #           "pageSize" : count,
        #           "Index" : 0}

        # set modloader type for single of multiple modloaders
        if modloader:
            if isinstance(modloader, list):
                params["gameFlavors"] = []
                for m in modloader:
                    params["gameFlavors"].append(self.get_modloader_type(m))
            else:
                params["gameFlavors"] = self.get_modloader_type(modloader)

        results = self.search_project(params)	

        if not "data" in results or len(results["data"]) == 0:
            return None

        return results["data"]


    # extract data from a project
    
    @staticmethod
    def extract_data(data):
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
            server_side    = data['latestFiles'][0]['isServerPack'] if data['latestFiles'] and 'isServerPack' in data['latestFiles'][0] else None,
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