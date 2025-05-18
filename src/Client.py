from __future__ import annotations

import asyncio
import copy
import json
import os
import random
import re
import requests
import sys
import time
import traceback
import typing
from collections import Counter
from typing import Any, Optional

# import AP's ModuleUpdate, which does a pip install among other things
# (Probably the place to find how to install nicegui pip package automatically for Manual client)
import ModuleUpdate
ModuleUpdate.update()

# import GUI library for Manual client
from nicegui import app, ui, Client

# import AP CommonClient skeleton and associated pieces
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, server_loop
from MultiServer import mark_raw
from NetUtils import ClientStatus, JSONtoTextParser, SlotType, HintStatus
import Utils
from worlds import AutoWorldRegister, network_data_package
from worlds.LauncherComponents import icon_paths
from kivy.app import App
from kivy.utils import escape_markup

# Universal Tracker initialization, if present
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext, TrackerCommandProcessor
    ClientCommandProcessor = TrackerCommandProcessor
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext
#from CommonClient import CommonContext as SuperContext

##########
#
# NiceGUI stuff to make the Manual client UI
#
##########

class NiceGUIJSONtoTextParser(JSONtoTextParser):
    # dummy class to absorb kvlang definitions
    class TextColors():
        pass

    def __init__(self, *args, **kwargs):
        # we grab the color definitions from the .kv file, then overwrite the JSONtoTextParser default entries
        colors = self.TextColors()
        color_codes = self.color_codes.copy()
        for name, code in color_codes.items():
            color_codes[name] = getattr(colors, name, code)
        self.color_codes = color_codes
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.ref_count = 0
        return super(NiceGUIJSONtoTextParser, self).__call__(*args, **kwargs)

    def _handle_item_name(self, node: JSONMessagePart):
        flags = node.get("flags", 0)
        item_types = []
        if flags & 0b001:  # advancement
            item_types.append("progression")
        if flags & 0b010:  # useful
            item_types.append("useful")
        if flags & 0b100:  # trap
            item_types.append("trap")
        if not item_types:
            item_types.append("normal")

        return super(NiceGUIJSONtoTextParser, self)._handle_item_name(node)

    def _handle_player_id(self, node: JSONMessagePart):
        player = int(node["text"])
        slot_info = self.ctx.slot_info.get(player, None)
        if slot_info:
            text = f"Game: {slot_info.game}<br>" \
                   f"Type: {SlotType(slot_info.type).name}"
            if slot_info.group_members:
                text += f"<br>Members:<br> " + "<br> ".join(
                    self._escape_markup(self.ctx.player_names[player])
                    for player in slot_info.group_members
                )
        return super(NiceGUIJSONtoTextParser, self)._handle_player_id(node)

    def _handle_color(self, node: JSONMessagePart):
        colors = node["color"].split(";")
        node["text"] = self._escape_markup(node["text"])
        for color in colors:
            color_code = self.color_codes.get(color, None)
            if color_code:
                node["text"] = f"[color={color_code}]{node['text']}[/color]"
                return self._handle_text(node)
        return self._handle_text(node)

    def _handle_text(self, node: JSONMessagePart):
        # All other text goes through _handle_color, and we don't want to escape markup twice,
        # or mess up text that already has intentional markup applied to it
        if node.get("type", "text") == "text":
            node["text"] = self._escape_markup(node["text"])
        return super(NiceGUIJSONtoTextParser, self)._handle_text(node)

    def _escape_markup(self, text: str):
        escaped_text = escape_markup(text)

        return escaped_text.replace("&bl;", "(").replace("&br;", ")")

