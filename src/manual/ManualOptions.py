from worlds.AutoWorld import World
from Options import Option

from .Collection import Collection

class ManualOptions(Collection):
    world: World

    def __init__(self, world: World):
        self.world = world

    @property
    def collection(self) -> dict:
        keys = self.world.options_dataclass.type_hints.keys()

        return { key: getattr(self.world.options, key) for key in keys }

    def __contains__(self, name: str) -> bool:
        return name in self.collection.keys()

    def __getitem__(self, name: str) -> Option:
        return self.world.options[name]

    def __setitem__(self, name: str):
        raise TypeError("You cannot replace or create options after the options defined phase.")

    def __delitem__(self, key: str):
        raise TypeError("You cannot delete options after they have been defined.")

