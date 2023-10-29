# Import modules and packages:  
import requests
import json

# packages

# Constants:
API_URL = "https://api.modrinth.com/v2"
DOWNLOAD_URL = "https://download.modrinth.com/v2"

# Set a user agent for the requests in this format:
# User-Agent: github_username/project_name/1.56.0 (contact@launcher.com)
# This is required by the modrinth api.
USER_AGENT = "LukasMandok/MinecraftModpackManager/0.1.0_dev (mrdevilsthumb@gmail.com)"


### General access:

# get project information
# project = project_id or project_slug
def get_project(project):
    url = "{api_url}/project/{project}".format(api_url=API_URL, project=project)

    # make the request
    response = requests.get(url, headers={"User-Agent": USER_AGENT})

    # check if the request was successful
    if response.status_code == 200:
        # return the json data
        return response.json()
    else:
        response.raise_for_status()


# get information about multiple projects
# ids = list of project ids
def get_projects(ids):
    # build the url
    url = "{api_url}/projects/{ids}".format(api_url=API_URL, ids=ids)

    # call the API
    response = requests.get(url, headers={"User-Agent": USER_AGENT})

    # check the response code
    if response.status_code == 200:
        # return the json data
        return response.json()
    else:
        # raise an exception
        response.raise_for_status()


# search for a project 
def search_project(query, facets = None, limit=10, index="relevance", offset=0):
    # create the request url including facets:
    url = "{api_url}/search?query={query}&limit={limit}&index={index}&offset={offset}".format(api_url=API_URL, query=query, limit=limit, index=index, offset=offset)
    
    # add facets to the url if they are specified
    if facets:
        url += "&facets={facets}".format(facets=json.dumps(facets))

    # make the request
    print("url:", url)
    response = requests.get(url, headers={"User-Agent": USER_AGENT})

    # check if the request was successful
    if response.status_code == 200:
        # return the json data
        return response.json()
    else:
        response.raise_for_status()


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

    return results
