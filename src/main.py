# Import modules and packages:

# modules
from .gui import gui
from .manager import application_manager
from . import utils
from .config import config

# packages
import sys



# Main function:
def main():
    # Initializion code 

    # Create an instance of the GUI 
    app = gui.Application()

    # Create an instance of the Download Manager
    manager = application_manager.ApplicationManager()

    app.set_application_manager(manager)

    # Start the GUI
    app.run()

if __name__ == "__main__":
    main()