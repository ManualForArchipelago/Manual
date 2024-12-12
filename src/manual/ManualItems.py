from worlds.AutoWorld import World

from ..Items import ManualItem

from .CollectionList import CollectionList

class ManualItems(CollectionList):
    world: World

    def __init__(self, world: World):
        self.world = world

    @property
    def collection(self) -> list:
        return [i for i in self.world.multiworld.get_items() if i.player == world.player]

    def __contains__(self, name: str) -> bool:
        return len([i for i in self.collection if i.name == name]) > 0

    def __getitem__(self, name: str) -> list | ManualItem:
        matches = [i for i in self.collection if i.name == name]

        if not matches:
            return []

        if len(matches) > 1:
            return matches

        return matches[0]

    def __delitem__(self, obj: ManualItem):
        self.world.multiworld.itempool.remove(item)
        
