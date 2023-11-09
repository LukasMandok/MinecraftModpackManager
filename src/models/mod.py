
class Project:
    def __init__(self, name, project_type, category, subcategories, description, authors):
        self.name = name
        self.type = project_type
        self.category = category
        self.subcategories = subcategories
        self.description = description
        self.authors = authors
        
        # updated at later access
        self.access_date = None
        self.modified_date = None
        
        self.sources = {}

        self.versions = {}

    def __str__(self):
        return "{name}: {cat} - {desc}".format(self.name, self.category, self.description)
    
    ### Data managment
    
    ## Source Managment
    def add_source(self, source, id, url, modified_date, data):
        if source in self.sources:
            return False
        else:
            # add the source to the dict
            self.sources[source] = {"id" : id, "url" : url, "modified_date" : modified_date, "data" : data}
        return True
    
    
    def update_source_date(self, source, modified_date):
        if source in self.sources:
            self.sources[source]["modified_date"] = modified_date
            return True
        else:
            return False
        
    ## Version Managment
    # ad a new version to the mod
    def add_version(self, game_version, source, id, version_id, url, filename, upload_date):
        if game_version in self.versions:
            if source in self.versions[game_version]["sources"]:
                return False
            else:
                # add the source to the dict
                self.versions[game_version]["sources"][source] = {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}
        else:
            self.versions[game_version] = {"sources" : {source: {"id" : id, "version_id" : version_id, "url" : url, "filename" : filename, "upload_date" : upload_date}}}
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


    