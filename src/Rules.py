from typing import TYPE_CHECKING, Optional
from enum import IntEnum

from .Regions import regionMap
from .hooks import Rules
from .Helpers import clamp, is_item_enabled, get_items_with_value, is_option_enabled, get_option_value, convert_string_to_type, format_to_valid_identifier

from BaseClasses import MultiWorld, CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule, add_rule

import re
import math
import inspect
import logging

if TYPE_CHECKING:
    from . import ManualWorld

class LogicErrorSource(IntEnum):
    INFIX_TO_POSTFIX = 1 # includes more closing parentheses than opening (but not the opposite)
    EVALUATE_POSTFIX = 2 # includes missing pipes and missing value on either side of AND/OR
    EVALUATE_STACK_SIZE = 3 # includes missing curly brackets

def construct_logic_error(location_or_region: dict, source: LogicErrorSource) -> KeyError:
    object_type = "location/region"
    object_name = location_or_region.get("name", "Unknown")

    if location_or_region.get("is_region", False) or "starting" in location_or_region or "connects_to" in location_or_region:
        object_type = "region"
    elif "region" in location_or_region or "category" in location_or_region:
        object_type = "location"

    if source == LogicErrorSource.INFIX_TO_POSTFIX:
        source_text = "There may be mismatched parentheses, or other invalid syntax for the requires."
    elif source == LogicErrorSource.EVALUATE_POSTFIX:
        source_text = "There may be missing || around item names, or an AND/OR that is missing a value on one side, or other invalid syntax for the requires."
    elif source == LogicErrorSource.EVALUATE_STACK_SIZE:
        source_text = "There may be missing {} around requirement functions like YamlEnabled() / YamlDisabled(), or other invalid syntax for the requires."
    else:
        source_text = "This requires includes invalid syntax."

    return KeyError(f"Invalid 'requires' for {object_type} '{object_name}': {source_text} (ERROR {source})")

def infix_to_postfix(expr, location):
    prec = {"&": 2, "|": 2, "!": 3}
    stack = []
    postfix = ""

    try:
        for c in expr:
            if c.isnumeric():
                postfix += c
            elif c in prec:
                while stack and stack[-1] != "(" and prec[c] <= prec[stack[-1]]:
                    postfix += stack.pop()
                stack.append(c)
            elif c == "(":
                stack.append(c)
            elif c == ")":
                while stack and stack[-1] != "(":
                    postfix += stack.pop()
                stack.pop()

        while stack:
            postfix += stack.pop()
    except Exception:
        raise construct_logic_error(location, LogicErrorSource.INFIX_TO_POSTFIX)

    return postfix


def evaluate_postfix(expr: str, location: str) -> bool:
    stack = []

    try:
        for c in expr:
            if c == "0":
                stack.append(False)
            elif c == "1":
                stack.append(True)
            elif c == "&":
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 and op2)
            elif c == "|":
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 or op2)
            elif c == "!":
                op = stack.pop()
                stack.append(not op)
    except Exception:
        raise construct_logic_error(location, LogicErrorSource.EVALUATE_POSTFIX)

    if len(stack) != 1:
        raise construct_logic_error(location, LogicErrorSource.EVALUATE_STACK_SIZE)

    return stack.pop()

