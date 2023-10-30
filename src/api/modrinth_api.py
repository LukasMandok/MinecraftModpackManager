# Import modules and packages:  
import json

# packages
from ..types.formats import *
from ..types.constants import *

from . import api

# Constants:
API_URL = "https://api.modrinth.com/v2"
DOWNLOAD_URL = "https://download.modrinth.com/v2"

# Set a user agent for the requests in this format:
# User-Agent: github_username/project_name/1.56.0 (contact@launcher.com)
# This is required by the modrinth api.
USER_AGENT = "LukasMandok/MinecraftModpackManager/0.1.0_dev (mrdevilsthumb@gmail.com)"
HEADERS = {"User-Agent": USER_AGENT}

# get project information
# project = project_id or project_slug
def get_project(project, debug = False):
    url = "{api_url}/project/{project}".format(api_url=API_URL, project=project)
    return api.request(url, HEADERS, debug)

# get information about multiple projects
# ids = list of project ids
def get_projects(project_ids, debug = False):
    url = "{api_url}/projects".format(api_url=API_URL)
    params = {"ids" : json.dumps(project_ids)}
    return api.request(url, HEADERS, params, debug=debug)

# get mod versions:
def get_project_versions(project, debug = False):
    url = "{api_url}/projects/{project}/version".format(api_url=API_URL, project=project)
    return api.request(url, HEADERS, debug=debug)


def get_version(version_id, debug = False):
    url = "{api_url}/version/{version_id}".format(api_url=API_URL, version_id=version_id)
    return api.request(url, HEADERS, debug=debug)


def get_versions(version_ids, debug = False):
    url = "{api_url}/versions".format(api_url=API_URL)
    params = {"ids" : json.dumps(version_ids)}
    return api.request(url, HEADERS, params, debug=debug)




# search for a project 
def search_project(query, facets = None, limit=10, index="relevance", offset=0, debug = False):
    # create the request url including facets:
    url = "{api_url}/search".format(api_url=API_URL)
    
    params = {
        "query" : query,
        "limit" : limit,
        "index" : index,
        "offset" : offset,
        "facets" : json.dumps(facets) if facets else None
    }

    print("url:", url)
    return api.request(url, HEADERS, params, debug=debug)


### Specific access:

# search for a mod
def search_mod(name, version=None, modloader=None, count=20):
    facets = [["project_type:{}".format("mod")]]

    # if version is a list, iterate over entries, create a list like this: versions=["versions:1.16.5", "versions:1.19.3"]
    versions = []
    if version:
        if isinstance(version, list):  
            for v in version:
                versions.append("versions:{}".format(v))
        else:
            versions.append("versions:{}".format(version))
        facets.append(versions)

    #do the same for modloader:
    
    modloaders = []
    if modloader:
        if isinstance(modloader, list):
            for m in modloader:
                modloaders.append("categories:{}".format(m))
        else:
            modloaders.append("categories:{}".format(modloader))
        facets.append(modloaders)
    
    print("name:", name)

    results = search_project(name, facets, count)

    if len(results["hits"]) == 0:
        return None
    
    return results["hits"]




### Convert Modrinth Data to Mod Format
