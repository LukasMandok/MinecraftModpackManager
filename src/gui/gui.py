import eel
import asyncio
import os
import json

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

        # exposing functions to javascript
        self.eel.expose(self.get_mod_search_results)
        self.eel.expose(self.request_download_list)
        self.eel.expose(self.request_downloaded_list)
        
        self.eel.start(self.html_file, size=(500, 500), mode='firefox', close_callback=self.close_callback)
    
    ### exposed to javascript
    def get_mod_search_results(self, name: str, source: str):
        
        source_enum = Sources.get_valid_source(source)   
        if source_enum is None:
            raise ValueError("Invalid source: " + source)     
        
        search_results = self.app_manager.get_mod_search_results(name, source = source_enum)
        return search_results
    
    def request_download_list(self):
        # for execution of async function -> put in event lop:
        # asyncio.run(self.app_manager.create_download_list())
        # TODO: make this async again
        self.app_manager.create_download_list()
        
    def request_downloaded_list(self):
        # TODO: Implement
        pass
        
    ### calling functions exposed in javascript
    def send_download_list(self, download_list):
        print("converting download list to json", download_list)
        json_dict = json.dumps(download_list, default=str)
        print("sending converted download list:", json_dict)
        self.eel.receive_download_list(json_dict)
        
    def update_download_list(self, update):
        # TODO: implement
        self.eel.update_download_list(update)