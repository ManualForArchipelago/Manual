from worlds.AutoWorld import World
from BaseClasses import Region

from .Collection import Collection

class ManualRegions(Collection):
    world: World

    def __init__(self, world: World):
        self.world = world

    @property
    def collection(self) -> list:
        return self.world.multiworld.get_regions(self.world.player)

    def __contains__(self, name: str) -> bool:
        return len([r for r in self.collection if r.name == name]) > 0

    def __getitem__(self, name: str) -> Region:
        return self.world.multiworld.get_region(name, self.world.player)

    def __setitem__(self, name: str):
        raise TypeError("You cannot replace or create regions after the regions created phase.")

    def __delitem__(self, key: str):
        raise TypeError("You cannot delete regions after they have been created.")

