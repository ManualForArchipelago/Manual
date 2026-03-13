import dataclasses
import inspect
from typing import TYPE_CHECKING, Any, Callable, Optional
from enum import IntEnum
from operator import eq, ge, le

from .Regions import regionMap
from .hooks import Rules
from .Helpers import clamp, is_item_enabled, is_option_enabled, get_option_value, convert_string_to_type,\
    format_to_valid_identifier, format_state_prog_items_key, ProgItemsCat
from .Game import game_name

from BaseClasses import MultiWorld, CollectionState, Entrance
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule, add_rule
from Options import Choice, Toggle, Range, NamedRange, NumericOption
from Utils import version_tuple

import re
import math
import logging

if TYPE_CHECKING:
    from . import ManualWorld

# At some point in the future, we should depreciate the non-RB codepath.  But that's not until at least 0.7.X
use_rulebuilder = version_tuple >= (0, 6, 7)

if TYPE_CHECKING and use_rulebuilder:
    import rule_builder.rules

FUNCTION_REGEX = re.compile(r'\{(\w+)\((.*?)\)\}')
ITEM_REGEX = re.compile(r'\|(@?)([^|]+?)(\:[^:|]+)?\|')
AND_REGEX = re.compile(r'\s?\bAND\b\s?', re.IGNORECASE)
OR_REGEX = re.compile(r'\s?\bOR\b\s?', flags=re.IGNORECASE)

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

