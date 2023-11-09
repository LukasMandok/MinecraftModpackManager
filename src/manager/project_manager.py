import json

from ..models.mod_info import SourceProjectInfo
from ..models.mod import Project, Mod
from ..models.mod_storage import ModList


class ProjectManager:
    def __init__(self):
        self.modList = ModList()

    def create_project(mod_info : SourceProjectInfo, categories : list[str] = None):
        type = mod_info.type
        if type == "mod":
            if categories:
                category = categories[0]
                subcategories = categories[1:] if len(categories) > 1 else None
            else: 
                pass
                # TODO: extract categories from mod_info
                
            return Mod(mod_info.name, mod_info.type, category, subcategories, mod_info.description, mod_info.authors)

    def init_mod_list_from_download_list(self, data):
        pass
        
### Example self.versions:

# {
#   "1.16.5" : {
#       "fabric" : {
#           "sources" : {
#               "modrinth" : {
#                   "id" : "modrinth_id",
#                   "version_id" : "modrinth_version_id",
#                   "url" : "modrinth_download_url",
#                   "filename" : "modrinth_filename",
#                   "date" : "modrinth_date"
#               },
#               "curseforge" : {
#                   "id" : "curseforge_id",
#                   "version_id" : "curseforge_version_id",
#                   "url" : "curseforge_download_url",
#                   "filename" : "curseforge_filename",
#                   "date" : "curseforge_date"
#               }
#           }
#       },
#       "forge" : {
#           "downlaoad" : {
#               "source" : "modrinth",
#               "path" : "path_to_file",
#               "download_date" : "download_date"
#           }
#           "sources" : {
#               "modrinth" : {
#                   "id" : "modrinth_id",
#                   "version_id" : "modrinth_version_id",
#                   "url" : "modrinth_download_url",
#                   "filename" : "modrinth_filename",
#                   "date" : "modrinth_date"
#               },
#               "curseforge" : {
#                   "id" : "curseforge_id",
#                   "version_id" : "curseforge_version_id",
#                   "url" : "curseforge_download_url",
#                   "filename" : "curseforge_filename",
#                   "date" : "curseforge_date"
#               }
#           }
#       }
#   }
# }