import webbrowser

from typing import Callable, Optional

import Utils
from worlds.LauncherComponents import Component, SuffixIdentifier, components, Type, launch_subprocess, icon_paths

CLIENT_VERSION = 2026_01_08 # YYYYMMDD

def launch_client(*args):
    import CommonClient
    from .ManualClient import launch as Main

    if CommonClient.gui_enabled:
        launch_subprocess(Main, name="Manual client")
    else:
        Main()

class VersionedComponent(Component):
    def __init__(self, display_name: str, script_name: Optional[str] = None, func: Optional[Callable] = None, version: int = 0, file_identifier: Optional[Callable[[str], bool]] = None, icon: Optional[str] = None):
        super().__init__(display_name=display_name, script_name=script_name, func=func, component_type=Type.CLIENT, file_identifier=file_identifier, icon=icon)
        self.version = version

def add_client_to_launcher() -> None:
    found = False

    if "manual" not in icon_paths:
        icon_paths["manual"] = Utils.user_path('data', 'manual.png')

    discord_component = None
    for c in components:
        if c.display_name == "Manual Client":
            found = True
            if getattr(c, "version", 0) < CLIENT_VERSION:  # We have a newer version of the Manual Client than the one the last apworld added
                c.version = CLIENT_VERSION
                c.func = launch_client
                c.icon = "manual"
        elif c.display_name == "Manual Discord Server":
            discord_component = c

    if not found:
        components.append(VersionedComponent(f"Manual Client", "ManualClient", func=launch_client, version=CLIENT_VERSION, file_identifier=SuffixIdentifier('.apmanual'), icon="manual"))
    if not discord_component:
        components.append(Component("Manual Discord Server", "ManualDiscord", func=lambda: webbrowser.open("https://discord.gg/hm4rQnTzQ5"), icon="discord", component_type=Type.ADJUSTER))

add_client_to_launcher()
