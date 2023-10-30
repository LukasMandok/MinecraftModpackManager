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