def infix_to_postfix(expr: str, location: dict) -> str:
    prec: dict[str, int] = {"&": 2, "|": 2, "!": 3}
    stack: list[str] = []
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
    def evaluate_nonnumeric_count(item_name: str, item_count: str, is_category: bool, area: dict) -> int:
        item_count = item_count.strip()
        if item_count.isnumeric():
            return int(item_count)

        items_counts = world.get_item_counts(player, only_progression=True)
        if is_category:
            category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items += [event for event in world.event_name_to_event.values() if "category" in event and item_name in event["category"]]
            total_count = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
        else:
            total_count = items_counts.get(item_name, 0)

        if item_count == 'all':
            return total_count
        elif item_count == 'half':
            return int(total_count / 2)
        elif item_count.endswith('%') and len(item_count) > 1:
            percent = clamp(float(item_count[:-1]) / 100, 0, 1)
            return math.ceil(total_count * percent)

        raise ValueError(f"Invalid item count `{item_name}` in {area}.")

    def construct_rule_from_string(area: dict) -> "rule_builder.rules.Rule | None":
        if not use_rulebuilder:
            return None

        import rule_builder.rules

        requires_list = area.get('requires', '')
        if requires_list == "":
            return rule_builder.rules.True_()

        def recursively_tokenize_manual_rule(partial: str) -> "rule_builder.rules.Rule | None":
            if not partial:
                return rule_builder.rules.True_()
            rule = None
            remaining = ''
            partial = partial.strip()
            if match := ITEM_REGEX.match(partial):
                is_category = bool(match.group(1))
                item_name = match.group(2)
                item_count = (str(match.group(3) or "1")).lstrip(':')

                if item_count.isnumeric():
                    count = int(item_count)
                else:
                    count = evaluate_nonnumeric_count(item_name, item_count, is_category, area)

                if is_category:
                    rule = rule_builder.rules.HasGroup(item_name, count)
                else:
                    rule = rule_builder.rules.Has(item_name, count)
                remaining = partial[len(match.group(0)):]
            elif match := FUNCTION_REGEX.match(partial):
                func_name = match.group(1)
                func_args = match.group(2).split(",")
                if func_args == ['']:
                    func_args.pop()

                rule_class = None
                search = [
                    (rule_builder.rules.DEFAULT_RULES, func_name),
                    (globals(), func_name + "Rule"),
                    (globals(), func_name),
                    (Rules, func_name + "Rule"),
                    (Rules, func_name),
                ]
                for ns, name in search:
                    if isinstance(ns, dict):
                        func = ns.get(name)
                    else:
                        func = getattr(ns, name, None)

                    if func and inspect.isclass(func) and issubclass(func, rule_builder.rules.Rule):
                        rule_class = func
                        break

                    if func and inspect.signature(func).return_annotation is str:
                        # I'm assuming that functions that return strings don't need states.
                        convert_req_function_args(None, func, func_args, area['name'], world)
                        rule = recursively_tokenize_manual_rule(func(*func_args))
                        break

                if rule is None:
                    if not rule_class:
                        print(f'Warning: Could not find Rule implmenentation of {func_name}.')
                        # By returning None, we're saying "This entire requires string can't be done with a Rule.  Fall back to the pre-rb lambdas"
                        return None

                    rule = rule_class(*func_args)
            elif partial[0] == "(":
                inner = ''
                queue = list(partial[1:])
                stack = 1
                while stack > 0:
                    c = queue.pop(0)
                    if c == "(":
                        stack += 1
                    elif c == ")":
                        stack -= 1
                    else:
                        inner += c
                rule = recursively_tokenize_manual_rule(inner)
                remaining = "".join(queue)
            else:
                print(f'Could not convert {partial} into a Rule')
                return None

            if rule is None:
                return None

            if match := OR_REGEX.match(remaining):
                remaining = remaining[len(match.group(0)):]
                right = recursively_tokenize_manual_rule(remaining)
                if right is None:
                    return None
                rule = rule | right
                remaining = ''
            elif match := AND_REGEX.match(remaining):
                remaining = remaining[len(match.group(0)):]
                right = recursively_tokenize_manual_rule(remaining)
                if right is None:
                    return None
                rule = rule & right
                remaining = ''

            if remaining:
                raise ValueError(f'Unexpected token `{remaining}` in {area["name"]} rule')
            return rule

        return recursively_tokenize_manual_rule(requires_list)

    # this is only called when the area (think, location or region) has a "requires" field that is a string
    def checkRequireStringForArea(state: CollectionState, area: dict):
        requires_list = area["requires"]

        # Preparing some variables for exception messages
        area_type = "region" if area.get("is_region",False) else "location"
        area_name = area.get("name", f"unknown with these parameters: {area}")

        if requires_list == "":
            return True

        def findAndRecursivelyExecuteFunctions(requires_list: str, recursionDepth: int = 0) -> str:
            found_functions = FUNCTION_REGEX.findall(requires_list)
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

                        convert_req_function_args(state, func, func_args, area_name, world)
                        try:
                            result = func(*func_args)
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
        for match in ITEM_REGEX.finditer(requires_list):
            item_base = match.group(0)
            is_category = match.group(1)
            item_name = match.group(2)
            item_count = match.group(3)
            require_type = 'item'
            if item_base not in requires_list:
                # previous instance of this item was already processed
                continue

            if is_category:
                require_type = 'category'

            if not item_count:
                item_count = "1"
            item_count = item_count.lstrip(':')

            total = 0

            if require_type == 'category':
                category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
                category_items += [event for event in world.event_name_to_event.values() if "category" in event and item_name in event["category"]]
                numeric_count = evaluate_nonnumeric_count(item_name, item_count, True, area)

                for category_item in category_items:
                    total += state.count(category_item["name"], player)

                    if total >= numeric_count:
                        requires_list = requires_list.replace(item_base, "1")
            elif require_type == 'item':
                numeric_count = evaluate_nonnumeric_count(item_name, item_count, False, area)

                total = state.count(item_name, player)

                if total >= numeric_count:
                    requires_list = requires_list.replace(item_base, "1")
            else:
                raise ValueError(f'Unknown require_type {require_type}')

            if total < numeric_count:
                requires_list = requires_list.replace(item_base, "0")

        requires_list = AND_REGEX.sub('&', requires_list, count=0)
        requires_list = OR_REGEX.sub('|', requires_list, count=0)

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
    extra_entrance_rules = {}
    for region in regionMap.keys():
        entrance_rules = regionMap[region].get("entrance_requires", {})
        for e in entrance_rules:
            entrance = world.get_entrance(f'{e}To{region}')
            area = {"requires": entrance_rules[e]}
            extra_entrance_rules[entrance.name] = area

        exit_rules = regionMap[region].get("exit_requires", {})
        for e in exit_rules:
            exit = world.get_entrance(f'{region}To{e}')
            area = {"requires": exit_rules[e]}
            extra_entrance_rules[exit.name] = area

    for region in regionMap.keys():
        used_location_names.extend([l.name for l in multiworld.get_region(region, player).locations])
        for exitRegion in multiworld.get_region(region, player).entrances:
            extra = extra_entrance_rules.get(exitRegion.name, {})
            rb_rule = construct_rule_from_string(regionMap[region])
            if rb_rule is not None:
                if extra:
                    rb_extra_rule = construct_rule_from_string(extra)
                    if rb_extra_rule is None:
                        raise ValueError(f'Unable to combine Rule and functions for {exitRegion.name}.')
                    rb_rule = rb_rule & rb_extra_rule
                world.set_rule(world.get_entrance(exitRegion.name), rb_rule)
            else:
                def fullRegionCheck(state: CollectionState, region=regionMap[region], region_name=exitRegion.name):
                    region['name'] = region_name
                    region['is_region'] = True

                    return fullLocationOrRegionCheck(state, region)

                add_rule(world.get_entrance(exitRegion.name), fullRegionCheck)
                if extra:
                    add_rule(world.get_entrance(exitRegion.name), lambda state, extra=extra: fullLocationOrRegionCheck(state, extra))

    # Location access rules
    for location in (world.location_table + world.event_table):
        if "location_name" in location:
            name = location["location_name"]
        elif location["name"] not in used_location_names:
            continue
        else:
            name = location["name"]

        locFromWorld = multiworld.get_location(name, player)

        if "requires" in location:
            rb_rule = construct_rule_from_string(location)
            if rb_rule is not None:
                world.set_rule(locFromWorld, rb_rule)
            else:
                def checkLocation(state: CollectionState, location=location):
                    locationCheck = fullLocationOrRegionCheck(state, location)
                    return locationCheck

                set_rule(locFromWorld, checkLocation)
        elif use_rulebuilder:
            import rule_builder.rules
            world.set_rule(locFromWorld, rule_builder.rules.True_())
        else: # No location requires? It's accessible.
            def allRegionsAccessible(state):
                return True

            set_rule(locFromWorld, allRegionsAccessible)

    # Victory requirement
    multiworld.completion_condition[player] = lambda state: state.has("__Victory__", player)

