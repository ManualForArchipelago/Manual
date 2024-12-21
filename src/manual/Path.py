import importlib
import importlib.util
import os
import sys
import warnings
import zipimport
from worlds import world_sources, WorldSource

class Path:
    path: str

    worlds_dir_name: str
    world_name: str
    world_source: WorldSource

    def __init__(self):
        self.path = os.path.abspath(__file__)
        self.worlds_dir_name = self._get_world_dir()
        self.world_name = self._get_world_name()
        self.world_source = self._get_world_source()

    def _get_world_dir(self):
        return __spec__.name.split(".")[0]

    def _get_world_name(self):
        return __spec__.name.split(".")[1]
    
    def _get_world_source(self):
        for source in world_sources:
            if source.path == self.world_name:
                return source
            if source.is_zip and os.path.basename(source.path) == self.world_name + '.apworld':
                return source
        return None

    def load_module(self, hooks_dir_name: str, module_name: str):
        package_name = ".".join([self.worlds_dir_name, self.world_name, hooks_dir_name])
        full_module_name = f"{package_name}.{module_name}"
        if full_module_name in sys.modules:
            return sys.modules[full_module_name]
        try:
            if self.world_source.is_zip:
                importer = zipimport.zipimporter(self.world_source.resolved_path)
                spec = importer.find_spec(f"{self.world_name}/{hooks_dir_name}")
                if spec is None:
                    print(f"WARNING: {self.world_name}.{hooks_dir_name} is None")
                    return None
                spec = importer.find_spec(f"{self.world_name}/{hooks_dir_name}/{module_name}")
                if spec is None:
                    print(f"{self.world_name}.{hooks_dir_name}.{module_name} is None")
                    return None
                mod = importlib.util.module_from_spec(spec)
                mod.__package__ = f"worlds.{mod.__package__}"

                mod.__name__ = f"worlds.{mod.__name__}"
                sys.modules[mod.__name__] = mod
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", message="__package__ != __spec__.parent")
                    # Found no equivalent for < 3.10
                    if hasattr(importer, "exec_module"):
                        importer.exec_module(mod)
                return mod
            
            return importlib.import_module(full_module_name, package_name)
        except ModuleNotFoundError:
            return None
