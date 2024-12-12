import importlib
import os

from worlds.AutoWorld import World

class ManualHooks:
    world: World

    worlds_dir_name: str
    hooks_dir_name: str = "hooks"
    world_name: str
    package_name: str
    available_modules: list[str] = ["World", "Data", "Options"]

    def __init__(self, world: World = None):
        self.set_world(world)
        
        path_parts = os.path.abspath(__file__).split("/")

        self.worlds_dir_name = "custom_worlds" if "custom_worlds" in path_parts else "worlds"
        self.world_name = [p for p in path_parts if "manual_" in p][0]
        self.package_name = ".".join([self.worlds_dir_name, self.world_name, self.hooks_dir_name])

    def __call__(self, hook_func_name: str, *args):
        for module_name in self.available_modules:
            try:
                module = importlib.import_module(f"{self.package_name}.{module_name}", self.package_name)
                module_func = getattr(module, hook_func_name)

                if self.world:
                    hook_func_results = module_func(*args, self.world, self.world.multiworld, self.world.player)
                else:
                    hook_func_results = module_func(*args)

                return hook_func_results
            except AttributeError:
                pass

        return

    def set_world(self, world: World = None):
        self.world = world
