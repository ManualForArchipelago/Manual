from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, PerGameCommonOptions, DeathLink
from dataclasses import make_dataclass
from .hooks.Options import before_options_defined, after_options_defined
from .Data import category_table, game_table, option_table

from .Locations import victory_names
from .Items import item_table
import logging


class FillerTrapPercent(Range):
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps."""
    range_end = 100

def convertToLongString(input: str | list) -> str: #Todo maybe find a better name for this
    if not isinstance(input, str):
        return str.join("\n", input)
    return input

def createChoiceOptions(values: dict, aliases: dict) -> dict:
    values = {'option_' + i: v for i, v in values.items()}
    aliases = {'alias_' + i: v for i, v in aliases.items()}
    return {**values, **aliases}

manual_options = before_options_defined({})

for option_name, option in option_table.items():
    if option_name.startswith('_'): #To allow commenting out options
        continue
    option_type = Toggle
    args = {'display_name': option.get('display_name', option_name)}
    if option['type'] == "DefaultOnToggle":
        option_type = DefaultOnToggle
    elif option['type'] == "Choice" or option['type'] == "TextChoice":
        option_type = Choice
        if option['type'] == "TextChoice":
            option_type = TextChoice
        args = {**args, **createChoiceOptions(option.get('values'), option.get('aliases', {}))}
    if option_name in ['goal', 'filler_traps']:
        if manual_options.get('goal'):
            logging.warn("Existing Goal option found created via Hooks, it will be overwritten by Manual's generated Goal option.\nIf you want to support old yaml you will need to add alias in after_options_defined")
        #todo do something for those situations, maybe convert, maybe warn idk for now
        continue
    if option_name not in manual_options:
        manual_options[option_name] = type(option_name, (option_type,), args )
        manual_options[option_name].__doc__ = convertToLongString(option.get('description', "an Option"))

if len(victory_names) > 1:
    goal = {'option_' + v: i for i, v in enumerate(victory_names)}
    # Check for existing Goal option
    manual_options['goal'] = type('goal', (Choice,), goal)
    manual_options['goal'].__doc__ = "Choose your victory condition."


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

manual_options = after_options_defined(manual_options)
manual_options_data = make_dataclass('ManualOptionsClass', manual_options.items(), bases=(PerGameCommonOptions,))
