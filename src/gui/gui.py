import eel
import os

from ..manager.application_manager import ApplicationManager

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
        self.eel.expose(self.search_project)
        self.eel.start(self.html_file, size=(500, 500), mode='firefox', close_callback=self.close_callback)

    def search_project(self, name):
        #self.eel.prompt_alerts("Searching for project: " + name)
        return self.manager.search_project(name)