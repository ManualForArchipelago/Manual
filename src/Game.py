from argparse import Namespace


def parse_gamedata(ret: Namespace):
    if 'creator' in ret.game_table:
        ret.game_table['player'] = ret.game_table['creator']

    ret.game_name = "Manual_%s_%s" % (ret.game_table["game"], ret.game_table["player"])
    ret.filler_item_name = ret.game_table["filler_item_name"] if "filler_item_name" in ret.game_table else "Filler"
    ret.starting_items = ret.game_table["starting_items"] if "starting_items" in ret.game_table else None

    if "starting_index" in ret.game_table:
        try:
            ret.starting_index = int(ret.game_table["starting_index"])
        except ValueError:
            raise Exception("The value of data/game.json:'starting_index' should be an int")
    else:
        ret.starting_index = 1
