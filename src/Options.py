from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, PerGameCommonOptions
from dataclasses import make_dataclass
from .hooks.Options import before_options_defined, after_options_defined
from .Data import category_table
from .Locations import victory_names
from .Items import item_table


class FillerTrapPercent(Range):
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps."""
    range_end = 100

manual_options = before_options_defined({})

if len(victory_names) > 1:
    goal = {'option_' + v: i for i, v in enumerate(victory_names)}
    docstring = "Choose your victory condition."
    defaultvalue = 0
    if manual_options.get('goal'): 
    #Grab existing Goal option and make alias out of it's values
        for alias, value in manual_options.get('goal').options.items():
            goal[f"alias_{alias}"] = value
        docstring = manual_options.get('goal').__doc__
        defaultvalue = manual_options.get('goal').default
    manual_options['goal'] = type('goal', (Choice,), goal)
    manual_options['goal'].__doc__ = docstring
    manual_options['goal'].default = defaultvalue


if any(item.get('trap') for item in item_table):
    manual_options["filler_traps"] = FillerTrapPercent

for category in category_table:
    for option_name in category_table[category].get("yaml_option", []):
        if option_name[0] == "!":
            option_name = option_name[1:]
        if option_name not in manual_options:
            manual_options[option_name] = type(option_name, (DefaultOnToggle,), {"default": True})
            manual_options[option_name].__doc__ = "Should items/locations linked to this option be enabled?"

manual_options = after_options_defined(manual_options)
manual_options_data = make_dataclass('ManualOptionsClass', manual_options.items(), bases=(PerGameCommonOptions,))
