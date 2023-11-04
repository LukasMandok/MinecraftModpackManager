# import modrinth api for testing purposes
from src.manager import application_manager
from src import utils

from src.models.formats import GameVersion


if __name__ == '__main__':
    # test_score = utils.custom_scorer("the aether", "the Aether II")
    # print("testscore: ", test_score)
    
    manager = application_manager.ApplicationManager()
    score = manager.apiManager.retrieve_mod("Lihium")
    print("comparison score", score)
    
    # version = GameVersion("1.19.4")
    # dict = {version : "test"}
    # print(dict["1.19.4"])
    # print("version1: ", "1.19.4" == version)
    # print("version2: ", version == "1.19.4")
    