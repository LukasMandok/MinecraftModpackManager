# Import modules and packages:

# modules
from .gui.backend import app
from .manager import application_manager
from . import utils
from .config import config

# packages
import sys



# Main function:
def main():
    # Initializion code 

    # Create an instance of the GUI 
    backend = app.Backend()

    # Create an instance of the Application Manager
    manager = application_manager.ApplicationManager(backend)

    backend.set_application_manager(manager)

    # Start the GUI
    print("Executing run function of gui:")
    backend.init_routes()
    backend.run()
    # backend.test_websocket()

if __name__ == "__main__":
    main()