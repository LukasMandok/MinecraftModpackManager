import json
import os
# import asyncio

from aiotinydb import AIOTinyDB
from aiotinydb.storage import AIOJSONStorage

from aiotinydb.middleware import CachingMiddleware

from ..config import config 

class DatabaseManager:
    database_file = config.database_file
    download_list_file = config.download_list_file

    def __init__(self, db, mods):

        self.db = db
        self.mods = mods
        
        # self.download_db = TinyDB(storage=MemoryStorage)
        # self.downloaded     = self.db.table('downloaded')
        # self.download_list  = self.db.table('download_list')    
    
    # asynchronously factory method
    @classmethod
    async def create(cls):
        db, mods = await cls._create_database()
        return cls(db, mods)
    
    @classmethod
    async def _create_database(cls):
        async with AIOTinyDB(cls.database_file, storage=CachingMiddleware(AIOJSONStorage)) as db:
            mods = db.table('mods')
            return db, mods
    
    ### public methods
        
    # Json Mod List
    # def load_mod_list(self):
    #     # create the database if it doesn't exist
    #     if not os.path.exists(self.mod_list_file):
    #         with open(self.mod_list_file, 'w') as f:
    #             json.dump({"mods": {}}, f)

    #     try:
    #         with open(self.mod_list_file, 'r') as f:
    #             data = json.load(f)
    #     except json.JSONDecodeError:
    #         # the file is corrupt, so we'll just start fresh
    #         data = {"mods": {}}
        
    #     return data


    # def save_mod_list(self, data):
    #     with open(self.mod_list_file, 'w') as f:
    #         json.dump(data, f)
    #         f.flush()
    #         os.fsync(f.fileno())
            
    @property
    def database(self):
        return self.db

    # Txt download List
    def save_download_list(self, iterator):
        # define generator to create lines from iterator:
        lines = (self._generate_download_file_line(level, name, comment) for level, name, comment in iterator)
        try:
            with open(self.download_list_file, 'w') as file:
                file.writelines(lines)
        except Exception as e:
            print(f'Error saving download list: {e}')
        
            
    def load_download_list(self):
        try:
            with open(self.download_list_file, 'r') as file:
                yield from self._parse_download_file(file)
        except OSError as error:
            print(f'Error: {error}')
            exit(1)
    
    
    ### private methods
    
    @staticmethod
    def _parse_download_file(file):    
        current_categories = []
        indentation = 0
        mod = None
        intendation_steps = None
        comment = None
        scope = None
        next_scope = None
        
        def parse_lines(lines):
            nonlocal next_scope
            for line in lines:
                # remove trailing whitespace
                line = line.rstrip()
                # get the indentation
                indentation = len(line) - len(line.lstrip())
                # remove whitespace from the line also on the left
                line = line.strip()
                
                # ignore comments and empty lines
                if line.startswith("#") or not line:
                    continue

                # ignore comment part of not-empty lines and strip again
                line, *comment = line.split("#", 1)
                line = line.strip()
                comment = comment[0].strip() if comment else None

                if line.startswith("[") and line.endswith("]"): 
                    next_scope = line[1:-1].lower()
                    continue

                yield line, indentation, comment
            
        for next_mod, next_indentation, next_comment in parse_lines(file):
            
            # calculate intendation difference to previous line and normalize to 1
            diff = next_indentation - indentation
            if intendation_steps is None:
                if diff > 0:
                    intendation_steps = diff
            else:
                diff //= intendation_steps
                
            if mod:
                if diff > 0:
                    # previous line was a category
                    current_categories.append(mod)
                    
                elif diff < 0:
                    # prvious line was a mod
                    yield mod, current_categories, scope, comment
                    # remove |diff| number of categories
                    current_categories = current_categories[:diff]
                    
                elif diff == 0:
                    # yield mod info
                    yield mod, current_categories, scope, comment
                    
            mod = next_mod
            indentation = next_indentation
            comment = next_comment
            scope = next_scope
            
        # Process the last line of the file
        if mod:
            yield mod, current_categories, scope, next_comment
            
    
    
    @staticmethod
    def _generate_download_file_line(level, name, comment):        
        def get_spaces(intendation):
            return " " * intendation * 4
        
        line = get_spaces(level) + name
        if comment:
            line += " # " + comment
            
        line += "\n"

        return line