class APConnection:
    ctx: ManualContext

    connected: bool = False
    server_address: str = ""
    username: str = ""
    password: str = ""
    game: str = ""

    messages: list = [
        "Welcome to the Manual client!",
        "To connect to an Archipelago server, use the connection form at the top right."
    ]
    messages_max_display: int = 50
    json_to_message_parser: NiceGUIJSONtoTextParser

    command_text: str = ""
    error_text: str = ""
    error_traceback: str = ""

    search_text: str = ""
    sort_order_items: str = "alpha"
    sort_order_locations: str = "alpha"
    expansion_visibility: dict = {}
    exclude_found_hints: bool = False

    item_categories: list = []
    location_categories: list = []
    victory_categories: list = []
    victory_location: str = ""

    items_received_previous: list = None
    update_requested_time: float = None

    def __init__(self, ctx: ManualContext):
        self.ctx = ctx
        self.json_to_message_parser = NiceGUIJSONtoTextParser(ctx)

    def init_items_and_locations(self):
        # seed all category names to start
        item_categories = set(["(No Category)"])
        location_categories = set(["(No Category)", "(Hinted)"])

        for item in self.ctx.item_table.values() or AutoWorldRegister.world_types[self.ctx.game].item_name_to_item.values():
            if "category" in item and len(item["category"]) > 0:
                for category in item["category"]:
                    category_settings = self.ctx.category_table.get(category) or getattr(AutoWorldRegister.world_types[self.ctx.game], "category_table", {}).get(category, {})

                    if "hidden" in category_settings and category_settings["hidden"]:
                        continue

                    item_categories.add(category)

        if not self.ctx.location_table and not hasattr(AutoWorldRegister.world_types[self.ctx.game], 'location_name_to_location'):
            raise Exception("The apworld for %s is too outdated for this client. Please update it." % (self.ctx.game))

        for location_id in self.ctx.missing_locations:
            location_name = self.ctx.location_names.lookup_in_game(location_id)
            location = self.ctx.get_location_by_name(location_name)

            if not location:
                continue

            if "category" in location and len(location["category"]) > 0:
                for category in location["category"]:
                    category_settings = self.ctx.category_table.get(category) or getattr(AutoWorldRegister.world_types[self.ctx.game], "category_table", {}).get(category, {})

                    if category_settings.get("hidden", False):
                        continue

                    location_categories.add(category)

        self.item_categories = sorted(item_categories)
        self.location_categories = sorted(location_categories)

        victory_location = self.ctx.goal_location
        victory_categories = set(victory_location.get("category", {}))

    def add_message(self, new_message: str):
        self.messages.append(new_message)
        self.messages = self.messages[-self.messages_max_display:]

        self.display_messages.refresh()

    @ui.refreshable
    def display_messages(self):
        for message in self.messages[-self.messages_max_display:]:
            message_parts = re.findall(r'((\[color=.+?\])?([^\[]+)(\[\/color\])?)', message)

            with ui.item():
                for message_part in message_parts:
                    color = None
                    text = message_part[0]

                    if message_part[1] != '':
                        color = re.search(r'\[color=(.+?)\]', message_part[1])
                        text = message_part[2]

                    if color:
                        ui.label(text).style(f'color: #{color.group(1)}; white-space: pre-wrap').classes('mt-1 text-base')
                    else:
                        ui.label(text).style('white-space: pre-wrap').classes('mt-1 text-base')

        ui.timer(0.01, lambda: console_scroll.scroll_to(percent=1e6), once=True)

    @ui.refreshable
    def display_items(self):
        if not self.connected:
            ui.label("Waiting for connection")
            return

        if self.sort_order_items == "numeric":
            sort_fn = lambda i: i
        else:
            sort_fn = self.ctx.item_names.lookup_in_game

        sorted_items_received = sorted([
            i.item for i in self.ctx.items_received
        ], key=sort_fn)

        items_length = len(sorted_items_received)

        if self.search_text:
            sorted_items_received = sorted([
                i.item for i in self.ctx.items_received
                    if self.search_text.lower() in self.ctx.item_names.lookup_in_game(i.item).lower()
            ], key=sort_fn)

            items_length = len(sorted_items_received)

        with ui.element('h2').classes('w-full text-xl font-extrabold dark:text-white'):
            with ui.row().classes('w-full justify-between'):
                ui.label(f"Received Items ({items_length})").classes("mb-3")

                with ui.row().classes('w-fit -mt-1 ml-auto'):
                    ui.label("Sort By: ").classes("text-sm font-bold mt-2")
                    ui.toggle(["alpha", "numeric"], value=self.sort_order_items, on_change=self.request_refresh_lists).props('toggle-color="blue-700"').classes("text-sm font-normal bg-blue-950").bind_value(self, 'sort_order_items')

        items_received_data = {}

        for i in sorted_items_received:
            item_name = self.ctx.item_names.lookup_in_game(i)
            item_data = self.ctx.get_item_by_name(item_name)
            item_count = sorted_items_received.count(i)

            items_received_data[i] = {
                'id': i,
                'name': item_name,
                'data': item_data,
                'count': item_count
            }

        new_items = self._get_new_item_ids()

        print("new items are: ")
        print(new_items)

        for category_name in self.item_categories:
            items_in_category = [
                i for i in items_received_data.values()
                    if category_name in i['data'].get('category', []) or
                        (category_name == '(No Category)' and i['data'].get('category', []) == [])
            ]
            item_count_in_category = sum([i['count'] for i in items_in_category])

            new_in_cat_classes = "font-bold !text-yellow-300" if set([i['id'] for i in items_in_category]).intersection(new_items) else "font-normal"

            with ui.expansion(f"{category_name} ({item_count_in_category})", icon="mark_email_read").props(f'header-class="text-base {new_in_cat_classes}"').classes("w-full bg-neutral-900").bind_value(self.expansion_visibility, f"itemcategory_{category_name}"):
                listed_items = set()

                for item in items_in_category:
                    network_item = item['id']

                    new_item_classes = "font-bold text-yellow-300" if network_item in new_items else "font-normal text-white-300"
                    ui.label(f"{item['name']} ({item['count']})").classes(f"indent-10 {new_item_classes}")
                    listed_items.add(item['name'])

        print("done displaying items")
        self.update_items_received_ids()

    @ui.refreshable
    def display_locations(self):
        if not self.connected:
            return # "waiting for conn" is shown in items column, so just return

        if self.sort_order_items == "numeric":
            sort_fn = lambda i: i
        else:
            sort_fn = self.ctx.location_names.lookup_in_game

        locations_length = len(self.ctx.missing_locations)

        sorted_locations_missing = sorted([
            l for l in self.ctx.missing_locations
        ], key=sort_fn)

        if self.search_text:
            locations_length = len([
                l for l in self.ctx.missing_locations
                    if self.search_text.lower() in self.ctx.location_names.lookup_in_game(l).lower()
            ])

            sorted_locations_missing = sorted([
                l for l in sorted_locations_missing
                    if self.search_text.lower() in self.ctx.location_names.lookup_in_game(l).lower()
            ], key=sort_fn)

        locations_missing_data = {}

        for l in sorted_locations_missing:
            location_name = self.ctx.location_names.lookup_in_game(l)
            location_data = self.ctx.get_location_by_name(location_name)

            locations_missing_data[l] = {
                'id': l,
                'name': location_name,
                'data': location_data,
            }

        with ui.element('h2').classes('w-full text-xl font-extrabold dark:text-white'):
            with ui.row().classes('w-full justify-between'):
                ui.label(f"Remaining Locations ({locations_length})").classes("mb-3")

                with ui.row().classes('w-fit -mt-1 ml-auto'):
                    ui.label("Sort By: ").classes("text-sm font-bold mt-2")
                    ui.toggle(["alpha", "numeric"], value=self.sort_order_locations, on_change=self.request_refresh_lists).props('toggle-color="blue-700"').classes("text-sm font-normal bg-blue-950").bind_value(self, 'sort_order_locations')

        for category_name in self.location_categories:
            locations_in_category = [
                l for l in locations_missing_data.values()
                    if category_name in l['data'].get('category', []) or
                        (category_name == '(No Category)' and l['data'].get('category', []) == [])
            ]
            location_count_in_category = len(locations_in_category)

            print(f"locations in cat ({category_name}) vs. reachable:")
            print(set([l['name'] for l in locations_in_category]))
            print(self.ctx.tracker_reachable_locations)

            reachable_cat_classes = "font-bold bg-green-700" if set([l['name'] for l in locations_in_category]).intersection(self.ctx.tracker_reachable_locations) else "font-normal bg-neutral-900"

            show_victory_button = False

            if category_name in self.victory_categories or (not self.victory_categories and category_name == "(No Category)"):
                show_victory_button = True
                location_count_in_category += 1

            with ui.expansion(f"{category_name} ({location_count_in_category})", group="loc_group", icon="send").props(f'header-class="text-base {reachable_cat_classes}"').classes("w-full").bind_value(self.expansion_visibility, f"locationcategory_{category_name}"):
                listed_locations = set()

                for location in locations_in_category:
                    location_id = location['id']

                    reachable_loc_classes = "font-bold !bg-green-700" if location['name'] in self.ctx.tracker_reachable_locations else "font-normal !bg-blue-700"

                    ui.button(location['name'], on_click=lambda e, loc_id=location_id: self.send_location(e.sender, loc_id)).classes(f"w-9/10 {reachable_loc_classes}")
                    listed_locations.add(location['name'])

                # if this is the category that Victory is in, display the Victory button
                if show_victory_button:
                    victory_text = "VICTORY! (seed finished)" if self.victory_location == "__Manual Game Complete__" else "GOAL: " + self.victory_location

                    reachable_loc_classes = "font-bold !bg-green-700" if self.victory_location in self.ctx.tracker_reachable_locations else "font-normal !bg-blue-700"

                    ui.button(victory_text, on_click=lambda e: self.send_victory(e.sender)).classes(reachable_loc_classes)

    @ui.refreshable
    def display_game_selector(self):
        manuals = [w for w in AutoWorldRegister.world_types.keys() if "Manual_" in w]
        manuals.sort()  # Sort by alphabetical order, not load order

        ui.select(options=manuals, with_input=True, label='Game').bind_value(connection, "game").props("outlined dense").classes("!bg-blue-700 mt-1")

    @ui.refreshable
    def display_error(self):
        if self.error_text == "":
            return

        with ui.dialog() as dialog, ui.card():
            ui.label(self.error_text).classes('text-base font-extrabold')
            ui.label(self.error_traceback).style('white-space: pre-wrap')
            ui.button('Close', on_click=dialog.close)

            dialog.open()

    @ui.refreshable
    def display_reachable_locations(self):
        if not self.ctx.tracker_reachable_locations:
            ui.item("No locations to show currently.").classes('mt-1 text-base')
            return

        for reachable_location in self.ctx.tracker_reachable_locations:
            with ui.item():
                ui.label(reachable_location).classes('mt-1 text-base')

    @ui.refreshable
    def display_hints(self):
        hints = self.ctx.get_hints()

        if not hints:
            ui.item("No hints yet.")
            return

        if self.exclude_found_hints:
            hints = [h for h in hints if not h.get("found")]

        table_columns = [
            { "name": "receiving_player", "field": "receiving_player", "label": "Receiving Player", 'align': 'left', "sortable": True },
            { "name": "item", "field": "item", "label": "Item", 'align': 'left', "sortable": True },
            { "name": "finding_player", "field": "finding_player", "label": "Finding Player", 'align': 'left', "sortable": True },
            { "name": "location", "field": "location", 'align': 'left', "label": "Location" },
            { "name": "entrance", "field": "entrance", 'align': 'left', "label": "Entrance" },
            { "name": "status", "field": "status", "label": "Status", 'align': 'left', "sortable": True }
        ]

        table_rows = [
            {
                "receiving_player": self.ctx.player_names[h['receiving_player']],
                "item": self.ctx.item_names.lookup_in_slot(h['item'], h['receiving_player']),
                "finding_player": self.ctx.player_names[h['finding_player']],
                "location": self.ctx.location_names.lookup_in_slot(h['location'], h['finding_player']),
                "entrance": h['entrance'] if h['entrance'] else 'Vanilla',
                "status": HintStatus(h['status']).name.replace("HINT_", "")
            }
            for h in hints
        ]

        table_font_size = "1.1em"

        ui.table(columns=table_columns, rows=table_rows).classes("w-full text-base")
        ui.query('th').classes('!bg-teal-950').style(f'font-size: {table_font_size};')
        ui.query('td').classes('!bg-zinc-200').style(f'font-size: {table_font_size};')

        # status == status || found

        #[{'receiving_player': 1, 'finding_player': 1, 'location': 17602652530, 'item': 17602652026, 'found': False, 'entrance': '', 'item_flags': 1, 'status': 30, 'class': 'Hint'}]

            # data.append({
            #     "receiving": {"text": self.parser.handle_node({"type": "player_id", "text": hint["receiving_player"]})},
            #     "item": {"text": self.parser.handle_node({
            #         "type": "item_id",
            #         "text": hint["item"],
            #         "flags": hint["item_flags"],
            #         "player": hint["receiving_player"],
            #     })},
            #     "finding": {"text": self.parser.handle_node({"type": "player_id", "text": hint["finding_player"]})},
            #     "location": {"text": self.parser.handle_node({
            #         "type": "location_id",
            #         "text": hint["location"],
            #         "player": hint["finding_player"],
            #     })},
            #     "entrance": {"text": self.parser.handle_node({"type": "color" if hint["entrance"] else "text",
            #                                                   "color": "blue", "text": hint["entrance"]
            #                                                   if hint["entrance"] else "Vanilla"})},
            #     "status": {
            #         "text": hint_status_node,
            #         "hint": hint,
            #     },
            # })



    def check_for_requested_refresh(self):
        current_time = time.time()

        # wait 0.25 seconds before executing update, in case there are multiple update requests coming in
        if self.update_requested_time and current_time - self.update_requested_time >= 0.25:
            self.update_requested_time = None

            self.show_item_notifications()
            self.refresh_lists()

    def request_refresh_lists(self):
        self.update_requested_time = time.time()

    def refresh_lists(self):
        # if the last received items is not null (so, not a new launch) and there are no new items, then we already updated
        #if self.items_received_previous != None and self._get_new_item_ids == []:
        #    return

        self.display_items.refresh()
        self.display_locations.refresh()
        self.display_reachable_locations.refresh()
        self.display_hints.refresh()

    def show_item_notifications(self):
        if self.items_received_previous == None:
            return

        new_items = self._get_new_item_ids()

        with container:
            for item in new_items:
                item_name = self.ctx.item_names.lookup_in_game(item)

                ui.notify(f"Received: {item_name}")

    def update_items_received_ids(self):
        print("updating received item ids")

        self.items_received_previous = [i.item for i in self.ctx.items_received]

    def _get_new_item_ids(self):
        items_received_ids = [i.item for i in self.ctx.items_received]

        if self.items_received_previous == None:
            return []

        print("items_received_ids: ")
        print(items_received_ids)
        print("items received previous: ")
        print(self.items_received_previous)

        counter_current = Counter(items_received_ids)
        counter_previous = Counter(self.items_received_previous)
        difference = list((counter_current - counter_previous).elements())

        return difference or []

    async def connect(self):
        self.ctx.server_address = self.server_address
        self.ctx.username = self.username
        self.ctx.password = self.password
        self.ctx.game = self.game

        await self.ctx.connect()

        # self.connected is set to True in the on_package method of context

    async def disconnect(self):
        await self.ctx.disconnect()
        self.connected = False

        self.add_message("Disconnected.")

    async def send_command(self):
        await self.ctx.send_msgs([{"cmd": "Say", "text": self.command_text }])
        self.command_text = ""

    async def send_location(self, btn: ui.button, location_id: int):
        if btn.text not in self.ctx.location_names_to_id:
            raise Exception("Locations were not loaded correctly. Please reconnect your client.")

        self.ctx.locations_checked.append(location_id)
        self.ctx.syncing = True
        btn.delete()

        pass

    async def send_victory(self, btn: ui.button):
        self.ctx.items_received.append("__Victory__")
        self.ctx.syncing = True


