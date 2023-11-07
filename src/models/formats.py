from .constants import *
    
### Mod Info stuff
        
class ModList(list):
    def __init__(self, mods: list = []):
        super().__init__(mods)
                
    def get_names(self):
        return [mod.name for mod in self]
        
    def to_dict(self):
        return [mod.to_dict() for mod in self]        
        
        

### GameVersion

class GameVersion:
    def __init__(self, text: str):
        self.text = text
        self.v0, self.v1, self.v2 = self._convert_to_version()
         
    def _convert_to_version(self):
        split_text = self.text.split(".")
        if (len(split_text) < 2 or len(split_text) > 3):
            raise ValueError(f"Invalid game version, needs format 'x.x' or 'x.x.x', got '{self.text}")
        
        v0, v1 = map(int, split_text[:2])
        v2 = int(split_text[2]) if len(split_text) == 3 else 0
        
        return v0, v1, v2
    
    def __hash__(self):
        return hash(self.text)
        
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return f"GameVersion('{self.text}')"
    
    # equal
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 == __value.v0 and self.v1 == __value.v1 and self.v2 == __value.v2)
        
        elif isinstance(__value, str):
            cond = (self.text == __value)
            if cond: return True
            
            # maybe this is not such a good because it will take much time to compute:
            print("compare: " + self.text + " with " + __value + " , not identical text")
            converted = self.__class__(__value)
            return self.__eq__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__} or str")
    
    def __ne__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 != __value.v0 or self.v1 != __value.v1 or self.v2 != __value.v2)

        elif isinstance(__value, str):
            cond = (self.text == __value)
            if cond: return False
            
            # maybe this is not such a good because it will take much time to compute:
            print("compare: " + self.text + " with " + __value + " , not identical text")
            converted = self.__class__(__value)
            return self.__ne__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__} or str")
        
    # greater than
    def __gt__(self, __value: object) -> bool:
        cond1 = False
        cond2 = False
        cond3 = False
        
        if isinstance(__value, type(self)):
            cond1 = (self.v0 > __value.v0)
            if cond1: return True
            
            cond2 = (self.v0 >= __value.v0 and self.v1 > __value.v1)
            if cond2: return True
            
            cond3 = (self.v0 >= __value.v0 and self.v1 >= __value.v1 and self.v2 > __value.v2)
            return cond3
        
        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__gt__(converted)      
              
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__} or str")
    
    
    # greater equal
    def __ge__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 >= __value.v0 and self.v1 >= __value.v1 and self.v2 >= __value.v2)

        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__ge__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__}")

        
    # less than
    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            cond1 = (self.v0 < __value.v0)
            if cond1: return True
            cond2 = (self.v0 <= __value.v0 and self.v1 < __value.v1)
            if cond2: return True
            cond3 = (self.v0 <= __value.v0 and self.v1 <= __value.v1 and self.v2 < __value.v2)
            if cond3: return True
        
        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__lt__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__}")

    # less equal
    def __le__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (self.v0 <= __value.v0 and self.v1 <= __value.v1 and self.v2 <= __value.v2)
        
        elif isinstance(__value, str):
            converted = self.__class__(__value)
            return self.__le__(converted)
        
        else:
            raise TypeError(f"__value must be an instance of {type(self).__name__}")


    ### Class Methods
        
    @classmethod
    def find_latest(cls, game_versions: list) -> "GameVersion":
        latest = None
        for game_version in game_versions:
            try:
                game_version = cls(game_version)
            except ValueError:
                print("GameVersion: " + game_version + " is not supported")
                continue
            if latest is None or game_version > latest:
                latest = game_version
                
        return latest