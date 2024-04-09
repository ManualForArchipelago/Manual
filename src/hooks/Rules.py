from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

def ItemValue(world: World, multiworld: MultiWorld, state: CollectionState, player: int, args: str):
    """Has the player reached a certain number of X value"""

    args_list = args.split(":")

    if not len(args_list) == 2 or not args_list[1].isnumeric():
        raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({args_list[0]}:12)'")
    args_list[1] = int(args_list[1])

    if not hasattr(world, 'custom_item_values'):
        #im making a cache so the future loops are not triggered every time
        world.custom_item_values = {}

    state_player = f"{player}_state"
    current_player = f"{player}_current"
    if not world.custom_item_values.get(state_player, {}): # First Time
        world.custom_item_values[state_player] = {}
        world.custom_item_values[current_player] = {}

    if args_list[0] not in world.custom_item_values.get(current_player, {}).keys() or world.custom_item_values[state_player] != dict(state.prog_items[player]):
        #First Time or if state changed since last check
        existing_item_values = _GetItemsWithValue(world, multiworld, args_list[0])
        total_Count = 0
        for name, value in existing_item_values.items():
            count = state.count(name, player)
            if count > 0:
                total_Count += count * value
        world.custom_item_values[current_player][args_list[0]] = total_Count
        world.custom_item_values[state_player] = dict(state.prog_items[player]) #save the current gotten items to check later if its the same
    return world.custom_item_values[current_player][args_list[0]] >= args_list[1]

def _GetItemsWithValue(world: World, multiworld: MultiWorld, items_value_to_get: str, player: Optional[int] = None, force: bool = False) -> dict[str, int]:
    if player is None:
        player = world.player

    if not hasattr(world, 'custom_item_values'):
        #I left a Copy here of the check if you decide to call _GetItemsWithValue before ItemValue
        world.custom_item_values = {}

    if not world.custom_item_values.get(player):
        world.custom_item_values[player] = {}

    if items_value_to_get not in world.custom_item_values.get(player, {}).keys() or force:
        real_pool = multiworld.get_items()
        item_with_values = {i.name: world.item_name_to_item[i.name]['value'].get(items_value_to_get)
                            for i in real_pool if i.player == player and i.code is not None
                            and world.item_name_to_item.get(i.name, {}).get('value', {}).get(items_value_to_get)}
        world.custom_item_values[player][items_value_to_get] = item_with_values
    return world.custom_item_values[player].get(items_value_to_get)

# Two useful functions to make require work if an item is disabled instead of making it inaccessible
# OptOne check if the passed item (with or without ||) is enabled, then return |item:count| where count is clamped to the maximum number of said item
# Eg. requires: "{OptOne(|ItemThatMightBeDisabled|)} and |other items|"
# become this if the item is disabled -> "|ItemThatMightBeDisabled:0| and |other items|"
def OptOne(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str, items_counts: Optional[dict] = None):
    """Returns item with count adjusted to Real Item Count"""
    if item == "":
        return "" #Skip this function if item is left blank
    if not items_counts:
        items_counts = world.get_item_counts()

    require_type = 'item'

    if '@' in item[:2]:
        require_type = 'category'

    item = item.lstrip('|@$').rstrip('|')

    item_parts = item.split(":")
    item_name = item
    item_count = '1'

    if len(item_parts) > 1:
        item_name = item_parts[0]
        item_count = item_parts[1]

    if require_type == 'category':
        if item_count.isnumeric():
            #Only loop if we can use the result to clamp
            category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
            item_count = clamp(int(item_count), 0, category_items_counts)
        return f"|@{item_name}:{item_count}|"
    elif require_type == 'item':
        if item_count.isnumeric():
            item_current_count = items_counts.get(item_name, 0)
            item_count = clamp(int(item_count), 0, item_current_count)
        return f"|{item_name}:{item_count}|"

# OptAll check the passed require string and loop every item to check if they're enabled,
# then returns the require string with counts ajusted using OptOne
# eg. requires: "{OptAll(|ItemThatMightBeDisabled| and |@itemCategoryWithCountThatMightBeModifedViaHook:10|)} and |other items|"
# become this if the item is disabled -> "|ItemThatMightBeDisabled:0| and |@itemCategoryWithCountThatMightBeModifedViaHook:2| and |other items|"
def OptAll(world: World, multiworld: MultiWorld, state: CollectionState, player: int, requires: str):
    """Returns an entire require string with counts adjusted to Real Item Count"""
    requires_list = requires

    items_counts = world.get_item_counts()

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
        itemScanned = OptOne(world, multiworld, state, player, item, items_counts)
        requires_list = requires_list.replace(item, itemScanned)

    for function in functions:
        requires_list = requires_list.replace("{" + function + "(temp)}", "{" + func_name + "(" + functions[func_name] + ")}")
    return requires_list

