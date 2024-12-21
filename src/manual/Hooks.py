import inspect

from typing import Type, Optional, TYPE_CHECKING

from worlds.AutoWorld import World
from BaseClasses import MultiWorld
from Options import Option, OptionGroup, PerGameCommonOptions

if TYPE_CHECKING:
    from ..Items import ManualItem
    from ..Locations import ManualLocation

from .Path import Path

class Hooks:
    hooks_dir_name: str = "hooks"
    package_name: str
    module_name: str

    is_extended: bool = True

    def __init__(self, module_name: str):
        path = Path()
        
        self.package_name = ".".join([path.worlds_dir_name, path.world_name, self.hooks_dir_name])
        self.module_name = module_name
        self.module = path.load_module(self.hooks_dir_name, self.module_name)

        if self.module_name == "Rules":
            self.is_extended = False # user-defined hooks are original, not extending preexisting methods

    def __getattr__(self, hook_func_name: str):
        if self.module is None:
            return
        try:
            module_func = getattr(self.module, hook_func_name)
        except ModuleNotFoundError: # the hook file itself doesn't exist
            return # nothing to do because no hook file, return
        except AttributeError: # the hook function doesn't exist in the user's specific hooks file
            return # nothing to do because no hook, return

        return module_func

    def call(self, hook_func_name: str, *args):
        if self.module is None:
            return
        if self.__class__.__name__ == "Hooks":
            raise TypeError("It is not intended to use the base Hooks class to call hook methods. Use the appropriate hook class instead.")

        if self.is_extended:
            original_func = getattr(self, hook_func_name, None)

            if not original_func: # non-existent method raises AttributeError, so raise that here as well
                raise AttributeError(f"The {self.module_name} hook '{hook_func_name}' is either misspelled or does not exist.")

        try:
            module_func = getattr(self.module, hook_func_name)
        except ModuleNotFoundError: # the hook file itself doesn't exist
            return # nothing to do because no hook file, return
        except AttributeError: # the hook function doesn't exist in the user's specific hooks file
            return # nothing to do because no hook, return

        try:
            return module_func(*args)
        except TypeError as e: # something went wrong, if possible give the user enough info to troubleshoot what they did wrong (and re-raise to deliver this info)
            if self.is_extended:
                func_signature = inspect.signature(original_func)
                func_params = str(func_signature).split(" -> ")[0] # alternative is func_signature.parameters, but is less readable
                func_return_type = func_signature.return_annotation

                if "inspect._empty" in str(func_return_type): # inspect._empty is effectively a None return type, or no return
                    func_return_type = None

                raise TypeError(
                    f"There is a problem with the hook function '{hook_func_name}'. This hook function expects the arguments {func_params}" +
                    f" and expects a return type of '{func_return_type}'." if func_return_type else "."
                )
            else:
                raise TypeError(
                    f"There is a problem with the user-created hook function '{hook_func_name}'. The error received was: {str(e)}" 
                )

        return

class DataHooks(Hooks):
    def __init__(self):
        super().__init__("Data")

    def after_load_game_file(self, game_table: dict) -> dict: pass
    def after_load_item_file(self, item_table: list) -> list: pass
    def after_load_progressive_item_file(self, progressive_item_table: list) -> list: pass
    def after_load_location_file(self, location_table: list) -> list: pass
    def after_load_region_file(self, region_table: dict) -> dict: pass
    def after_load_category_file(self, category_table: dict) -> dict: pass
    def after_load_option_file(self, option_table: dict) -> dict: pass
    def after_load_meta_file(self, meta_table: dict) -> dict: pass
    def hook_interpret_slot_data(self, world, player: int, slot_data: dict[str, any]) -> dict | bool: pass

class HelpersHooks(Hooks):
    def __init__(self):
        super().__init__("Helpers")

    def before_is_category_enabled(self, multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]: pass
    def before_is_item_enabled(self, multiworld: MultiWorld, player: int, item: "ManualItem") -> Optional[bool]: pass
    def before_is_location_enabled(self, multiworld: MultiWorld, player: int, location: "ManualLocation") -> Optional[bool]: pass

class OptionsHooks(Hooks):
    def __init__(self):
        super().__init__("Options")

    def before_options_defined(self, options: dict) -> dict: pass
    def after_options_defined(self, options: Type[PerGameCommonOptions]): pass
    def before_option_groups_created(self, groups: dict[str, list[Option]]) -> dict[str, list[Option]]: pass
    def after_option_groups_created(self, groups: list[OptionGroup]) -> list[OptionGroup]: pass

class RulesHooks(Hooks):
    def __init__(self):
        super().__init__("Rules")

class WorldHooks(Hooks):
    def __init__(self):
        super().__init__("World")

    def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool: pass
    def before_create_regions(world: World, multiworld: MultiWorld, player: int): pass
    def after_create_regions(world: World, multiworld: MultiWorld, player: int): pass
    def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list: pass
    def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list: pass
    def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list: pass
    def before_set_rules(world: World, multiworld: MultiWorld, player: int): pass
    def after_set_rules(world: World, multiworld: MultiWorld, player: int): pass
    def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str: pass
    def after_create_item(item: "ManualItem", world: World, multiworld: MultiWorld, player: int) -> "ManualItem": pass
    def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list: pass
    def after_generate_basic(world: World, multiworld: MultiWorld, player: int): pass
    def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict: pass
    def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict: pass
    def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None: pass
    def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None: pass
    def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None: pass