def convert_req_function_args(state: CollectionState | None, func, args: list[str | Any], areaName: str, world: World) -> None:
    parameters = inspect.signature(func).parameters
    knownParameters = [World, 'ManualWorld', MultiWorld, CollectionState]
    index = -1
    for parameter in parameters.values():
        target_type = parameter.annotation
        index += 1
        if target_type in knownParameters:
            if target_type in [World, 'ManualWorld']:
                args.insert(index, world)
            elif target_type == MultiWorld:
                args.insert(index, world.multiworld)
            elif target_type == CollectionState and state is None:
                raise ValueError('Function needs a state but none was available')
            elif target_type == CollectionState:
                args.insert(index, state)
            continue
        if parameter.name.lower() == "player":
            args.insert(index, world.player)
            continue

        if index < len(args) and args[index] != "":
            value = args[index].strip()
        else:
            if parameter.default is not inspect.Parameter.empty:
                if index < len(args):
                    args[index] = parameter.default
                else:
                    args.insert(index, parameter.default)
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


def ItemValue(state: CollectionState, player: int, valueCount: str):
    """When passed a string with this format: 'valueName:int',
    this function will check if the player has collect at least 'int' valueName worth of items\n
    eg. {ItemValue(Coins:12)} will check if the player has collect at least 12 coins worth of items
    """

    args: list[str] = valueCount.split(":")
    if not len(args) == 2 or not args[1].isnumeric():
        raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({args[0]}:12)'")
    value_name = format_state_prog_items_key(ProgItemsCat.VALUE, args[0])
    requested_count = int(args[1].strip())
    return state.has(value_name, player, requested_count)


# Two useful functions to make require work if an item is disabled instead of making it inaccessible
def OptOne(world: "ManualWorld", item: str) -> str:
    """Check if the passed item (with or without ||) is enabled, then this returns |item:count|
    where count is clamped to the maximum number of said item in the itempool.\n
    Eg. requires: "{OptOne(|DisabledItem|)} and |other items|" become "|DisabledItem:0| and |other items|" if the item is disabled.
    """
    if item == "":
        return "" #Skip this function if item is left blank

    items_counts = world.get_item_counts(only_progression=True)

    require_category = False

    if '@' in item[:2]:
        require_category = True

    item = item.lstrip('|@$').rstrip('|')

    item_parts = item.split(":")
    item_name = item
    item_count = '1'

    if len(item_parts) > 1:
        item_name = item_parts[0]
        item_count = item_parts[1]

    if require_category:
        if item_count.isnumeric():
            #Only loop if we can use the result to clamp
            category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
            item_count = clamp(int(item_count), 0, category_items_counts)
        return f"|@{item_name}:{item_count}|"
    else:
        if item_count.isnumeric():
            item_current_count = items_counts.get(item_name, 0)
            item_count = clamp(int(item_count), 0, item_current_count)
        return f"|{item_name}:{item_count}|"

# OptAll check the passed require string and loop every item to check if they're enabled,
def OptAll(world: "ManualWorld", requires: str) -> bool|str:
    """Check the passed require string and loop every item to check if they're enabled,
    then returns the require string with items counts adjusted using OptOne\n
    eg. requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"
    become "|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|" """
    requires_list = requires

    if requires_list == "":
        return True

    # parse user written statement into list of each item
    for item in re.findall(r'\|[^|]+\|', requires):
        itemScanned = OptOne(world, item)
        requires_list = requires_list.replace(item, itemScanned)

    return requires_list

