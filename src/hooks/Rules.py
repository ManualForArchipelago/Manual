from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with (function_name()}.
def overfishedAnywhere(world: World, mw: MultiWorld, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(world: World, mw: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee(world: World, mw: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

# Two useful functions to make require work if an item is disabled instead of making it inaccessible
# OptOne check if the passed item (with or without ||) is enabled, then return |item:count| where count is clamped to the maximum number of said item
def OptOne(base: World, world: MultiWorld, state: CollectionState, player: int, item: str, items_counts: Optional[dict] = None):
    """Returns item with count adjusted to Real Item Count"""
    if item == "":
        return "" #Skip this function if item is left blank
    if not items_counts:
        items_counts = base.get_item_counts()

    require_type = 'item'

    if '@' in item[:2]:
        require_type = 'category'

    item = item.lstrip('|@$').rstrip('|')

    item_parts = item.split(":")
    item_name = item
    item_count = 1

    if len(item_parts) > 1:
        item_name = item_parts[0]
        item_count = item_parts[1]

    if require_type == 'category':
        if isinstance(item_count, int):
            #Only loop if we can use the result to clamp
            category_items = [item for item in base.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
            item_count = clamp(item_count, 0, category_items_counts)
        return f"|@{item_name}:{item_count}|"
    elif require_type == 'item':
        if isinstance(item_count, int):
            item_current_count = items_counts.get(item_name, 0)
            item_count = clamp(item_count, 0, item_current_count)
        return f"|{item_name}:{item_count}|"

# OptAll check the passed require string and loop every item to check if they're enabled,
# then returns the require string with counts ajusted using OptOne
def OptAll(base: World, world: MultiWorld, state: CollectionState, player: int, requires: str):
    """Returns an entire require string with counts adjusted to Real Item Count"""
    requires_list = requires

    items_counts = base.get_item_counts()

    functions = {}
    if requires_list == "":
        return True
    for item in re.findall(r'\{(\w+)\(([^)]*)\)\}', requires_list):
        #so this function doesnt try to get item from other functions, in theory.
        func_name = item[0]
        functions[func_name] = item[1]
        requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", "{" + func_name + "(temp)}")
    # parse user written statement into list of each item
    for item in re.findall(r'\|[^|]+\|', requires):
        itemScanned = OptOne(base, world, state, player, item, items_counts)
        requires_list = requires_list.replace(item, itemScanned)

    for function in functions:
        requires_list = requires_list.replace("{" + function + "(temp)}", "{" + func_name + "(" + functions[func_name] + ")}")
    return requires_list

