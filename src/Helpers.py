from BaseClasses import MultiWorld
from .Data import category_table
from .Items import ManualItem
from .Locations import ManualLocation
from .hooks.Helpers import before_is_category_enabled, before_is_item_enabled, before_is_location_enabled

from typing import Union

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world.worlds[player].options, name, None)
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

def is_category_enabled(world: MultiWorld, player: int, category_name: str) -> bool:
    """Check if a category has been disabled by a yaml option."""
    hook_result = before_is_category_enabled(world, player, category_name)
    if hook_result is not None:
        return hook_result

    category_data = category_table.get(category_name, {})
    if "yaml_option" in category_data:
        for option_name in category_data["yaml_option"]:
            required = True
            if option_name.startswith("!"):
                option_name = option_name[1:]
                required = False

            if is_option_enabled(world, player, option_name) != required:
                return False
    return True

def is_item_name_enabled(world: MultiWorld, player: int, item_name: str) -> bool:
    """Check if an item named 'item_name' has been disabled by a yaml option."""
    item = world.worlds[player].item_name_to_item.get(item_name, {})
    if not item:
        return False

    return is_item_enabled(world, player, item)

def is_item_enabled(world: MultiWorld, player: int, item: ManualItem) -> bool:
    """Check if an item has been disabled by a yaml option."""
    hook_result = before_is_item_enabled(world, player, item)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(world, player, item)

def is_location_name_enabled(world: MultiWorld, player: int, location_name: str) -> bool:
    """Check if a location named 'location_name' has been disabled by a yaml option."""
    location = world.worlds[player].location_name_to_location.get(location_name, {})
    if not location:
        return False

    return is_location_enabled(world, player, location)

def is_location_enabled(world: MultiWorld, player: int, location: ManualLocation) -> bool:
    """Check if a location has been disabled by a yaml option."""
    hook_result = before_is_location_enabled(world, player, location)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(world, player, location)

def _is_manualobject_enabled(world: MultiWorld, player: int, object: any) -> bool:
    """Internal method: Check if a Manual Object has any category disabled by a yaml option.
    \nPlease use the proper is_'item/location'_enabled or is_'item/location'_name_enabled methods instead.
    """
    enabled = True
    for category in object.get("category", []):
        if not is_category_enabled(world, player, category):
            enabled = False
            break

    return enabled