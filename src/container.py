import json
import zipfile
from typing import Any

from worlds import Files

from .Data import region_table, category_table
from .Game import game_name
from .Items import item_name_to_item
from .Locations import location_name_to_location


class APManualFile(Files.APPlayerContainer):
    game = game_name
    patch_file_ending = ".apmanual"

    items: dict[str, Any] = None
    locations: dict[str, Any] = None
    regions: dict[str, Any] = None
    categories: dict[str, Any] = None

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)


    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("items.json", json.dumps(item_name_to_item, indent=2))
        opened_zipfile.writestr("locations.json", json.dumps(location_name_to_location, indent=2))
        opened_zipfile.writestr("regions.json", json.dumps(region_table, indent=2))
        opened_zipfile.writestr("categories.json", json.dumps(category_table, indent=2))

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.items = json.loads(opened_zipfile.read("items.json"))
        self.locations = json.loads(opened_zipfile.read("locations.json"))
        self.regions = json.loads(opened_zipfile.read("regions.json"))
        return manifest

    def get_manifest(self) -> dict[str, Any]:
        data = super().get_manifest()
        data["items"] = self.items
        data["locations"] = self.locations
        data["regions"] = self.regions
        return data