@ui.page('/')
async def index(client: Client):

    # Old client stuff below

    parser = get_base_parser(description="Manual Client, for operating a Manual game in Archipelago.")
    parser.add_argument('apmanual_file', default="", type=str, nargs="?",
                        help='Path to an APMANUAL file')

    args = sys.argv[1:]
    if "Manual Client" in args:
        args.remove("Manual Client")
    args, rest = parser.parse_known_args(args=args)
    main(args)

    # NiceGUI layout from here

    ui.dark_mode().enable()
    ui.page_title("Client - Manual for Archipelago")

    with ui.header(elevated=True).classes("bg-purple-950"):
        with ui.row().classes("w-full"):
            # Header text
            ui.image("https://raw.githubusercontent.com/ManualForArchipelago/ManualBuilder/refs/heads/main/images/ap-manual-discord-logo-square-96x96.png").classes("w-[48px] border-[3px] border-purple-500/75 -mt-1/2 rounded-lg")
            ui.label("Manual").classes("font-serif italic text-3xl tracking-tighter p-2.5 text-purple-500/50 -ml-1 -mt-1")

            # Tab bar
            with ui.tabs().classes("pl-20") as tabs:
                tab_console = ui.tab("Console")
                tab_items_and_locations = ui.tab("Items and Locations")
                tab_locations_in_logic = ui.tab("Locations in Logic")
                tab_hints = ui.tab("Hints")

            connection_details = ui.column()

            # show if connected
            with ui.row().bind_visibility_from(connection, "connected").classes("ml-auto text-base text-white"):
                with ui.column().classes("h-10"):
                    with ui.row().classes("h-3"):
                        ui.label("Playing ")
                        ui.label().bind_text_from(connection, "game", backward=lambda game: re.sub(r'\_([^_]+)$', r' (by \1)', game.replace("Manual_", ""))).classes("text-purple-300")
                        ui.label("as")
                        ui.label().bind_text_from(connection, "username").classes("text-purple-300")

                        ui.button("Disconnect", on_click=connection.disconnect).classes("mt-2")

                    with ui.row().classes("h-3"):
                        ui.label().bind_text_from(connection, "server_address").classes("text-yellow-300")


            # show if not connected
            with ui.row().classes("ml-auto").bind_visibility_from(connection, "connected", backward=lambda v: not v):
                connection.display_game_selector()

                ui.input("Server").bind_value(connection, "server_address").props("outlined dense").classes("mt-1")
                ui.input("Username").bind_value(connection, "username").props("outlined dense").classes("mt-1")
                ui.input("Password (optional)").bind_value(connection, "password").props("outlined dense").classes("mt-1")

                ui.button("Connect", on_click=connection.connect).classes("mt-1.5 !bg-blue-700")

    global container
    with ui.row().classes("w-full h-full") as container:
        # Tab panels (value is default tab on load)
        tab_transition = "jump-right"

        with ui.tab_panels(tabs, value=tab_console).props(f'transition-prev="{tab_transition}" transition-next="{tab_transition}"').classes("w-full"):
            # Tab panel "Console" contents
            with ui.tab_panel(tab_console).classes("!pb-8"):
                with ui.element('h2').classes('text-xl font-extrabold dark:text-white'):
                    ui.label("Send Console Command")

                with ui.row().classes("w-full"):
                    ui.label("Command:").classes("text-base font-extrabold mt-2")
                    ui.input().bind_value(connection, "command_text").props("clearable outlined dense").classes("w-1/2")
                    ui.button("Send", on_click=connection.send_command).classes("mt-0.5 !bg-blue-700")

                with ui.element('h2').classes('text-xl font-extrabold dark:text-white mt-10'):
                    ui.label("Console Output")

                global console_scroll
                with ui.scroll_area().props('visible bar-style="background-color:#ccc"').classes("h-[500px]") as console_scroll:
                    with ui.list().props('bordered separator').classes("w-full"):
                        connection.display_messages()

            # Tab panel "Items and Locations" contents
            with ui.tab_panel(tab_items_and_locations):
                with ui.row().classes("w-full bg-teal-950 px-5 py-2"):
                    ui.label("Search: ").classes("text-base mt-2 font-bold")
                    ui.input(value=connection.search_text, on_change=connection.request_refresh_lists).bind_value(connection, "search_text").props("clearable outlined dense")

                with ui.grid(columns=2).classes("w-full"):
                    with ui.column().style('row-gap: 0.2rem'):
                        connection.display_items()

                    with ui.column().style('row-gap: 0.2rem'):
                        connection.display_locations()

            # Tab panel "Locations In Logic" contents
            with ui.tab_panel(tab_locations_in_logic).classes("!pb-8"):
                with ui.element('h2').classes('text-xl font-extrabold dark:text-white p-0'):
                    ui.label("Locations in Logic")

                ui.label("Powered by Universal Tracker").classes('!text-sky-500 p-0 -mt-3')

                with ui.scroll_area().props('visible bar-style="background-color:#ccc"').classes("h-[500px]"):
                    with ui.list().props('bordered separator').classes("w-full"):
                        connection.display_reachable_locations()

            # Tab panel "Hints" contents
            with ui.tab_panel(tab_hints).classes("!pb-8"):
                with ui.element('h2').classes('text-xl font-extrabold dark:text-white p-0'):
                    ui.label("Hints")

                ui.switch("Exclude Found Hints", value=connection.exclude_found_hints, on_change=connection.request_refresh_lists).bind_value(connection, "exclude_found_hints").classes("text-base")

                connection.display_hints()

        connection.display_error()

    # NiceGUI-related: client.disconnected is true when the user closes the browser window, then we shutdown the app
    await client.disconnected()
    app.shutdown() # shutdown NiceGUI
    await connection.ctx.shutdown() # shutdown CommonClient context