def set_rules(world: "ManualWorld", multiworld: MultiWorld, player: int):
    # this is only called when the area (think, location or region) has a "requires" field that is a string
    def checkRequireStringForArea(state: CollectionState, area: dict):
        requires_list = area["requires"]

        # Get the "real" item counts of item in the pool/placed/starting_items
        items_counts = world.get_item_counts(player)

        # Preparing some variables for exception messages
        area_type = "region" if area.get("is_region",False) else "location"
        area_name = area.get("name", f"unknown with these parameters: {area}")

        if requires_list == "":
            return True

        def findAndRecursivelyExecuteFunctions(requires_list: str, recursionDepth: int = 0) -> str:
            found_functions = re.findall(r'\{(\w+)\((.*?)\)\}', requires_list)
            if found_functions:
                if recursionDepth > world.rules_functions_maximum_recursion:
                    raise RecursionError(f'One or more functions in {area_type} "{area_name}"\'s requires looped too many time (maximum recursion is {world.rules_functions_maximum_recursion}) \
                                         \n    As of this Exception the following function(s) are waiting to run: {[f[0] for f in found_functions]} \
                                         \n    And the currently processed requires look like this: "{requires_list}"')
                else:
                    for item in found_functions:
                        func_name = item[0]
                        func_args = item[1].split(",")
                        if func_args == ['']:
                            func_args.pop()

                        func = globals().get(func_name)

                        if func is None:
                            func = getattr(Rules, func_name, None)

                        if not callable(func):
                            raise ValueError(f'Invalid function "{func_name}" in {area_type} "{area_name}".')

                        convert_req_function_args(func, func_args, area_name)
                        try:
                            result = func(world, multiworld, state, player, *func_args)
                        except Exception as ex:
                            raise RuntimeError(f'A call to the function "{func_name}" in {area_type} "{area_name}"\'s requires raised an Exception. \
                                                \nUnless it was called by another function, it should look something like "{{{func_name}({item[1]})}}" in {area_type}s.json. \
                                                \nFull error message: \
                                                \n\n{type(ex).__name__}: {ex}')
                        if isinstance(result, bool):
                            requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", "1" if result else "0")
                        else:
                            requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", str(result))

                requires_list = findAndRecursivelyExecuteFunctions(requires_list, recursionDepth + 1)
            return requires_list

        requires_list = findAndRecursivelyExecuteFunctions(requires_list)

        # parse user written statement into list of each item
        for item in re.findall(r'\|[^|]+\|', requires_list):
            require_type = 'item'

            if '|@' in item:
                require_type = 'category'

            item_base = item
            item = item.lstrip('|@$').rstrip('|')

            item_parts = item.split(":")  # type: list[str]
            item_name = item
            item_count = "1"


            if len(item_parts) > 1:
                item_name = item_parts[0].strip()
                item_count = item_parts[1].strip()

            total = 0

            if require_type == 'category':
                category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
                category_items += [event for event in world.event_name_to_event.values() if "category" in event and item_name in event["category"]]
                category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
                if item_count.lower() == 'all':
                    item_count = category_items_counts
                elif item_count.lower() == 'half':
                    item_count = int(category_items_counts / 2)
                elif item_count.endswith('%') and len(item_count) > 1:
                    percent = clamp(float(item_count[:-1]) / 100, 0, 1)
                    item_count = math.ceil(category_items_counts * percent)
                else:
                    try:
                        item_count = int(item_count)
                    except ValueError as e:
                        raise ValueError(f"Invalid item count `{item_name}` in {area}.") from e

                for category_item in category_items:
                    total += state.count(category_item["name"], player)

                    if total >= item_count:
                        requires_list = requires_list.replace(item_base, "1")
            elif require_type == 'item':
                item_current_count = items_counts.get(item_name, 0)
                if item_count.lower() == 'all':
                    item_count = item_current_count
                elif item_count.lower() == 'half':
                    item_count = int(item_current_count / 2)
                elif item_count.endswith('%') and len(item_count) > 1:
                    percent = clamp(float(item_count[:-1]) / 100, 0, 1)
                    item_count = math.ceil(item_current_count * percent)
                else:
                    item_count = int(item_count)

                total = state.count(item_name, player)

                if total >= item_count:
                    requires_list = requires_list.replace(item_base, "1")

            if total <= item_count:
                requires_list = requires_list.replace(item_base, "0")

        requires_list = re.sub(r'\s?\bAND\b\s?', '&', requires_list, 0, re.IGNORECASE)
        requires_list = re.sub(r'\s?\bOR\b\s?', '|', requires_list, 0, re.IGNORECASE)

        requires_string = infix_to_postfix("".join(requires_list), area)
        return (evaluate_postfix(requires_string, area))

    # this is only called when the area (think, location or region) has a "requires" field that is a dict
    def checkRequireDictForArea(state: CollectionState, area: dict):
        canAccess = True

        for item in area["requires"]:
            # if the require entry is an object with "or" or a list of items, treat it as a standalone require of its own
            if (isinstance(item, dict) and "or" in item and isinstance(item["or"], list)) or (isinstance(item, list)):
                canAccessOr = True
                or_items = item

                if isinstance(item, dict):
                    or_items = item["or"]

                for or_item in or_items:
                    or_item_parts = or_item.split(":")
                    or_item_name = or_item
                    or_item_count = 1

                    if len(or_item_parts) > 1:
                        or_item_name = or_item_parts[0]
                        or_item_count = int(or_item_parts[1])

                    if not state.has(or_item_name, player, or_item_count):
                        canAccessOr = False

                if canAccessOr:
                    canAccess = True
                    break
            else:
                item_parts = item.split(":")
                item_name = item
                item_count = 1

                if len(item_parts) > 1:
                    item_name = item_parts[0]
                    item_count = int(item_parts[1])

                if not state.has(item_name, player, item_count):
                    canAccess = False

        return canAccess

    # handle any type of checking needed, then ferry the check off to a dedicated method for that check
    def fullLocationOrRegionCheck(state: CollectionState, area: dict):
        # if it's not a usable object of some sort, default to true
        if not area:
            return True

        # don't require the "requires" key for locations and regions if they don't need to use it
        if "requires" not in area.keys():
            return True

        if isinstance(area["requires"], str):
            return checkRequireStringForArea(state, area)
        else:  # item access is in dict form
            return checkRequireDictForArea(state, area)

    used_location_names = []
    # Region access rules
    for region in regionMap.keys():
        used_location_names.extend([l.name for l in multiworld.get_region(region, player).locations])
        if region != "Menu":
            for exitRegion in multiworld.get_region(region, player).entrances:
                def fullRegionCheck(state: CollectionState, region=regionMap[region]):
                    return fullLocationOrRegionCheck(state, region)

                add_rule(world.get_entrance(exitRegion.name), fullRegionCheck)
            entrance_rules = regionMap[region].get("entrance_requires", {})
            for e in entrance_rules:
                entrance = world.get_entrance(f'{e}To{region}')
                add_rule(entrance, lambda state, rule={"requires": entrance_rules[e]}: fullLocationOrRegionCheck(state, rule))
            exit_rules = regionMap[region].get("exit_requires", {})
            for e in exit_rules:
                exit = world.get_entrance(f'{region}To{e}')
                add_rule(exit, lambda state, rule={"requires": exit_rules[e]}: fullLocationOrRegionCheck(state, rule))

    # Location access rules
    for location in world.location_table:
        if location["name"] not in used_location_names:
            continue

        locFromWorld = multiworld.get_location(location["name"], player)

        locationRegion = regionMap[location["region"]] if "region" in location else None

        if locationRegion:
            locationRegion['name'] = location['region']
            locationRegion['is_region'] = True

        if "requires" in location: # Location has requires, check them alongside the region requires
            def checkBothLocationAndRegion(state: CollectionState, location=location, region=locationRegion):
                locationCheck = fullLocationOrRegionCheck(state, location)
                regionCheck = True # default to true unless there's a region with requires

                if region:
                    regionCheck = fullLocationOrRegionCheck(state, region)

                return locationCheck and regionCheck

            set_rule(locFromWorld, checkBothLocationAndRegion)
        elif "region" in location: # Only region access required, check the location's region's requires
            def fullRegionCheck(state, region=locationRegion):
                return fullLocationOrRegionCheck(state, region)

            set_rule(locFromWorld, fullRegionCheck)
        else: # No location region and no location requires? It's accessible.
            def allRegionsAccessible(state):
                return True

            set_rule(locFromWorld, allRegionsAccessible)

    # Event access rules
    for name, event in world.event_name_to_event.items():
        locFromWorld = multiworld.get_location(name, player)
        locationRegion = regionMap[event["region"]] if "region" in event else None

        if locationRegion:
            locationRegion['name'] = event['region']
            locationRegion['is_region'] = True

        if "requires" in event: # Event has requires, check them alongside the region requires
            def checkBothLocationAndRegion(state: CollectionState, location=event, region=locationRegion):
                locationCheck = fullLocationOrRegionCheck(state, event)
                regionCheck = True # default to true unless there's a region with requires

                if region:
                    regionCheck = fullLocationOrRegionCheck(state, region)

                return locationCheck and regionCheck

            set_rule(locFromWorld, checkBothLocationAndRegion)
        elif "region" in event: # Only region access required, check the location's region's requires
            def fullRegionCheck(state, region=locationRegion):
                return fullLocationOrRegionCheck(state, region)

            set_rule(locFromWorld, fullRegionCheck)
        else: # No location region and no location requires? It's accessible.
            def allRegionsAccessible(state):
                return True

            set_rule(locFromWorld, allRegionsAccessible)

    # Victory requirement
    multiworld.completion_condition[player] = lambda state: state.has("__Victory__", player)

    def convert_req_function_args(func, args: list[str], areaName: str):
        parameters = inspect.signature(func).parameters
        knownParameters = ["world", "multiworld", "state", "player"]
        index = -1
        for parameter in parameters.values():
            if parameter.name in knownParameters:
                continue
            index += 1
            target_type = parameter.annotation

            if index < len(args) and args[index] != "":
                value = args[index].strip()
            else:
                if parameter.default is not inspect.Parameter.empty:
                    if index < len(args):
                        args[index] = parameter.default
                    continue
                else:
                    if parameter.annotation is inspect.Parameter.empty:
                        raise Exception(f"A call of the \"{func.__name__}\" function in \"{areaName}\"'s requirement, asks for a value for its argument \"{parameter.name}\" but it's missing.")
                    else:
                        raise Exception(f"A call of the \"{func.__name__}\" function in \"{areaName}\"'s requirement, asks for a value of type {target_type} for its argument \"{parameter.name}\" but it's missing.")

            if target_type == str or parameter.annotation is inspect.Parameter.empty: #Don't convert since its already a string or if we don't know the type to convert to
                args[index] = value
                continue

            try:
                value = convert_string_to_type(value, target_type)

            except Exception as e:
                raise Exception(f"A call of the \"{func.__name__}\" function in \"{areaName}\"'s requirement, asks for a value of type {target_type}\nfor its argument \"{parameter.name}\" but its value \"{value}\" cannot be converted to {target_type} \nOriginal Error:'{e}'")

            args[index] = value


