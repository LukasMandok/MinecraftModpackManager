import webview
import os

from ..manager.application_manager import ApplicationManager

class Application:
    def __init__(self):
        self.manager = None

        self.html_file = os.path.join(os.path.dirname(__file__), 'webpage', 'index.html')
        #self.js_file = os.path.join(os.path.dirname(__file__), 'webpage', 'index.js')

        with open(self.html_file, 'r') as f:
            self.html = f.read()
        
        #with open(self.js_file, 'r') as f:
        #    self.js = f.read()

    def set_application_manager(self, manager):
        self.manager = manager

    def run(self):

        js_api = (self.manager, {'search_project': self.manager.search_project})

        webview.create_window("Hello world", html=self.html, js_api=js_api)
        webview.start()