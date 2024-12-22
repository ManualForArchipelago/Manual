from argparse import Namespace

from BaseClasses import Location


def parse_locationdata(ret: Namespace):
    ######################
    # Generate location lookups
    ######################

    count = ret.starting_index
    ret.victory_names: list[str] = []

    # add sequential generated ids to the lists
    for key, _ in enumerate(ret.location_table):
        if "victory" in ret.location_table[key] and ret.location_table[key]["victory"]:
            ret.victory_names.append(ret.location_table[key]["name"])

        if "id" in ret.location_table[key]:
            item_id = ret.location_table[key]["id"]
            if item_id >= count:
                count = item_id
            else:
                raise ValueError(f"{ret.location_table[key]['name']} has an invalid ID. ID must be at least {count + 1}")

        ret.location_table[key]["id"] = count

        if "region" not in ret.location_table[key]:
            ret.location_table[key]["region"] = "Manual" # all locations are in the same region for Manual

        if isinstance(ret.location_table[key].get("category", []), str):
            ret.location_table[key]["category"] = [ret.location_table[key]["category"]]

        count += 1

    if not ret.victory_names:
        # Add the game completion location, which will have the Victory item assigned to it automatically
        ret.location_table.append({
            "id": count + 1,
            "name": "__Manual Game Complete__",
            "region": "Manual",
            "requires": []
            # "category": custom_victory_location["category"] if "category" in custom_victory_location else []
        })
        ret.victory_names.append("__Manual Game Complete__")

    ret.location_id_to_name: dict[int, str] = {}
    ret.location_name_to_location: dict[str, dict] = {}
    ret.location_name_groups: dict[str, list[str]] = {}

    for item in ret.location_table:
        ret.location_id_to_name[item["id"]] = item["name"]
        ret.location_name_to_location[item["name"]] = item

        for c in item.get("category", []):
            if c not in ret.location_name_groups:
                ret.location_name_groups[c] = []
            ret.location_name_groups[c].append(item["name"])


    # ret.location_id_to_name[None] = "__Manual Game Complete__"
    ret.location_name_to_id = {name: id for id, name in ret.location_id_to_name.items()}

######################
# Location classes
######################


class ManualLocation(Location):
    game = "Manual"