def ItemValue(world: World, multiworld: MultiWorld, state: CollectionState, player: int, valueCount: str, skipCache: bool = False):
    """When passed a string with this format: 'valueName:int',
    this function will check if the player has collect at least 'int' valueName worth of items\n
    eg. {ItemValue(Coins:12)} will check if the player has collect at least 12 coins worth of items\n
    You can add a second string argument to disable creating/checking the cache like this:
    '{ItemValue(Coins:12,Disable)}' it can be any string you want
    """

    valueCount = valueCount.split(":")
    if not len(valueCount) == 2 or not valueCount[1].isnumeric():
        raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({valueCount[0]}:12)'")
    value_name = valueCount[0].lower().strip()
    requested_count = int(valueCount[1].strip())

    if not hasattr(world, 'itemvalue_rule_cache'): #Cache made for optimization purposes
        world.itemvalue_rule_cache = {}

    if not world.itemvalue_rule_cache.get(player, {}):
        world.itemvalue_rule_cache[player] = {}

    if not skipCache:
        if not world.itemvalue_rule_cache[player].get(value_name, {}):
            world.itemvalue_rule_cache[player][value_name] = {
                'state': {},
                'count': -1,
                }

    if (skipCache or world.itemvalue_rule_cache[player][value_name].get('count', -1) == -1
            or world.itemvalue_rule_cache[player][value_name].get('state') != dict(state.prog_items[player])):
        # Run First Time, if state changed since last check or if skipCache has a value
        existing_item_values = get_items_with_value(world, multiworld, value_name)
        total_Count = 0
        for name, value in existing_item_values.items():
            count = state.count(name, player)
            if count > 0:
                total_Count += count * value
        if skipCache:
            return total_Count >= requested_count
        world.itemvalue_rule_cache[player][value_name]['count'] = total_Count
        world.itemvalue_rule_cache[player][value_name]['state'] = dict(state.prog_items[player])
    return world.itemvalue_rule_cache[player][value_name]['count'] >= requested_count

