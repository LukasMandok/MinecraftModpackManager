import json
import os

from ..config import config

# Create a Class for the DataManager that contains the functinos above:
class DataManager:
    def __init__(self, fileManager):
        self.data = None
        self.fileManager = fileManager

    ### public functions

    def get_projects(self, type):
        return self.data[type]

    def get_project(self, type, id):
        return self.get_projects(type)[id]


    def find_project(self, type, name):
        return next((project for project in self.data[type] if project['name'] == name), None)

    def add_project(self, type, project):
        id = project.getID()
        self.data[type].append()
        self._save_mod_list()

    # mod specific funtions

    def get_mods(self):
        return self.get_projects("mods")

    def get_mod(self, id):
        return self.get_project("mods", id)


    def find_mod(self, name):
        return self.find_project("mods", name)

    def add_mod(self, mod):
        self.add_project("mods", mod)