# going to be deprecated to name consistently to other req functions, in pascal case
def canReachLocation(state: CollectionState, player: int, location: str):
    logging.warning("The 'canReachLocation' requirement function is being renamed to 'CanReachLocation'. Use that instead, as the lowercase version will be deprecated.")
    return CanReachLocation(state, player, location)

# Rule to expose the can_reach_location core function
def CanReachLocation(state: CollectionState, player: int, location: str) -> bool:
    """Can the player reach the given location?"""
    if state.can_reach_location(location, player):
        return True
    return False

def OptionCount(world: "ManualWorld", item: str, option_name: str) -> str:
    """Set the required count of 'item' to be the value set in the player's yaml of the Numerical option 'option_name'."""
    return _optionCountLogic(world, item, option_name )

def OptionCountPercent(world: "ManualWorld", item: str, option_name: str) -> str:
    """Set the required count of 'item' to be a percentage of it total count based on the player's yaml value for Numerical option 'option_name'."""
    return _optionCountLogic(world, item, option_name, is_percent=True)

def _optionCountLogic(world: "ManualWorld", item: str, option_name: str, is_percent: bool = False) -> str:
    option_name = option_name.strip()
    option: NumericOption | None = getattr(world.options, option_name, None)
    if option is None:
        raise ValueError(f"Could not find an option named: {option_name}")

    # Verification that the value is compatible
    if not isinstance(option.value, int):
        raise ValueError(f"Cannot use a value that is not a number. Got value of '{option.value}' from option {option_name}")

    item = item.strip('|').strip()
    return f"|{item}:{option.value}{'%' if is_percent else ''}|"

def YamlEnabled(multiworld: MultiWorld, player: int, param: str) -> bool:
    """Is a yaml option enabled?"""
    return is_option_enabled(multiworld, player, param)

def YamlDisabled(multiworld: MultiWorld, player: int, param: str) -> bool:
    """Is a yaml option disabled?"""
    return not is_option_enabled(multiworld, player, param)

def YamlCompare(world: "ManualWorld", args: str, skipCache: bool = False) -> bool:
    """Is a yaml option's value compared using {comparator} to the requested value
    \nFormat it like {YamlCompare(OptionName==value)}
    \nWhere == can be any of the following: ==, !=, >=, <=, <, >
    \nExample: {YamlCompare(Example_Range > 5)}"""
    comp_symbols = { #Maybe find a better name for this
        '==' : eq,
        '!=' : eq, #complement of ==
        '>=' : ge,
        '<=' : le,
        '=': eq, #Alternate to be like yaml_option
        '<' : ge, #complement of >=
        '>' : le, #complement of <=
    }

    reverse_result = False

    #Find the comparator symbol to split the string with and for logs
    if '==' in args:
        comparator = '=='
    elif '!=' in args:
        comparator = '!='
        reverse_result = True #complement of == thus reverse by default
    elif '>=' in args:
        comparator = '>='
    elif '<=' in args:
        comparator = '<='
    elif '=' in args:
        comparator = '='
    elif '<' in args:
        comparator = '<'
        reverse_result = True #complement of >=
    elif '>' in args:
        comparator = '>'
        reverse_result = True #complement of <=
    else:
        raise  ValueError(f"Could not find a valid comparator in given string '{args}', it must be one of {comp_symbols.keys()}")

    option_name, value = args.split(comparator)

    initial_option_name = str(option_name).strip() #For exception messages
    option_name = format_to_valid_identifier(option_name)

    # Detect !reversing of result like yaml_option
    if option_name.startswith('!'):
        reverse_result = not reverse_result
        option_name = option_name.lstrip('!')
        initial_option_name = initial_option_name.lstrip('!')

    value = value.strip()

    option = getattr(world.options, option_name, None)
    if option is None:
        raise ValueError(f"YamlCompare could not find an option called '{initial_option_name}' to compare against, its either missing on misspelt")

    if not value: #empty string ''
        raise ValueError(f"Could not find a valid value to compare against in given string '{args}'. \nThere must be a value to compare against after the comparator (in this case '{comparator}').")

    if not skipCache: #Cache made for optimization purposes
        cacheindex = option_name + '_' + comp_symbols[comparator].__name__ + '_' + format_to_valid_identifier(value.lower())

        if not hasattr(world, 'yaml_compare_rule_cache'):
            world.yaml_compare_rule_cache = dict[str,bool]()

    if skipCache or world.yaml_compare_rule_cache.get(cacheindex, None) is None:
        try:
            if issubclass(type(option), Choice):
                value = convert_string_to_type(value, str|int)
                if isinstance(value, str):
                    value = option.from_text(value).value

            elif issubclass(type(option), Range):
                if type(option).__base__ == NamedRange:
                    value = convert_string_to_type(value, str|int)
                    if isinstance(value, str):
                        value = option.from_text(value).value

                else:
                    value = convert_string_to_type(value, int)

            elif issubclass(type(option), Toggle):
                value = int(convert_string_to_type(value, bool))

            else:
                raise ValueError(f"YamlCompare does not currently support Option of type {type(option)} \nAsk about it in #Manual-dev and it might be added.")

        except KeyError as ex:
            raise ValueError(f"YamlCompare failed to find the requested value in what the \"{initial_option_name}\" option supports.\
                \nRaw error:\
                \n\n{type(ex).__name__}:{ex}")

        except Exception as ex:
            raise TypeError(f"YamlCompare failed to convert the requested value to what a {type(option).__base__.__name__} option supports.\
                \nCaused By:\
                \n\n{type(ex).__name__}:{ex}")

        if isinstance(value, str) and comp_symbols[comparator].__name__ != 'eq':
            #At this point if its still a string don't try and compare with strings using > < >= <=
            raise ValueError(f'YamlCompare can only compare strings with one of the following: {[s for s, v in comp_symbols.items() if v.__name__ == "eq"]} and you tried to do: "{option.value} {comparator} {value}"')

        result = comp_symbols[comparator](option.value, value)

        if not skipCache:
            world.yaml_compare_rule_cache[cacheindex] = result

    else: #if exists and not skipCache
        result = world.yaml_compare_rule_cache[cacheindex]

    return not result if reverse_result else result