# Two useful functions to make require work if an item is disabled instead of making it inaccessible
def OptOne(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str, items_counts: Optional[dict] = None):
    """Check if the passed item (with or without ||) is enabled, then this returns |item:count|
    where count is clamped to the maximum number of said item in the itempool.\n
    Eg. requires: "{OptOne(|DisabledItem|)} and |other items|" become "|DisabledItem:0| and |other items|" if the item is disabled.
    """
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
def OptAll(world: World, multiworld: MultiWorld, state: CollectionState, player: int, requires: str):
    """Check the passed require string and loop every item to check if they're enabled,
    then returns the require string with items counts adjusted using OptOne\n
    eg. requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"
    become "|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|" """
    requires_list = requires

    items_counts = world.get_item_counts()

    functions = {}
    if requires_list == "":
        return True
    for item in re.findall(r'\{(\w+)\(([^)]*)\)\}', requires_list):
        #so this function doesn't try to get item from other functions, in theory.
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

# Rule to expose the can_reach_location core function
def canReachLocation(world: World, multiworld: MultiWorld, state: CollectionState, player: int, location: str):
    """Can the player reach the given location?"""
    if state.can_reach_location(location, player):
        return True
    return False

def YamlEnabled(world: "ManualWorld", multiworld: MultiWorld, state: CollectionState, player: int, param: str) -> bool:
    """Is a yaml option enabled?"""
    return is_option_enabled(multiworld, player, param)

def YamlDisabled(world: "ManualWorld", multiworld: MultiWorld, state: CollectionState, player: int, param: str) -> bool:
    """Is a yaml option disabled?"""
    return not is_option_enabled(multiworld, player, param)
