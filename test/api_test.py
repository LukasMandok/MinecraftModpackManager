# import modrinth api for testing purposes
from src.manager import application_manager
from src import utils

from src.models.formats import GameVersion


if __name__ == '__main__':
    # test_score = utils.custom_scorer("the aether", "the Aether II")
    # print("testscore: ", test_score)
    
    manager = application_manager.ApplicationManager()
    # CTOV - Farmer's Delight Compat
    shared_mod = manager.apiManager.find_shared_mod("Terralith") #ChoiceTheorems Overhauled Villages
    print("shared_mod", shared_mod)
    
    # version = GameVersion("1.19.4")
    # dict = {version : "test"}
    # print(dict["1.19.4"])
    # print("version1: ", "1.19.4" == version)
    # print("version2: ", version == "1.19.4")
    
    # print("comparison 1: ", utils.strict_scorer("CTOV - Farmer Delight Compat", "CTOV - Farmer Delight Compatibility pack"))
    # print("comparison 2: ", utils.strict_scorer("Terralith", "Terralith - Villager Compar"))
    # print("comparison 3: ", utils.strict_scorer("Farmers Delight", "Farmers Delight [Fabric]"))
    