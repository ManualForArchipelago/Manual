from Options import PerGameCommonOptions, FreeText, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, DeathLink, \
    OptionGroup, StartInventoryPool, Visibility, item_and_loc_options
from .hooks.Options import before_options_defined, after_options_defined, before_option_groups_created, after_option_groups_created
from .Data import category_table, game_table, option_table
from .Helpers import convertToLongString
from .Locations import victory_names
from .Items import item_table
from .Game import starting_items

from dataclasses import make_dataclass
from typing import List
import logging


class FillerTrapPercent(Range):
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps."""
    range_end = 100

def createChoiceOptions(values: dict, aliases: dict) -> dict:
    values = {'option_' + i: v for i, v in values.items()}
    aliases = {'alias_' + i: v for i, v in aliases.items()}
    return {**values, **aliases}

manual_options = before_options_defined({})
manual_options["start_inventory_from_pool"] = StartInventoryPool

manual_option_groups = {}
manual_goal_override = {}

# A list of Currently Supported Option types
# full support looks like: ["Toggle", "DefaultOnToggle", "Choice", "TextChoice", "Range", "NamedRange"]
supported_option_types = ["Toggle", "DefaultOnToggle", "Choice", "TextChoice", "Range", "NamedRange"]
for option_name, option in option_table.get('data', {}).items():
    if option_name.startswith('_'): #To allow commenting out options
        continue

    if option_name in ['goal', 'filler_traps']:
        if manual_options.get('goal'):
            logging.warning("Existing Goal option found created via Hooks, it will be overwritten by Manual's generated Goal option.\nIf you want to support old yaml you will need to add alias in after_options_defined")
        # todo do something for those situations, maybe convert, maybe warn idk for now
        if option_name == 'goal':
            if option['type'] != 'Choice':
                raise Exception("a 'goal' option must be of type 'Choice'")
            manual_goal_override['args'] = createChoiceOptions({}, option.get('aliases', {}))
            manual_goal_override['args']['default'] = args['default'] = option.get('default', 0)
            manual_goal_override['args']['display_name'] = option.get('display_name', option_name)
            manual_goal_override['description'] = convertToLongString(option.get('description', ''))
        continue

    if option_name not in manual_options:
        option_type = option.get('type', None)

        if option_type is None or option_type not in supported_option_types:
            raise Exception(f'Option {option_name} in options.json has an invalid type of "{option["type"]}".\nIt must be one of the folowing: {supported_option_types}')

        args = {'display_name': option.get('display_name', option_name)}

        if option_type in ["Toggle", "DefaultOnToggle"]:
            option_class = Toggle if option_type == "Toggle" else DefaultOnToggle

        elif option_type in ["Choice", "TextChoice"]:
            args = {**args, **createChoiceOptions(option.get('values'), option.get('aliases', {}))}
            option_class = Choice if option_type == "Choice" else TextChoice

        elif option_type in ["Range", "NamedRange"]:
            args['range_start'] = option.get('range_start', 0)
            args['range_end'] = option.get('range_end', 1)
            if option_type == "NamedRange":
                args['special_range_names'] = option.get('special_range_names', {})
                args['special_range_names']['default'] = option.get('default', args['range_start'])
            option_class = Range if option_type == "Range" else NamedRange

        if option.get('default'):
            args['default'] = option['default']

        if option.get('rich_text_doc',None) is not None:
            args["rich_text_doc"] = option["rich_text_doc"]

        if option.get('visibility'):
            visibility = Visibility.all
            if isinstance(option['visibility'], list):
                visibility = Visibility.none
                for type in option['visibility']:
                    visibility += Visibility[type.lower()]
            elif isinstance(option['visibility'],str):
                if option['visibility'].startswith('0b'):
                    visibility = int(option['visibility'], base=0)
                else:
                    visibility = Visibility[option['visibility'].lower()]
            elif isinstance(option['visibility'], int):
                visibility = option['visibility']
            args['visibility'] = visibility

        manual_options[option_name] = type(option_name, (option_type,), args )
        manual_options[option_name].__doc__ = convertToLongString(option.get('description', "an Option"))

    if option.get('group'):
        group = option['group']
        if group not in manual_option_groups.keys():
            manual_option_groups[group] = []
        if option_name not in manual_option_groups[group]:
            manual_option_groups[group].append(manual_options[option_name])

if len(victory_names) > 1:
    goal = {'option_' + v: i for i, v in enumerate(victory_names)}
    # Check for existing Goal option
    if manual_goal_override:
        goal = {**goal, **manual_goal_override['args']}
    manual_options['goal'] = type('goal', (Choice,), goal)
    manual_options['goal'].__doc__ = manual_goal_override.get('description', '') or "Choose your victory condition."


if any(item.get('trap') for item in item_table):
    manual_options["filler_traps"] = FillerTrapPercent

if game_table.get("death_link"):
    manual_options["death_link"] = DeathLink

for category in category_table:
    for option_name in category_table[category].get("yaml_option", []):
        if option_name[0] == "!":
            option_name = option_name[1:]
        if option_name not in manual_options:
            manual_options[option_name] = type(option_name, (DefaultOnToggle,), {"default": True})
            manual_options[option_name].__doc__ = "Should items/locations linked to this option be enabled?"

if starting_items:
    for starting_items in starting_items:
        if starting_items.get("yaml_option"):
            for option_name in starting_items["yaml_option"]:
                if option_name[0] == "!":
                    option_name = option_name[1:]
                if option_name not in manual_options:
                    manual_options[option_name] = type(option_name, (DefaultOnToggle,), {"default": True})
                    manual_options[option_name].__doc__ = "Should items/locations linked to this option be enabled?"

def make_options_group() -> list[OptionGroup]:
    global manual_option_groups
    manual_option_groups = before_option_groups_created(manual_option_groups)
    option_groups: List[OptionGroup] = []

    # For some reason, unless they are added manually, the base item and loc option don't get grouped as they should
    base_item_loc_group = item_and_loc_options

    if manual_option_groups:
        if 'Item & Location Options' in manual_option_groups.keys():
            base_item_loc_group.extend(manual_option_groups['Item & Location Options'])
            manual_option_groups.pop('Item & Location Options')

        for group, options in manual_option_groups.items():
            option_groups.append(OptionGroup(group, options))

    option_groups.append(OptionGroup('Item & Location Options', base_item_loc_group, True))

    return after_option_groups_created(option_groups)

manual_options = after_options_defined(manual_options)
manual_options_data = make_dataclass('ManualOptionsClass', manual_options.items(), bases=(PerGameCommonOptions,))
