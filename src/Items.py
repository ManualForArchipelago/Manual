from argparse import Namespace

from BaseClasses import Item


def parse_itemdata(ret: Namespace):

    ######################
    # Generate item lookups
    ######################

    ret.item_id_to_name: dict[int, str] = {}
    ret.item_name_to_item: dict[str, dict] = {}
    ret.item_name_groups: dict[str, str] = {}
    advancement_item_names: set[str] = set()
    lastItemId = -1

    count = ret.starting_index

    # add the filler item to the list of items for lookup
    if ret.filler_item_name:
        ret.item_table.append({
            "name": ret.filler_item_name
        })

    # add sequential generated ids to the lists
    for key, val in enumerate(ret.item_table):
        if "id" in ret.item_table[key]:
            item_id = ret.item_table[key]["id"]
            if item_id >= count:
                count = item_id
            else:
                raise ValueError(f"{ret.item_table[key]['name']} has an invalid ID. ID must be at least {count + 1}")

        ret.item_table[key]["id"] = count
        ret.item_table[key]["progression"] = val["progression"] if "progression" in val else False
        if isinstance(val.get("category", []), str):
            ret.item_table[key]["category"] = [val["category"]]
            
        count += 1

    for item in ret.item_table:
        item_name = item["name"]
        ret.item_id_to_name[item["id"]] = item_name
        ret.item_name_to_item[item_name] = item

        if item["id"] is not None:
            lastItemId = max(lastItemId, item["id"])

        for c in item.get("category", []):
            if c not in ret.item_name_groups:
                ret.item_name_groups[c] = []
            ret.item_name_groups[c].append(item_name)

        #Just lowercase the values here to remove all the .lower.strip down the line
        item['value'] = {k.lower().strip(): v
                         for k, v in item.get('value', {}).items()}

        for v in item.get("value", {}).keys():
            group_name = f"has_{v}_value"
            if group_name not in ret.item_name_groups:
                ret.item_name_groups[group_name] = []
            ret.item_name_groups[group_name].append(item_name)

    ret.item_id_to_name[None] = "__Victory__"
    ret.item_name_to_id = {name: id for id, name in ret.item_id_to_name.items()}


######################
# Item classes
######################


class ManualItem(Item):
    game = "Manual"
