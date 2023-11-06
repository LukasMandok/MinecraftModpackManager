# Import modules and packages:  
import json

# packages
from ..models.formats import GameVersion
from ..models.mod_info import SourceModInfo
from ..models.constants import *

from .base_api import BaseAPI
from .high_level_api import HighLevelAPI


class ModrinthAPI(BaseAPI): #, HighLevelAPI
    def __init__(self):
        self.name = "Modrinth API"
        
        user_agent = "LukasMandok/MinecraftModpackManager/0.1.0_dev (mrdevilsthumb@gmail.com)"

        api_url = "https://api.modrinth.com/v2"
        download_url = "https://download.modrinth.com/v2"
        headers = {
            'User-Agent': user_agent,
        }

        super().__init__(api_url, download_url, headers)

        # BaseAPI.__init__(self, api_url, download_url, headers)
        # TODO: No idea, if this allowed to do.
        # HighLevelAPI.__init__(self, self)
        
    ### Declare Class specific variables
    @property
    def name_tag(self): return "title"
    @property
    def id_tag(self): return "id"
    @property
    def search_id_tag(self): return "project_id"

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
        sub_url = f"/project/{project}/version"

        return self.request(sub_url, debug = debug)
        
    # search for a project 
    def search_project(self, params, debug = False):
        # create the request url including facets:
        sub_url = "/search"

        return self.request(sub_url, params, debug = debug)
    
    
    
    ### Specific access (specifically available for this api)

    # get details about a specific version
    def get_version(self, version_id, debug = False):
        sub_url = f"/version/{version_id}"

        return self.request(sub_url, debug = debug)

    # get details for multiple versions
    def get_versions(self, version_ids, debug = False):
        sub_url = "/versions"

        params = {"ids" : json.dumps(version_ids)}

        return self.request(sub_url, params, debug = debug)
    
    # get members from a team
    def get_project_team(self, project, debug = False): 
        sub_url = f"/project/{project}/members"
        
        return self.request(sub_url, debug = debug)
    
    
        
    ### More complex, api specific functions
        
    # search for a mod
    def get_mod_search_results(self, name, version = None, modloader = None, count = 20, debug = False):
        
        params = {
            "query" : name,
            "limit" : count,
            "index" : "relevance",
            "offset" : 0,
        }
        
        # project type to mod
        facets = [[ "project_type : mod" ]]        
        
        # if version is a list, iterate over entries, create a list like this: versions=["versions:1.16.5", "versions:1.19.3"]
        versions = []
        if version:
            if isinstance(version, list):  
                for v in version:
                    versions.append(f"versions:{v}")
            else:
                versions.append(f"versions:{version}")
                
            facets.append(versions)

        #do the same for modloader:
        
        modloaders = []
        if modloader:
            if isinstance(modloader, list):
                for m in modloader:
                    modloaders.append(f"categories:{m}")
            else:
                modloaders.append(f"categories:{modloader}")
                
            facets.append(modloaders)
        
        print("name:", name)
        
        params["facets"] = json.dumps(facets)

        results = self.search_project(params, debug = debug)

        if len(results["hits"]) == 0:
            return None
        
        return results["hits"]
    
    
    def add_missing_project_info(self, project):
        # add authors:
        # FIXME: removed since it is slow
        #team = self.get_project_team(project["id"])
        ##names = [member["user"]["name"] or member["user"]["username"] for member in team]
        #names = [member["user"]["username"] for member in team]
        #project["authors"] = names
        project["authors"] = project["team"]
        
        # add recent version - this takes too long
        # versions = self.get_project_versions(project["id"])
        # project["recent_version"] = versions[0]["game_versions"][-1]        
        
        # add recent version 
        versions = project["game_versions"]
        recent_version = GameVersion.find_latest(versions)
        print("recent version:", recent_version)
        project["recent_version"] = str(recent_version)

        return project
    
    
    def decode_version_info(self, version_info):
        # version specific stuff
        version_id    = version_info["id"]
        version_num   = version_info["version_number"]
        version_date  = version_info["date_published"]
        
        dependencies = version_info["dependencies"]
        
        # file stuff
        file_url = None
        for file in version_info["files"]:
            if file["primary"] == True:
                file_url = file["url"]
            
        # game versions and loaders
        game_versions = [GameVersion(v) for v in version_info["game_versions"]]
        loaders      = version_info["loaders"]
        
        return version_id, version_num, version_date, dependencies, file_url, game_versions, loaders
    
    
    
    

    def extract_data(self, data):
        source      = Sources.MODRINTH 
        id          = data['id']
        name        = data['title']
        slug        = data['slug']
        description = data['description']
        categories  = data['categories']

        # Assuming 'team' refers to the author. 
        authors     = data['authors']
        updated     = data['updated']
        icon        = data['icon_url']
        downloads   = data['downloads']
        color       = data.get('color', None)

        mod_info = SourceModInfo(source, id, name, slug, description, categories, authors, updated, icon, downloads, color)
                
        # Initializing additional details if available in the data


        mod_info.add_details(
            mod_loaders    = data.get('loaders', []),
            recent_version = data.get("recent_version", None),
            client_side    = data.get('client_side', None),
            server_side    = data.get('server_side', None)
        )

        mod_info.add_links(
            source   = data.get('source_url', None),
            website  = None,
            issues   = data.get('issues_url', None),
            wiki     = data.get('wiki_url', None),
            donation = data['donation_urls'][0] if data['donation_urls'] else None
        )

        mod_info.add_long_desc(
            data['body']
        )

        for screenshot in data['gallery']:
            mod_info.add_screenshot(
                url   = screenshot['url'],
                title = screenshot['title'],
                desc  = screenshot['description']
            )

        return mod_info


