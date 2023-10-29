# import modrinth api for testing purposes
from source.api import m_api


if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    versions = sys.argv[2].split(',')
    loader = sys.argv[3].split(',')
    print(m_api.search_mod(name, versions, loader))