if use_rulebuilder:
    from rule_builder.rules import Rule, Has, True_, False_

    @dataclasses.dataclass()
    class ItemValueRule(Rule["ManualWorld"], game=game_name):
        valueCount: str
        def _instantiate(self, world: "ManualWorld") -> Rule.Resolved:
            args: list[str] = self.valueCount.split(":")
            if not len(args) == 2 or not args[1].isnumeric():
                raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({args[0]}:12)'")
            value_name = format_state_prog_items_key(ProgItemsCat.VALUE, args[0])
            requested_count = int(args[1].strip())
            return Has(value_name, requested_count).resolve(world)

    @dataclasses.dataclass()
    class YamlEnabledRule(Rule["ManualWorld"], game=game_name):
        yaml_option: str
        def _instantiate(self, world: "ManualWorld") -> Rule.Resolved:
            if getattr(world.options, self.yaml_option).value:
                return True_().resolve(world)
            else:
                return False_().resolve(world)

    @dataclasses.dataclass()
    class YamlDisabledRule(Rule["ManualWorld"], game=game_name):
        yaml_option: str
        def _instantiate(self, world: "ManualWorld") -> Rule.Resolved:
            if getattr(world.options, self.yaml_option).value:
                return False_().resolve(world)
            else:
                return True_().resolve(world)

    @dataclasses.dataclass()
    class YamlCompareRule(Rule["ManualWorld"], game=game_name):
        yaml_comparison: str
        def _instantiate(self, world: "ManualWorld") -> Rule.Resolved:
            if YamlCompare(world, self.yaml_comparison):
                return True_().resolve(world)
            else:
                return False_().resolve(world)



    # # This was an attempt to make a universal lambda caller rule.  It's messy, complicated, and probably not worth it.
    # # As you can see above, you are much better off implementing optimized Rules rather than trying to execute check-time access rules this way.
    # # This code is left here both as a warning and also a starting point.
    # # But as things currently stand, you're better off either letting the whole rule fall back to lambdas or writing a proper custom Rule.
    # # This middleground is not a good idea.
    # @dataclasses.dataclass()
    # class FallbackLambdaRule(Rule["ManualWorld"], game=game_name):
    #     access_rule: Callable
    #     args: list[str | Any]

    #     def _instantiate(self, world: "ManualWorld") -> Rule.Resolved:
    #         return self.Resolved(self.access_rule, self.args, world)

    #     class Resolved(Rule.Resolved):
    #         access_rule: Callable
    #         args: list[str | Any]
    #         world: World

    #         @override
    #         def _evaluate(self, state: CollectionState) -> bool:
    #             args = self.args.copy()
    #             convert_req_function_args(state, self.access_rule, args, "", self.world)
    #             value = self.access_rule(*args)
    #             if isinstance(value, bool):
    #                 return value
    #             name = self.access_rule.__name__
    #             raise ValueError(f'Unexpected return value {value} from {name}')