#########
#
# Objects to tie into CommonClient's networking capabilities
#
#########

class ManualClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self) -> bool:
        """Manually trigger a resync."""
        self.output("Syncing items.")
        self.ctx.syncing = True
        return True

    @mark_raw
    def _cmd_send(self, location_name: str) -> bool:
        """Send a check"""
        names = self.ctx.location_names_to_id.keys()
        location_name, usable, response = Utils.get_intended_text(
            location_name,
            names
        )
        if usable:
            location_id = self.ctx.location_names_to_id[location_name]
            self.ctx.locations_checked.append(location_id)
            self.ctx.syncing = True
        else:
            self.output(response)
            return False


class ManualContext(SuperContext):
    command_processor = ManualClientCommandProcessor
    game = "not set"  # this is changed in server_auth below based on user input
    items_handling = 0b111  # full remote
    tags = {"AP"}

    location_table = {}
    item_table = {}
    region_table = {}
    category_table = {}

    tracker_reachable_locations = []
    tracker_reachable_events = []

    set_deathlink = False
    last_death_link = 0
    deathlink_out = False

    search_text = ""

    colors = {
        'location_default': [219/255, 218/255, 213/255, 1],
        'location_in_logic': [2/255, 242/255, 42/255, 1],
        'category_even_default': [0.5, 0.5, 0.5, 0.1],
        'category_odd_default': [1.0, 1.0, 1.0, 0.0],
        'category_in_logic': [2/255, 82/255, 2/255, 1],
        'deathlink_received': [1, 0, 0, 1],
        'deathlink_primed': [1, 1, 1, 1],
        'deathlink_sent': [0, 1, 0, 1],
        'game_select_button': [200/255, 200/255, 200/255, 1],
        'header_background': [15/255, 80/255, 112/255, 1]
    }

    def __init__(self, server_address, password, game, player_name) -> None:
        super(ManualContext, self).__init__(server_address, password)

        print("tracker loaded is: ")
        print(tracker_loaded)

        if tracker_loaded:
            super().set_callback(self.on_tracker_updated) # Universal Tracker takes this func and calls it when updateTracker is called
            if hasattr(self, "set_events_callback"):
                super().set_events_callback(self.on_tracker_events) # Universal Tracker takes this func and calls it when events are calculated

        self.send_index: int = 0
        self.syncing = False
        self.game = game
        self.username = player_name

        self.ui = self.make_gui()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ManualContext, self).server_auth(password_requested)

        if "Manual_" not in self.game:
            raise Exception("The Manual client can only be used for Manual games.")

        world = AutoWorldRegister.world_types.get(self.game)
        if not self.location_table and not self.item_table and world is None:
            raise Exception(f"Cannot load {self.game}, please add the apworld to lib/worlds/")

        data_package = network_data_package["games"].get(self.game, {})

        self.update_ids(data_package)

        if world is not None and hasattr(world, "victory_names"):
            self.victory_names = world.victory_names
            self.goal_location = self.get_location_by_name(world.victory_names[0])
        else:
            self.victory_names = ["__Manual Game Complete__"]
            self.goal_location = self.get_location_by_name("__Manual Game Complete__")

        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(ManualContext, self).connection_closed()

    @property
    def suggested_game(self) -> str:
        if self.game:
            return self.game
        from .Game import game_name  # This will at least give us the name of a manual they've installed
        return Utils.persistent_load().get("client", {}).get("last_manual_game", game_name)

    def get_location_by_name(self, name) -> dict[str, Any]:
        location = self.location_table.get(name)
        if not location:
            # It is absolutely possible to pull categories from the data_package via self.update_game. I have not done this yet.
            location = AutoWorldRegister.world_types[self.game].location_name_to_location.get(name, {"name": name})
        return location

    def get_location_by_id(self, id) -> dict[str, Any]:
        name = self.location_names.lookup_in_game(id)
        return self.get_location_by_name(name)

    def get_item_by_name(self, name):
        item = self.item_table.get(name)
        if not item:
            item = AutoWorldRegister.world_types[self.game].item_name_to_item.get(name, {"name": name})
        return item

    def get_item_by_id(self, id):
        name = self.item_names.lookup_in_game(id)
        return self.get_item_by_name(name)

    def update_ids(self, data_package) -> None:
        self.location_names_to_id = data_package['location_name_to_id']
        self.item_names_to_id = data_package['item_name_to_id']

    def update_data_package(self, data_package: dict):
        super().update_data_package(data_package)
        for game, game_data in data_package["games"].items():
            if game == self.game:
                self.update_ids(game_data)

    def get_hints(self):
        print("getting hints")
        hints = self.stored_data.get(f"_read_hints_{self.team}_{self.slot}", [])
        print("hints are: ")
        print(hints)

        return hints

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(ManualContext, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd in {"Connected", "DataPackage"}:
            if cmd == "Connected":
                Utils.persistent_store("client", "last_manual_game", self.game)
                goal = args["slot_data"].get("goal")
                if goal and goal < len(self.victory_names):
                    self.goal_location = self.get_location_by_name(self.victory_names[goal])
                if args['slot_data'].get('death_link'):
                    #self.ui.enable_death_link()
                    self.set_deathlink = True
                    self.last_death_link = 0
                logger.info(f"Slot data: {args['slot_data']}")

                connection.connected = True

            print("[on_package] connected or datapackage")

            connection.init_items_and_locations()
        elif cmd in {"ReceivedItems"}:
            print("[on_package] receiveditems")

            connection.request_refresh_lists()
        elif cmd in {"RoomUpdate"}:
            print("[on_package] roomupdate")

            connection.request_refresh_lists()

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)
        #self.ui.death_link_button.text = f"Death Link: {data['source']}"
        #self.ui.death_link_button.background_color = self.colors['deathlink_received']

    def on_tracker_updated(self, reachable_locations: list[str]):
        self.tracker_reachable_locations = reachable_locations
        print("reachable locations:")
        print(reachable_locations)
        connection.request_refresh_lists()

    def on_tracker_events(self, events: list[str]):
        self.tracker_reachable_events = events

        if events:
            connection.request_refresh_lists()

    def handle_connection_loss(self, msg: str) -> None:
        """Helper for logging and displaying a loss of connection. Must be called from an except block."""
        exc_info = sys.exc_info()
        logger.exception(msg, exc_info=exc_info, extra={'compact_gui': True})
        tracker_error = False
        e = exc_info[2]
        formatted_tb = ''.join(traceback.format_tb(e))
        while e:
            if '/tracker/' in e.tb_frame.f_code.co_filename:
                tracker_error = True
                break
            e = e.tb_next

        if tracker_error:
            connection.error_text = "A Universal Tracker error has occurred. Please ensure that your version of UT matches your version of Archipelago."
            connection.error_traceback = formatted_tb
        else:
            connection.error_text = msg
            connection.error_traceback = formatted_tb

        connection.display_error.refresh()

    def run_gui(self):
        # CommonClient ui is only used to detect if a UI is present, so perhaps we can just let it "do its thing"?
        ui_class = self.make_gui()
        self.ui = ui_class(self)

        # CommonClient ui_task is only used to keep track of a process that needs awaiting in the case of shutdown
        # so we can just manually handle shutdown instead
        self.ui_task = None

    def make_gui(self) -> typing.Type["kvui.GameManager"]:
        ui_class = super().make_gui()

        class ManualManager(ui_class):
            base_title = "Archipelago Manual Client"
            ctx: ManualContext

            def __init__(self, ctx):
                super().__init__(ctx)

            # Not using Kivy client's address bar, so just sinkhole this function
            def update_address_bar(self, text): pass
            # No hints tab, so sinkhole this function too
            def update_hints(self): pass

            def print_json(self, data):
                parsed_data = connection.json_to_message_parser(copy.deepcopy(data))

                connection.add_message(parsed_data)

        return ManualManager

