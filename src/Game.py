from .Data import game_table
from .hooks.Docs import hook_set_world_description, hook_set_world_webworld
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

if 'creator' in game_table:
    game_table['player'] = game_table['creator']

game_name = "Manual_%s_%s" % (game_table["game"], game_table["player"])
filler_item_name = game_table["filler_item_name"] if "filler_item_name" in game_table else "Filler"
starting_items = game_table["starting_items"] if "starting_items" in game_table else None

# Programmatically generate starting indexes for items and locations based upon the game name and player name to aim for non-colliding indexes
# Additionally, make this use as many characters of the game name as possible to avoid accidental id pool collisions
# - It's assumed that the first two characters of a game and the last character *should* be fairly unique, but we use the remaining characters anyways to move the pool
# - The player name is meant to be a small differentiator, so we just apply a flat multiplier for that

# 100m + 70m + 10m, which should put all Manual games comfortably in the billions
starting_index = (ord(game_table["game"][:1]) * 100000000) + \
    (ord(game_table["game"][1:2]) * 70000000) + \
    (ord(game_table["game"][-1:]) * 10000000)

if len(game_table["game"]) > 3:
    for index in range(2, len(game_table["game"]) - 1):
        multiplier = 100000

        starting_index += (ord(game_table["game"][index:index+1]) * multiplier)

for index in range(0, len(game_table["player"])):
    starting_index += (ord(game_table["player"][index:index+1]) * 1000)

def set_world_doc(base_doc: str):
    if game_table.get("documentation", {}).get("apworld_description", ""):
        base_doc = game_table["documentation"]["apworld_description"]
    return hook_set_world_description(base_doc)

def set_world_webworld(web: WebWorld) -> WebWorld:
    if game_table.get("documentation", {}).get("web", {}):
        Web_Config = game_table["documentation"]["web"]

        web.theme = Web_Config.get("theme", web.theme)
        web.game_info_languages = Web_Config.get("game_info_languages", web.game_info_languages)
        web.options_presets = Web_Config.get("options_presets", web.options_presets)
        web.options_page = Web_Config.get("options_page", web.options_page)
        web.bug_report_page = Web_Config.get("bug_report_page", web.bug_report_page)

        if Web_Config.get("tutorials", []):
            tutorials = []
            for tutorial in Web_Config.get("tutorials", []):
                tutorials.append(Tutorial(
                    tutorial.get("name", "Multiworld Setup Guide"),
                    tutorial.get("description", "A guide to setting up manual game integration for Archipelago multiworld games."),
                    tutorial.get("language", "English"),
                    tutorial.get("file_name", "setup_en.md"),
                    tutorial.get("link", "setup/en"),
                    tutorial.get("authors", [game_table.get("creator", game_table.get("player", "Unknown"))])
                ))
            web.tutorials = tutorials
    return hook_set_world_webworld(web)