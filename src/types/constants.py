from enum import Enum

# Type definitions
class Modloader(Enum):
    FORGE = "forge"
    FABRIC = "fabric"
    QUILT = "quilt"
    NEOFORGE = "neoforge"
    UNKNOWN = "unknown"

class Sources(Enum):
    MODRINTH = "modrinth"
    CURSEFORGE = "curseforge"
    UNKNOWN = "unknown"   
    
    @classmethod
    def get_valid_source(cls, source):
        if source in cls._value2member_map_:
            return cls(source)
        elif source in cls._value2member_map_.values():
            return source
        else:
            return None