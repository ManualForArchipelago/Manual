import json
import logging
import os
import pkgutil

from .DataValidation import DataValidation, ValidationError

from .hooks.Data import \
    after_load_game_file, \
    after_load_item_file, after_load_location_file, \
    after_load_region_file, after_load_category_file, \
    after_load_meta_file

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

def convert_to_list(data, property_name: str) -> list:
    if isinstance(data, dict):
        data = data.get(property_name, [])
    return data

game_table = load_data_file('game.json') #dict
item_table = convert_to_list(load_data_file('items.json'), 'data') #list
location_table = convert_to_list(load_data_file('locations.json'), 'data') #list
region_table = load_data_file('regions.json') #dict
category_table = load_data_file('categories.json') or {} #dict
meta_table = load_data_file('meta.json') or {} #dict

# Removal of schemas in root of tables
region_table.pop('$schema', '')
category_table.pop('$schema', '')

# hooks
game_table = after_load_game_file(game_table)
item_table = after_load_item_file(item_table)
location_table = after_load_location_file(location_table)
region_table = after_load_region_file(region_table)
category_table = after_load_category_file(category_table)
meta_table = after_load_meta_file(meta_table)

# seed all of the tables for validation
DataValidation.game_table = game_table
DataValidation.item_table = item_table
DataValidation.location_table = location_table
DataValidation.region_table = region_table

validation_errors = []

# check that json files are not just invalid json
try: DataValidation.checkForGameBeingInvalidJSON()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkForItemsBeingInvalidJSON()
except ValidationError as e: validation_errors.append(e)

try: DataValidation.checkForLocationsBeingInvalidJSON()
except ValidationError as e: validation_errors.append(e)


############
# If there are any validation errors, display all of them at once
############

if len(validation_errors) > 0:
    logging.error("\nValidationError(s): \n\n%s\n\n" % ("\n".join([' - ' + str(validation_error) for validation_error in validation_errors])))
    print("\n\nYou can close this window.\n")
    keeping_terminal_open = input("If you are running from a terminal, press Ctrl-C followed by ENTER to break execution.")
