import json
import logging

from .DataValidation import DataValidation, ValidationError

from .Utils import load_data_file

from .hooks.Data import \
    after_load_game_file, \
    after_load_item_file, after_load_location_file, \
    after_load_region_file, after_load_category_file, \
    after_load_meta_file

def convert_to_list(data, property_name: str) -> list:
    if isinstance(data, dict):
        data = data.get(property_name, [])
    return data

def convert_to_dict(data) -> dict:
    if isinstance(data, list):
        data = {'data':data}
    return data

class ManualFile:
    filename: str
    data_type: dict|list

    def __init__(self, filename, data_type):
        self.filename = filename
        self.data_type = data_type

    def load(self):
        contents = load_data_file(self.filename)

        if not contents and type(contents) != self.data_type:
            return self.data_type()

        return contents

# seed all of the tables for validation and keep the $schema if present
DataValidation.game_table = ManualFile('game.json', dict).load() #dict
DataValidation.item_table = convert_to_dict(ManualFile('items.json', list).load())
DataValidation.location_table = convert_to_dict(ManualFile('locations.json', list).load())
DataValidation.region_table = ManualFile('regions.json', dict).load()
DataValidation.category_table = ManualFile('categories.json', dict).load()
DataValidation.meta_table = ManualFile('meta.json', dict).load()

game_table = DataValidation.game_table #dict
item_table = DataValidation.item_table['data'] #list
location_table = DataValidation.location_table['data'] #list
region_table = DataValidation.region_table #dict
category_table = DataValidation.category_table #dict
meta_table = DataValidation.meta_table #dict


# hooks
game_table = after_load_game_file(game_table)
item_table = after_load_item_file(item_table)
location_table = after_load_location_file(location_table)
region_table = after_load_region_file(region_table)
category_table = after_load_category_file(category_table)
meta_table = after_load_meta_file(meta_table)

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
