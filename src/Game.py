from .Data import game_table

game_name: str = "Manual_%s_%s" % (game_table["game"], game_table["creator"])
filler_item_name: str = game_table["filler_item_name"] if "filler_item_name" in game_table else "Filler"
glitches_item_name: str | None = game_table["glitches_item_name"] if "glitches_item_name" in game_table else None
starting_items: list[dict]|None = game_table["starting_items"] if "starting_items" in game_table else None

if "starting_index" in game_table:
    try:
        starting_index = int(game_table["starting_index"])
    except ValueError:
        raise Exception("The value of data/game.json:'starting_index' should be an int")
else:
    starting_index = 1
