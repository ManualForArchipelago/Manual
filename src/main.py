import sys
import asyncio

from nicegui import binding, ui

@binding.bindable_dataclass
class APConnection:
    connected: bool = False
    server: str = ""
    username: str = ""
    password: str = ""

    command_text: str = ""

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def send_command(self):
        pass

@ui.page('/')
def main_page():
    items_received = {
        "(no category)": [
            "Item Name 1",
            "Item Name 2"
        ],
        "My Category": [
            "Foo Item",
            "Bar Item"
        ]
    }

    locations_missing = {
        "(no category)": [
            "VICTORY! (goal complete)"
        ],
        "Blah Locations": [
            "Blah Location 1",
            "Blah Location 2",
            "Blah Location 3"
        ],
        "Blargh Loc": [
            "Loc 1",
            "Loc 2"
        ]
    }

    ui.dark_mode().enable()

    # Header
    connection = APConnection()
    connected = False

    ui.page_title("Client - Manual for Archipelago")
    with ui.header(elevated=True).classes("bg-purple-950"):
        with ui.row().classes("w-full"):
            # Header text
            ui.label("Client - Manual for Archipelago").classes("text-xl p-2")

            # Tab bar
            with ui.tabs().classes("pl-20") as tabs:
                tab_ap = ui.tab("Archipelago")
                tab_man = ui.tab("Manual")

            connection_details = ui.column()

            # show if connected
            with ui.row().bind_visibility_from(connection, "connected").classes("ml-auto text-base text-white"):
                with ui.row().classes("p-3"):
                    ui.label("Connected to")
                    ui.label().bind_text_from(connection, "server").classes("text-purple-300")
                    ui.label("as")
                    ui.label().bind_text_from(connection, "username").classes("text-purple-300")

                ui.button("Disconnect", on_click=connection.disconnect).classes("mt-2")

            # show if not connected
            with ui.row().classes("ml-auto").bind_visibility_from(connection, "connected", backward=lambda v: not v):
                ui.input("Server").bind_value(connection, "server").props("outlined dense").classes("mt-1")
                ui.input("Username").bind_value(connection, "username").props("outlined dense").classes("mt-1")
                ui.input("Password (optional)").bind_value(connection, "password").props("outlined dense").classes("mt-1")
                ui.button("Connect", on_click=connection.connect).classes("mt-1.5 !bg-blue-700")

    # Tab panels (value is default tab on load)
    with ui.tab_panels(tabs, value=tab_ap).classes("w-full"):
        # Tab panel "Archipelago" contents
        with ui.tab_panel(tab_ap):
            with ui.element('h2').classes('text-xl font-extrabold dark:text-white'):
                ui.label("Send Console Command")

            with ui.row().classes("w-full"):
                ui.label("Command:").classes("text-base font-extrabold mt-2")
                ui.input().bind_value(connection, "command_text").props("outlined dense").classes("w-1/2")
                ui.button("Send", on_click=connection.send_command).classes("mt-0.5 !bg-blue-700")

            with ui.element('h2').classes('text-xl font-extrabold dark:text-white mt-10'):
                ui.label("Console Output")

            with ui.list().props('bordered separator').classes("w-full"):
                ui.item("[Server] Welcome to the Manual client!")
                ui.item("[Server] To connect to an Archipelago server, use the connection form at the top right.")

        # Tab panel "Manual" contents
        with ui.tab_panel(tab_man):
            with ui.grid(columns=2).classes("w-full"):
                with ui.column():
                    with ui.element('h2').classes('text-xl font-extrabold dark:text-white'):
                        ui.label("Received Items (14)").classes("mb-3")

                        for cat in items_received.keys():
                            with ui.expansion(cat, icon="mark_email_read").classes("w-full text-sm bg-neutral-900 mb-1"):
                                for item_name in items_received[cat]:
                                    ui.label(item_name).classes("indent-10")

                with ui.column():
                    with ui.element('h2').classes('text-xl font-extrabold dark:text-white'):
                        ui.label("Remaining Locations (22)").classes("mb-3")

                        for cat in locations_missing.keys():
                            with ui.expansion(cat, icon="send").classes("w-full text-sm bg-neutral-900 mb-1"):
                                for location_name in locations_missing[cat]:
                                    ui.button(location_name, on_click=lambda: ui.notify("Location Send 123")).classes("!bg-blue-700")

#########
#
# old client stuff
#
#########

async def game_watcher_manual(ctx):
    while not ctx.exit_event.is_set():
        if ctx.ui:
            ctx.ui.check_for_requested_update()

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

async def main(args):
    config_file = {}
    # if args.apmanual_file:
    #     config_file = read_apmanual_file(args.apmanual_file)
    # ctx = ManualContext(args.connect, args.password, config_file.get("game"), config_file.get("player_name"))
    # ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    #
    # ctx.item_table = config_file.get("items", {})
    # ctx.location_table = config_file.get("locations", {})
    # ctx.region_table = config_file.get("regions", {})
    # ctx.category_table = config_file.get("categories", {})
    #
    # if tracker_loaded:
    #     ctx.run_generator()
    # if gui_enabled:
    #     ctx.run_gui()
    # ctx.run_cli()


    # progression_watcher = asyncio.create_task(
    #     game_watcher_manual(ctx), name="ManualProgressionWatcher")
    #
    # await ctx.exit_event.wait()
    # ctx.server_address = None
    #
    # await progression_watcher
    #
    # await ctx.shutdown()

def launch() -> None:
    #import colorama

    #parser = get_base_parser(description="Manual Client, for operating a Manual game in Archipelago.")
    #parser.add_argument('apmanual_file', default="", type=str, nargs="?",
    #                    help='Path to an APMANUAL file')

    args = sys.argv[1:]
    if "Manual Client" in args:
        args.remove("Manual Client")
    #args, rest = parser.parse_known_args(args=args)
    #colorama.init()
    asyncio.run(main(args))
    #colorama.deinit()

    # Run NiceGUI localhost web app
    #ui.run(native=True)
    ui.run(port=8928, reload=False)

# if __name__ in { '__main__', '__mp_main__' }:
    launch()
