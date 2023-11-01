from typing import overload
import eel
import os

from ..types.constants import Sources

class Application:
    def __init__(self):
        # print("Initializing GUI... with object: " + str(self))
        self.manager = None

        self.html_dir  = os.path.dirname(__file__)
        self.html_file = os.path.join(self.html_dir, 'webpage', 'index.html')

        self.eel = eel

    def set_application_manager(self, manager):
        self.manager = manager

    def close_callback(self, websockets, *args):
        if websockets == []:
            print('Exiting application!')
            exit()


    def run(self):

        # Ensure the manager is set before starting.
        if self.manager is None:
            raise ValueError("Manager not set!")

        self.eel.init(self.html_dir)
        self.eel.expose(self.search_mod)
        self.eel.start(self.html_file, size=(500, 500), mode='firefox', close_callback=self.close_callback)
    
    # @overload
    # def search_mod(self, name: str):
    #     #self.eel.prompt_alerts("Searching for project: " + name)
    #     return self.manager.search_mod(name)
    
    # @overload
    def search_mod(self, name: str, source: str):
        
        source_enum = Sources.get_valid_source(source)   
        if source_enum is None:
            raise ValueError("Invalid source: " + source)     
        
        return self.manager.search_mod(name, source = source_enum)
    