import json

from ..models.mod import Project, Mod


class ProjectManager:
    def __init__(self):
        pass

    def create_project(info):
        type = info["type"]
        if type == "mod":
            return Mod(info["name"], info["type"], info["category"], info["subcategories"], info["description"], info["authors"])


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