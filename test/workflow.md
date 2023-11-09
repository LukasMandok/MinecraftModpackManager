# TODOs:

- Make Mods active / inactive in mods 
- Put functions in Project / Mod into ProjectManager (mostly)
- Make a download List from Project-Cards in HTML
- Show which mods are available on which mod loader and which version
- make the version and mod loader selectable -> non available mods are grey

# Workflows

- everything that is done, needs to be updated in mods data
<br>-> need functions in ApplicationManager that initiates all the stuff in other Managers

## 1. Retrieve Data from Download List
- No data saved anywhere else:
- -> Need to fill complete mod-list 

1. Read mod download list (dict, list):
   <br>GUI -> ApplicationManager -> DataManager (done) -> GUI (make mods selectable - select all button)

2. Import Selected Mods:
    - Search Mod one by one on both websites
    <br> ApplicationManager -> ApiManager (create SourceProjectInfo object)

    - If found create Project object and add it to ModList
    <br> ApplicationManager -> DataManager -> ProjectManager -> ProjectModMod 