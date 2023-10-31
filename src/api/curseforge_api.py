# Import modules and packages:  
import requests
import json

# packages
from ..types.formats import *
from ..types.constants import *

from . import api

# Constants:
API_URL = "https://api.curseforge.com/v1"
API_URL_SEARCH = "https://www.curseforge.com/api/v1"
API_KEY = "$2a$10$IGsBR6CXosB.y2eYiS6eQu7a6CCDKGDBeLOeqMcIeLnSCAJBOiAee"

HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': API_KEY
}

## retrieve Data from curseforge

def get_games(debug = False):
    url = "{api_url}/games".format(api_url=API_URL)
    return api.request(url, HEADERS, debug=debug)


def get_categories(gameId = 432, debug = False):
    params = {"gameId" : gameId}
    url = "{api_url}/categories".format(api_url=API_URL)
    return api.request(url, HEADERS, params, debug=debug)


def get_project(id, debug = False):
    url = "{api_url}/mods/{modId}".format(api_url=API_URL, modId=id)
    return api.request(url, HEADERS, debug=debug)


def get_projects(ids, debug = False):
    body = {
        "modIds": list(ids),
        "filterPcOnly": True
    }

    url = "{api_url}/mods".format(api_url=API_URL)
    result = api.request(url, HEADERS, None, body, debug=debug)
    
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
def search_project(params, debug = False):
    url = "{api_url}/mods/search".format(api_url=API_URL_SEARCH)
    return api.request(url, HEADERS, params, debug=debug)

### Specific access:

# help functions
def get_modloader_type(name):
    loaders = {
        None : 0,
        FORGE : 1,
        FABRIC : 4,
        QUILT : 5
    } 
    return loaders[name]

# search for a mod
def search_mod(name, version = None, modloader = None, count = 50):
    params = {"filterText" : name,
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
                params["gameFlavors"].append(get_modloader_type(m))
        else:
            params["gameFlavors"] = get_modloader_type(modloader)

    results = search_project(params)	

    if len(results["data"]) == 0:
        return None

    return results["data"]


    # Convert Mod format