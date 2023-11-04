import json



class Project:
    def __init__(self, name, type, category, subcategories, description, authors):
        self.name = name
        self.type = type
        self.category = category
        self.subcategories = subcategories
        self.description = description
        self.authors = authors

        self.versions = {}

    def __str__(self):
        return "{name}: {cat} - {desc}".format(self.name, self.category, self.description)
    
    ### Data managment

    # ad a new version to the mod
    def add_version(self, version, source, id, version_id, url, filename, upload_date):
        if version in self.versions:
            if source in self.versions[version]["sources"]:
                return False
            else:
                # add the source to the dict
                self.versions[version]["sources"][source] = {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}
        else:
            self.versions[version] = {"sources" : {source: {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}}}
        return True


    def add_download(self, version, source, path, download_date, active):      
        # raise error, if the version was not added correctly to the mod before
        if version not in self.versions:
            raise ValueError("Version not found")
        elif source not in self.versions[version]["sources"]:
            raise ValueError("source not found")
        
        # check if the version has been already downloaded:
        if self.versions[version]["download"]:
            return False

        # add the download to the dict
        self.versions[version]["download"] = {"source" : source, "path" : path, "download_date" : download_date, "active" : active}
        return True
    
    

class Mod(Project):
    #def __init__(self, name, type, category, subcategories, description, author):
    #    super().__init__(self, name, type, category, subcategories, description, author)

    def add_version(self, version, modloader, source, id, version_id, url, filename, upload_date):
        if version in self.versions:
            if modloader in self.versions[version]:
                if source in self.versions[version][modloader]["sources"]:
                    return False
                else:
                    # add the source to the dict
                    self.versions[version][modloader]["sources"][source] = {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}
            else:
                # add the modloader to the dict
                self.versions[version][modloader] = {"sources" : {source: {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}}}
        else:
            self.versions[version] = {modloader : {"sources" : {source: {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}}}}
        return True


    def add_download(self, version, modLoader, source, path, download_date, active):      
        # raise error, if the version was not added correctly to the mod before
        if version not in self.versions:
            raise ValueError("Version not found")
        elif modLoader not in self.versions[version]:
            raise ValueError("ModLoader not found")
        elif source not in self.versions[version][modLoader]["sources"]:
            raise ValueError("source not found")
        
        # check if the version has been already downloaded:
        if self.versions[version][modLoader]["download"]:
            return False

        # add the download to the dict
        self.versions[version][modLoader]["download"] = {"source" : source, "path" : path, "download_date" : download_date, "active" : active}
        return True


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