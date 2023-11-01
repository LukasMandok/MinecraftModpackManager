# Import modules and packages:  
import json

# packages
from ..types.formats import *
from ..types.constants import *

from .base_api import BaseAPI


class ModrinthAPI(BaseAPI):
    def __init__(self):
        user_agent = "LukasMandok/MinecraftModpackManager/0.1.0_dev (mrdevilsthumb@gmail.com)"

        api_url = "https://api.modrinth.com/v2"
        download_url = "https://download.modrinth.com/v2"
        headers = {
            'User-Agent': user_agent,
        }

        super().__init__(api_url, download_url, headers)
        
    ### Declare Class specific variables
    def name_tag(self): return "title"
    def id_tag(self): return "project_id"

    ### General API Access

    # get project information
    # project = project_id or project_slug  
    def get_project(self, project, debug = False):
        sub_url = f"/project/{project}"

        return self.request(sub_url, debug = debug)
    
    # get information about multiple projects
    # ids = list of project ids
    def get_projects(self, project_ids, debug = False):
        sub_url = "/projects"

        params = {"ids" : json.dumps(project_ids)}

        return self.request(sub_url, params, debug = debug)


    # get mod versions:
    def get_project_versions(self, project, debug = False):
        sub_url = f"/projects/{project}/version"

        return self.request(sub_url, debug = debug)

    # get details about a specific version
    def get_version(self, version_id, debug = False):
        sub_url = f"/version/{version_id}"

        return self.request(sub_url, debug = debug)

    # get details for multiple versions
    def get_versions(self, version_ids, debug = False):
        sub_url = "/versions"

        params = {"ids" : json.dumps(version_ids)}

        return self.request(sub_url, params, debug = debug)
        
    # search for a project 
    def search_project(self, params, debug = False):
        # create the request url including facets:
        sub_url = "/search"

        return self.request(sub_url, params, debug = debug)
    
    ### Specific access

    # search for a mod
    def search_mod(self, name, version = None, modloader = None, count = 20, debug = False):
        
        params = {
            "query" : name,
            "limit" : count,
            "index" : "relevance",
            "offset" : 0,
            "facets" : [[ "project_type : mod" ]]
        }
        
        # if version is a list, iterate over entries, create a list like this: versions=["versions:1.16.5", "versions:1.19.3"]
        versions = []
        if version:
            if isinstance(version, list):  
                for v in version:
                    versions.append(f"versions:{v}")
            else:
                versions.append(f"versions:{version}")
                
            params["facets"].append(versions)

        #do the same for modloader:
        
        modloaders = []
        if modloader:
            if isinstance(modloader, list):
                for m in modloader:
                    modloaders.append(f"categories:{m}")
            else:
                modloaders.append(f"categories:{modloader}")
                
            params["facets"].append(modloaders)
        
        print("name:", name)

        results = self.search_project(params, debug = debug)

        if len(results["hits"]) == 0:
            return None
        
        return results["hits"]



