from worlds.AutoWorld import World

from .ManualItems import ManualItems
from .ManualLocations import ManualLocations
from .ManualOptions import ManualOptions
from .ManualRegions import ManualRegions
from .ManualHooks import ManualHooks

class Manual:
    # an AP World object imported via the constructor to later use custom functions to access AP-defined methods
    world: World

    # Manual classes to represent different data structures
    items: ManualItems
    locations: ManualLocations
    options: ManualOptions
    regions: ManualRegions
    hooks: ManualHooks

    def __init__(self, world: World):
        self.world = world
        self.items = ManualItems(self.world)
        self.locations = ManualLocations(self.world)
        self.options = ManualOptions(self.world)
        self.regions = ManualRegions(self.world)
        self.hooks = ManualHooks(self.world)
    
