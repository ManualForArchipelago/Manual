from worlds.AutoWorld import World

from ..Locations import ManualLocation

from .CollectionList import CollectionList

class ManualLocations(CollectionList):
    world: World

    def __init__(self, world: World):
        self.world = world

    @property
    def collection(self) -> list:
        return self.world.multiworld.get_locations(world.player)

    def __contains__(self, name: str) -> bool:
        return len([i for i in self.collection if i.name == name]) > 0

    def __getitem__(self, name: str) -> list | ManualLocation:
        matches = [i for i in self.collection if i.name == name]

        if not matches:
            return []

        if len(matches) > 1:
            return matches

        return matches[0]

    def __delitem__(self, obj: ManualLocation):
        if not obj.parent_region:
            raise TypeError("You cannot remove a location that has no region associated with it.")

        obj.parent_region.locations.remove(obj)

