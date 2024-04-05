# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import WebWorld
from typing import Optional
from BaseClasses import Tutorial
from ..Data import game_table

# Nothing in the world.py hook is executed by the webhost so any logic you want to do need to be done here

# Return a string containing a custom world description
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#docstrings
def hook_set_world_description(base_doc: str) -> str:
    return base_doc


# this hooks allows you to modify the Webworld that get shown on the WebHost when hosted locally
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def hook_set_world_webworld(web: WebWorld) -> WebWorld:
    return web