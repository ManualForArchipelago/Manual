import os

class Path:
    path: str

    worlds_dir_name: str
    world_name: str

    def __init__(self):
        self.path = os.path.abspath(__file__)
        self.worlds_dir_name = self._get_world_dir()
        self.world_name = self._get_world_name()

    def _get_world_dir(self):
        path_parts = self.path.split("/")

        if "custom_worlds" in path_parts:
            return "custom_worlds"
        elif "lib" in path_parts:
            return "lib/worlds"
        else:
            return "worlds"

    def _get_world_name(self):
        path_parts = self.path.split("/")

        return [p for p in path_parts if "manual_" in p][0]

