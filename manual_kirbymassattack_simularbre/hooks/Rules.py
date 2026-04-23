from typing import Optional
from worlds.AutoWorld import World
from .. import location_table
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

def medalRequirement(world: World, state: CollectionState, player: int):
    total_locations = 0
    if world.options.Include_Green_Grounds.value == 1:
        for location in location_table:
            if "Green Grounds" in location["region"]:
                total_locations += 1

    if world.options.Include_Sandy_Canyon.value == 1:
        for location in location_table:
            if "Sandy Canyon" in location["region"]:
                total_locations += 1

    if world.options.Include_Dedede_Resort.value == 1:
        for location in location_table:
            if "Dedede Resort" in location["region"]:
                total_locations += 1

    if world.options.Include_Volcano_Valley.value == 1:
        for location in location_table:
            if "Volcano Valley" in location["region"]:
                total_locations += 1

    amount_progression = 0
    id_Rainbow_Medal = -1
    for i in range(len(world.item_table)):
        if world.item_table[i]["name"] == "Rainbow Medal":
            id_Rainbow_Medal = i
        elif world.item_table[i]["progression"] == True:
            amount_progression += int(world.item_table[i]["count"])
    world.item_table[id_Rainbow_Medal]["count"] = min(total_locations - amount_progression,
                                                     world.options.Amount_of_Rainbow_Medals.value)

    return f"|Rainbow Medal:{int(world.item_table[id_Rainbow_Medal]["count"]*world.options.Rainbow_Medals_required/100)}|"