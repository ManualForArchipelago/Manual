from BaseClasses import Location
from .Data import location_table, event_table
from .Game import starting_index, game_name


######################
# Generate location lookups
######################

count = starting_index
victory_names: list[str] = []

# add sequential generated ids to the lists
for key, _ in enumerate(location_table):
    if "victory" in location_table[key] and location_table[key]["victory"]:
        victory_names.append(location_table[key]["name"])

    if "id" in location_table[key]:
        item_id = location_table[key]["id"]
        if item_id >= count:
            count = item_id
        else:
            raise ValueError(f"{location_table[key]['name']} has an invalid ID. ID must be at least {count + 1}")

    location_table[key]["id"] = count

    if "region" not in location_table[key]:
        location_table[key]["region"] = "Manual" # all locations are in the same region for Manual

    if isinstance(location_table[key].get("category", []), str):
        location_table[key]["category"] = [location_table[key]["category"]]

    count += 1

if not victory_names:
    # Add the game completion location, which will have the Victory item assigned to it automatically
    location_table.append({
        "id": count + 1,
        "name": "__Manual Game Complete__",
        "region": "Manual",
        "requires": []
        # "category": custom_victory_location["category"] if "category" in custom_victory_location else []
    })
    victory_names.append("__Manual Game Complete__")

location_id_to_name: dict[int, str] = {}
location_name_to_location: dict[str, dict] = {}
location_name_groups: dict[str, list[str]] = {}
event_name_to_event: dict[str, list[str]] = {}

for loc in location_table:
    loc_name = loc.get("name", f"Unnamed Location {loc['id']}")
    location_id_to_name[loc["id"]] = loc_name
    location_name_to_location[loc_name] = loc

    for c in loc.get("category", []):
        if c not in location_name_groups:
            location_name_groups[c] = []
        location_name_groups[c].append(loc_name)


# location_id_to_name[None] = "__Manual Game Complete__"
location_name_to_id = {name: id for id, name in location_id_to_name.items()}

for key, _ in enumerate(event_table):
    if "copy_location" in event_table[key]:
        event_table[key] = location_name_to_location[event_table[key]["copy_location"]] | event_table[key]

id = 0
for key, event in enumerate(event_table):
    if "location_name" in event:
        if event["location_name"] in location_name_to_location:
            raise Exception(f"Cannot define event {event['location_name']} with the same name as a location.")
        event_name_to_event[event_name] = event
    else:
        event_name = f"{id}_{event['name']}".upper().replace(" ", "_")
        while event_name in location_name_to_location:
            id += 1
            event_name = f"{id}_{event['name']}".upper().replace(" ", "_")
        event_name_to_event[event_name] = event
        event_name_to_event[event_name]["location_name"] = event_name
        event_table[key]["location_name"] = event_name
    if 'visible' not in event:
        event_name_to_event[event_name]['visible'] = False
        event_table[key]['visible'] = False
    if 'region' not in event:
        event_name_to_event[event_name]['region'] = "Manual"
        event_table[key]['region'] = "Manual"
    id += 1

######################
# Location classes
######################


class ManualLocation(Location):
    game = game_name
