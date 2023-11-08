# import modrinth api for testing purposes
from src.manager import application_manager
from src import utils

from src.models.formats import GameVersion


if __name__ == '__main__':
    # test_score = utils.custom_scorer("the aether", "the Aether II")
    # print("testscore: ", test_score)
    
    manager = application_manager.ApplicationManager()
    # CTOV - Farmer's Delight Compat
    #shared_mod = manager.apiManager.find_shared_mod("Terralith") #ChoiceTheorems Overhauled Villages
    #print("shared_mod", shared_mod)
    
    dataManager = manager.dataManager
    
    dataManager._load_download_list_from_file()