###

async def game_watcher_manual(ctx):
    while not ctx.exit_event.is_set():
        if connection:
            connection.check_for_requested_refresh()

        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False

        if ctx.set_deathlink:
            ctx.set_deathlink = False
            await ctx.update_death_link(True)

        if ctx.deathlink_out:
            ctx.deathlink_out = False
            await ctx.send_death()

        sending = []
        victory = ("__Victory__" in ctx.items_received)
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)

def read_apmanual_file(apmanual_file):
    from base64 import b64decode

    with open(apmanual_file, 'r') as f:
        return json.loads(b64decode(f.read()))

def create_icon_if_missing():
    if not os.path.exists(icon_paths["manual"]):
        # Download the icon for next time
        icon_url = "https://manualforarchipelago.github.io/ManualBuilder/images/ap-manual-discord-logo-square-96x96.png"
        with open(icon_paths["manual"], 'wb') as f:
            f.write(requests.get(icon_url).content)

def main(args):
    config_file = {}
    if args.apmanual_file:
        config_file = read_apmanual_file(args.apmanual_file)
    ctx = ManualContext(args.connect, args.password, config_file.get("game"), config_file.get("player_name"))
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    ctx.item_table = config_file.get("items", {})
    ctx.location_table = config_file.get("locations", {})
    ctx.region_table = config_file.get("regions", {})
    ctx.category_table = config_file.get("categories", {})

    if tracker_loaded:
        ctx.run_generator()

    # Haven't tested CLI yet.
    #
    #if CommonClient.gui_enabled:
    ctx.run_gui()

    ctx.run_cli()

    progression_watcher = asyncio.create_task(
        game_watcher_manual(ctx), name="ManualProgressionWatcher")

    ctx.server_address = None

    # Give the NiceGUI custom connection class the CommonContext to use, and make connection global
    global connection
    connection = APConnection(ctx)
    # [TODO] remove, just for testing
    connection.server_address = "localhost:38281"
    connection.username = "Fuzzy"
    connection.game = "Manual_WordFactori_Fuzzy"

def launch() -> None:
    create_icon_if_missing()

    # NiceGUI doesn't play well with subprocess launching, and not launching it as a subprocess blocks the Launcher process.
    # So close the Launcher so our client doesn't block its process. Maybe can figure out subprocess things later.
    launcher = App.get_running_app()
    launcher.stop()

    # Run NiceGUI stuff. There's a native window flag, but it requires installing Qt, etc. Can figure out later.
    ui.run(port=random.randint(8000, 9000), reload=False)

if __name__ in { '__main__', '__mp_main__' }:
    launch()
