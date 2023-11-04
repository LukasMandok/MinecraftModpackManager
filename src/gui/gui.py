from typing import overload
import eel
import os

from ..models.constants import Sources

class Application:
    def __init__(self):
        # print("Initializing GUI... with object: " + str(self))
        self.app_manager = None

        self.html_dir  = os.path.dirname(__file__)
        self.html_file = os.path.join(self.html_dir, 'webpage', 'index.html')

        self.eel = eel

    def set_application_manager(self, manager):
        self.app_manager = manager

    def close_callback(self, websockets, *args):
        if websockets == []:
            print('Exiting application!')
            exit()


    def run(self):

        # Ensure the manager is set before starting.
        if self.app_manager is None:
            raise ValueError("Manager not set!")

        self.eel.init(self.html_dir)
        self.eel.expose(self.get_mod_search_results)
        self.eel.start(self.html_file, size=(500, 500), mode='firefox', close_callback=self.close_callback)
    
    # @overload
    # def get_mod_search_results(self, name: str):
    #     #self.eel.prompt_alerts("Searching for project: " + name)
    #     return self.manager.get_mod_search_results(name)
    
    # @overload
    def get_mod_search_results(self, name: str, source: str):
        
        source_enum = Sources.get_valid_source(source)   
        if source_enum is None:
            raise ValueError("Invalid source: " + source)     
        
        search_results = self.app_manager.get_mod_search_results(name, source = source_enum)
        return search_results