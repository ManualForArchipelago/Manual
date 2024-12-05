import csv
import os
import pkgutil
import json

from BaseClasses import MultiWorld, Item
from typing import Optional, List, TYPE_CHECKING
from worlds.AutoWorld import World
from .hooks.Helpers import before_is_category_enabled, before_is_item_enabled, before_is_location_enabled

from typing import Union

if TYPE_CHECKING:
    from .Items import ManualItem
    from .Locations import ManualLocation

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

def load_data_csv(*args) -> list[dict]:
    fname = os.path.join("data", *args)

    try:
        lines = pkgutil.get_data(__name__, fname).decode().splitlines()
    except:
        lines = []
    filedata = list(csv.DictReader(lines))

    return filedata

def is_option_enabled(multiworld: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(multiworld, player, name) > 0

def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(multiworld.worlds[player].options, name, None)
    if option is None:
        return 0

    return option.value

def clamp(value, min, max):
    """Returns value clamped to the inclusive range of min and max"""
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

def is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> bool:
    from .Data import category_table
    """Check if a category has been disabled by a yaml option."""
    hook_result = before_is_category_enabled(multiworld, player, category_name)
    if hook_result is not None:
        return hook_result

    category_data = category_table.get(category_name, {})
    return resolve_yaml_option(multiworld, player, category_data)

def resolve_yaml_option(multiworld: MultiWorld, player: int, data: dict) -> bool:
    if "yaml_option" in data:
        for option_name in data["yaml_option"]:
            required = True
            if option_name.startswith("!"):
                option_name = option_name[1:]
                required = False

            if is_option_enabled(multiworld, player, option_name) != required:
                return False
    return True

def is_item_name_enabled(multiworld: MultiWorld, player: int, item_name: str) -> bool:
    """Check if an item named 'item_name' has been disabled by a yaml option."""
    item = multiworld.worlds[player].item_name_to_item.get(item_name, {})
    if not item:
        return False

    return is_item_enabled(multiworld, player, item)

def is_item_enabled(multiworld: MultiWorld, player: int, item: "ManualItem") -> bool:
    """Check if an item has been disabled by a yaml option."""
    hook_result = before_is_item_enabled(multiworld, player, item)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(multiworld, player, item)

def is_location_name_enabled(multiworld: MultiWorld, player: int, location_name: str) -> bool:
    """Check if a location named 'location_name' has been disabled by a yaml option."""
    location = multiworld.worlds[player].location_name_to_location.get(location_name, {})
    if not location:
        return False

    return is_location_enabled(multiworld, player, location)

def is_location_enabled(multiworld: MultiWorld, player: int, location: "ManualLocation") -> bool:
    """Check if a location has been disabled by a yaml option."""
    hook_result = before_is_location_enabled(multiworld, player, location)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(multiworld, player, location)

def _is_manualobject_enabled(multiworld: MultiWorld, player: int, object: any) -> bool:
    """Internal method: Check if a Manual Object has any category disabled by a yaml option.
    \nPlease use the proper is_'item/location'_enabled or is_'item/location'_name_enabled methods instead.
    """
    enabled = True
    for category in object.get("category", []):
        if not is_category_enabled(multiworld, player, category):
            enabled = False
            break

    return enabled

def get_items_for_player(multiworld: MultiWorld, player: int, includePrecollected: bool = False) -> List[Item]:
    """Return list of items of a player including placed items"""
    items = [i for i in multiworld.get_items() if i.player == player]
    if includePrecollected:
        items.extend(multiworld.precollected_items.get(player, []))
    return items

def reset_specific_item_value_cache_for_player(world: World, value: str, player: Optional[int] = None) -> dict[str, int]:
    if player is None:
        player = world.player
    return world.item_values[player].pop(value, {})

def reset_item_value_cache_for_player(world: World, player: Optional[int] = None):
    if player is None:
        player = world.player
    world.item_values[player] = {}

def get_items_with_value(world: World, multiworld: MultiWorld, value: str, player: Optional[int] = None, skipCache: bool = False) -> dict[str, int]:
    """Return a dict of every items with a specific value type present in their respective 'value' dict\n
    Output in the format 'Item Name': 'value count'\n
    Keep a cache of the result, it can be skipped with 'skipCache == True'\n
    To force a Reset of the player's cache of a value use either reset_specific_item_value_cache_for_player or reset_item_value_cache_for_player
    """
    if player is None:
        player = world.player

    player_items = get_items_for_player(multiworld, player, True)
    # Just a small check to prevent caching {} if items don't exist yet
    if not player_items:
        return {value: -1}

    value = value.lower().strip()

    if not skipCache:
        if not hasattr(world, 'item_values'): #Cache of just the item values
            world.item_values = {}

        if not world.item_values.get(player):
            world.item_values[player] = {}

    if value not in world.item_values.get(player, {}).keys() or skipCache:
        item_with_values = {i.name: world.item_name_to_item[i.name]['value'].get(value, 0)
                            for i in player_items if i.code is not None
                            and i.name in world.item_name_groups.get(f'has_{value}_value', [])}
        if skipCache:
            return item_with_values
        world.item_values[player][value] = item_with_values
    return world.item_values[player].get(value)


def filter_used_regions(player_regions: dict|list) -> set:
    """Return a set of regions that are actually used in Generation. It includes region that have no locations but are required by other regions\n
    The dict version of the player_regions must be in the format: dict(region name str: region)
    """
    used_regions = set()

    if isinstance(player_regions, list):
        player_regions = {r.name: r for r in player_regions}

    #Grab all the player's regions and take note of those with locations
    for region in player_regions.values():
        if region.locations:
            used_regions.add(region)

    #Check every known region with location for parent regions
    checked_parent = []
    for region in set(used_regions):
        def checkParent(parent_region):
            if parent_region.name in checked_parent: #dont check a region twice
                return
            checked_parent.append(parent_region.name)
            used_regions.add(parent_region)
            for entrance in parent_region.entrances:
                if player_regions.get(entrance.parent_region.name):
                    checkParent(entrance.parent_region)
            return
        checkParent(region)
    return used_regions

def convert_to_long_string(input: str | list[str]) -> str:
    """Verify that the input is a str. If it's a list[str] then it combine them into a str in a way that works with yaml template/website options descriptions"""
    if not isinstance(input, str):
        return str.join("\n    ", input)
    return input
