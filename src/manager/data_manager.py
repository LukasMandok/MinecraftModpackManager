import json
import os

from .. import config

# Create a Class for the DataManager that contains the functinos above:
class DataManager:
    def __init__(self):
        self.file_path = config.load_config()["mod_list_file"]
        self.data = None

        self._load_data()

    # private functions

    def _load_data(self):
        # create the file if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"mods": {}}, f)


        with open(self.file_path, 'r') as f:
            self.data = json.load(f)
        

    def _save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)


    # public functions

    def get_projects(self, type):
        return self.data[type]

    def get_project(self, type, id):
        return self.get_projects(type)[id]


    def find_project(self, type, name):
        return next((project for project in self.data[type] if project['name'] == name), None)

    def add_project(self, type, project):
        id = project.getID()
        self.data[type].append()
        self._save_data()

    # mod specific funtions

    def get_mods(self):
        return self.get_projects("mods")

    def get_mod(self, id):
        return self.get_project("mods", id)


    def find_mod(self, name):
        return self.find_project("mods", name)

    def add_mod(self, mod):
        self.add_project("mods", mod)
