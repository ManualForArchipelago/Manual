import logging
import os
import json
import zipfile
from argparse import Namespace

from .DataValidation import DataValidation, ValidationError
from .Helpers import load_data_file as helpers_load_data_file

from .hooks.Data import \
    after_load_game_file, \
    after_load_item_file, after_load_location_file, \
    after_load_region_file, after_load_category_file, \
    after_load_option_file, after_load_meta_file

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    logging.warning("Deprecated usage of importing load_data_file from Data.py uses the one from Helper.py instead")
    return helpers_load_data_file(*args)

def convert_to_list(data, property_name: str) -> list:
    if isinstance(data, dict):
        data = data.get(property_name, [])
    return data

class ManualFile:
    source_path: any
    filename: str
    data_type: dict|list

    def __init__(self, source_path, filename, data_type):
        self.source_path = source_path
        self.filename = filename
        self.data_type = data_type

    def load(self, safe=False):
        if safe:
            try:
                return json.loads(zipfile.Path(
                        self.source_path,
                        f"{os.path.splitext(self.source_path.name)[0]}/data/{self.filename}"
                    ).open().read())
            except:
                return self.data_type()
        else:
            contents = helpers_load_data_file(self.filename, source=self.source_path)

            if not contents and type(contents) != self.data_type:
                return self.data_type()

            return contents

def get_data_Namespace(path="", safe=False) -> Namespace:
    # TODO add path handling so it can be retargeted to a different source than self
    ret = Namespace()

    ret.game_table = ManualFile(path, 'game.json', dict).load(safe=safe) #dict
    ret.item_table = convert_to_list(ManualFile(path, 'items.json', list).load(safe=safe), 'data') #list
    ret.location_table = convert_to_list(ManualFile(path, 'locations.json', list).load(safe=safe), 'data') #list
    ret.region_table = ManualFile(path, 'regions.json', dict).load(safe=safe) #dict
    ret.category_table = ManualFile(path, 'categories.json', dict).load(safe=safe) #dict
    ret.option_table = ManualFile(path, 'options.json', dict).load(safe=safe) #dict
    ret.meta_table = ManualFile(path, 'meta.json', dict).load(safe=safe) #dict

    # Removal of schemas in root of tables
    ret.region_table.pop('$schema', '')
    ret.category_table.pop('$schema', '')

    # hooks
    ret.game_table = after_load_game_file(ret.game_table)
    ret.item_table = after_load_item_file(ret.item_table)
    ret.location_table = after_load_location_file(ret.location_table)
    ret.region_table = after_load_region_file(ret.region_table)
    ret.category_table = after_load_category_file(ret.category_table)
    ret.option_table = after_load_option_file(ret.option_table)
    ret.meta_table = after_load_meta_file(ret.meta_table)

    # seed all of the tables for validation
    ret.data_validation = DataValidation()
    ret.data_validation.game_table = ret.game_table
    ret.data_validation.item_table = ret.item_table
    ret.data_validation.location_table = ret.location_table
    ret.data_validation.region_table = ret.region_table

    validation_errors = []

    # check that json files are not just invalid json
    try: ret.data_validation.checkForGameBeingInvalidJSON()
    except ValidationError as e: validation_errors.append(e)

    try: ret.data_validation.checkForItemsBeingInvalidJSON()
    except ValidationError as e: validation_errors.append(e)

    try: ret.data_validation.checkForLocationsBeingInvalidJSON()
    except ValidationError as e: validation_errors.append(e)


    ############
    # If there are any validation errors, display all of them at once
    ############

    if len(validation_errors) > 0:
        logging.error("\nValidationError(s): \n\n%s\n\n" % ("\n".join([' - ' + str(validation_error) for validation_error in validation_errors])))
        print("\n\nYou can close this window.\n")
        keeping_terminal_open = input("If you are running from a terminal, press Ctrl-C followed by ENTER to break execution.")

    from .Game import parse_gamedata
    parse_gamedata(ret)
    from .Items import parse_itemdata
    parse_itemdata(ret)
    from .Locations import parse_locationdata
    parse_locationdata(ret)
    from .Meta import parse_metadata
    parse_metadata(ret)
    from .Regions import parse_regiondata
    parse_regiondata(ret)

    return ret
