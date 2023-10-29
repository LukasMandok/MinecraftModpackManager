from setuptools import setup, find_packages

setup(
    name="MinecraftModpackManager",
    version="0.1.0",
    author="DevilsThumb",
    author_email="MrDevilsThumb@gmail.com",
    description="A Python CLI and GUI for downloading and managing mods from CurseForge and Modrinth into subfolders for modpack creation",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LukasMandok/MinecraftModpackManager",
    packages=find_packages(exclude=["tests*"]), #['minecraft_mod_manager', *find_packages(exclude=["tests*"])],
    entry_points={
        'console_scripts': [
            'minecraft-mod-manager = source.main:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        # Add other dependencies here
    ],
)