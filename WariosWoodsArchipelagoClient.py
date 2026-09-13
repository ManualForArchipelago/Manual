

#Hi! This is my Client Subclass. It extends CommonContext, from Archipelago's CommonClient.py.
#If you use this in any capacity, reference or copy/paste or whatever, let me know!! It would make me happy to hear it was helpful~ <33

#Happy to answer any questions! Ask them in the game's topic post within the official Archipelago Discord server.

#CCtheOwl 9/11/2026


import asyncio #Turns this into more than just a script! Now it's multithreaded!
import base64 #One of the many fun little ways I format data before sending it to Lua.
import importlib.resources
import json
import os
import shutil
import subprocess
import tempfile
import Utils
import kvui #I know nothing here uses this, but trust me, take this away & Client won't open.
from CommonClient import CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
import Patch #Learning how to use this is nightmarish.


class WWNESContext(CommonContext):
    game = "Wario's Woods"
    items_handling = 0b111 #Archipelago constant. Tells it what to do. You guys couldn't have used like 1 2 3 instead of b00lalala??

    @property #Override the Superclass, CommonContext.
    def suggested_address(self): #Returns the archipelago.gg port you last used, to default into Client's URL textbox.
        storage = Utils.persistent_load() #Todo: test if loading this once is fine, as opposed to loading it in every function I use it in.
        return storage.get("WariosWoods", {}).get("last_server", super().suggested_address) #I prefer not to use a variable for the storage pointer. The stored value though, I don't care about.

    def __init__(self, server_address: str, password: str):
        super().__init__(server_address, password) #Run the init of the Superclass.

        self.lua_reader = None #This listener will hear output from Lua, mailed directly to Client's doorstep.
        self.lua_writer = None #This listener will write Lua a loveletter and send it straight from here, the Client.
        self.lua_task = None #This listener fires off the lua_to_ap function, and keeps it rolling.
        self.heartbeat_task = None #This listener fires off the heartbeat function, to satisfy Lua, who constantly wants to know if Client is still alive. I just wanted to make sure you haven't died!

        self.location_reminder = 0 #Tell me once, and only once, what we've already sent to Server.
        self.atype_count = 3 #How many A-Type Rounds the player should be able to play. Yes, the number is wacky, I know. You think you can do better? HUH? jk i love you <3
        self.btype_count = 3 #How many B-Type Rounds the player should be able to play.
        self.data_package_ready = asyncio.Event() #A boolean that'll force an await from another function.
        
        self.check_still_connected = 1 #Used to tell the player when Client reconnects to Lua after Lua doesn't send heartbeats.

    async def send_lua_object(self, obj): #I do this a lot so it gets its own function now.
        if self.lua_writer is None: #If there's nothing to tell Lua, skip.
            return
        self.lua_writer.write(json.dumps(obj).encode() + b"\n") #Write Lua our letter.
        await self.lua_writer.drain() #Send it off. There it goes!

    def get_lua_script(self): #The script is inside the APWorld zip so we gotta pull it out lol.
        destination = os.path.join(tempfile.gettempdir(), "WWNES_connector_bizhawk.lua") #Here's where we're gonna put it once we pull it.
        lua_resource = (
            importlib.resources.files(__package__) #Here's the APWorld root.
            .joinpath("hooks") #Lua's in this folder.
            .joinpath("WWNES_connector_bizhawk.lua") #Oh hey there it is!
        )

        with lua_resource.open("rb") as source, open(destination, "wb") as target: #Just wanted to try a fancy way to plug in some variables. I forget if it works the normal way or not.
            shutil.copyfileobj(source, target) #Pull Lua out of the APWorld zip and move it to the destination.

        return destination #Tell the caller where we put it.

    def get_emuhawk_path(self): #Where's the emulator? I need to know so I can open the emulator. No emulator, no play-play video gamey.
        storage = Utils.persistent_load() #Maybe we've saved the location already?
        if "WariosWoods" in storage: #Double-check storage exists at all. If so...
            path = storage["WariosWoods"].get("emuhawk_path") #...Pull the last path to the emulator they provided. Surely people move/delete their old versions when upgrading to new versions, right? Hahaha...RIGHT?
            if path and os.path.exists(path): #If the path is stored, and the file it points to exists...
                return path #...Use that, then.

        #Well, if we made it here, then the path was invalid, or didn't exist.
        path = Utils.open_filename("Select EmuHawk.exe PLEASE PLEASE PLEASE SELECT IT NOWWWWW", filetypes=[("EmuHawk", "*.exe")]) #Select the emulator.
        
        if not path: 
            raise RuntimeError("EmuHawk executable not selected.") #SELECT. THE. EMULATOR.

        Utils.persistent_store("WariosWoods", "emuhawk_path", path) #Thank you. Store the emulator path so the player doesn't have to re-select it every time they wanna play.
        return path #...And use that.

    def get_patched_rom_path(self, opened_thru_patchfile: int): #Same exact thing as get_emuhawk_path, but for your vanilla dump of the vanilla game. Except I don't need to check if the storage exists here, cuz get_emuhawk_path gets called before this.
        
        if opened_thru_patchfile == 0: #But I do need to know if a patchfile wasn't used, because otherwise, Client will open everything and assume the last patched rom should be used again, despite the actual multiworld being played.
            Utils.persistent_store("WariosWoods", "patched_rom_path", None) #Clear it. I don't know if they're going to be connecting to the same multiworld as their savedata or not.
        
        storage = Utils.persistent_load() #Storage.
        path = storage.get("WariosWoods", {}).get("patched_rom_path") #Dump path.
        if path and os.path.exists(path): #Path is stored and file still there?
            return path #Use it.

        #Well, if we made it here, then the path was invalid, or didn't exist.                                              
        path = Utils.open_filename("Select Patched Wario's Woods (NES) ROM. Don't have one yet? Use Open Patch instead of Wario's Woods Client.", filetypes=[("NES Files", "*.nes"), ("All files", "*.*")]) #Select your dump.
        if not path:
            raise RuntimeError("ROM not selected.") #Fine, don't. Whatever.

        Utils.persistent_store("WariosWoods", "patched_rom_path", path) #Save the selected location so the player doesn't have to select it every time they wanna play the APWorld.
        return path #...And use that.

    def launch_bizhawk(self, opened_thru_patchfile: int): #Called by main once main has everything prepped. Opens BizHawk, and the Lua.
        logger.info("Please select EmuHawk.exe") #Debugger logging.
        emuhawk_path = self.get_emuhawk_path() #Get the emulator path.

        logger.info("Please select your Wario's Woods (NES) ROM.")
        rom_path = self.get_patched_rom_path(opened_thru_patchfile) #Get your patched dump's path.
        lua_script = self.get_lua_script() #Get Lua's path.

        logger.info(f"Launching {rom_path}")
        subprocess.Popen([emuhawk_path, rom_path, "--lua", lua_script]) #Use all the paths, together with the --lua argument, to open everything the player needs at once.

    def lua_location_name_to_id(self): #I do this enough to warrant a function.
        return {name: location_id for location_id, name in self.location_names[self.game].items()} #Invert the superclass's location_id_to_name into a location_name_to_id.

    async def connect_lua(self): #Connect Client to Lua.
        #logger.info("Waiting for BizHawk Lua server...")                                                         
        for _ in range(60): #Every second for the next 60 seconds...
            try:
                self.lua_reader, self.lua_writer = await asyncio.open_connection("127.0.0.1", 43055) #Probe the port that Lua emits from. Lua, my dear, are you there?
                logger.info("Connected to BizHawk.") #Debugger output.
                return #And break.
            except ConnectionRefusedError:
                await asyncio.sleep(1) #Wait a second.

        raise RuntimeError("Timed out waiting for BizHawk Lua server.") #We waited 60 seconds...no Lua. Heartbreaking...

    async def lua_handshake(self): #Rise and shine, script!
        self.lua_writer.write(b"VERSION\n") #Writing on a postcard: "What version are you?"
        await self.lua_writer.drain() #Mailing it out and waiting at the mailbox for a reply.

        response = await self.lua_reader.readline() #I GOT A LETTER OH MY GOSH OH MY GOSH
        if not response:
            raise RuntimeError("BizHawk closed connection during handshake.") #But it was only just a dream...

        version = response.decode().strip() #The letter just has a bunch of numbers in it what is this junk?? zzzzzzzzzzzz
        
        #print(f"WWNES Lua version: {version}") #Nobody needs that psh
 
    '''Not implemented Lua-side yet. Not really on my priority list. Fancy way of saying I tried and got tired of testing it too quickly. I'll implement this if somebody shoots me a working solution for both client and lua side.
    Otherwise, the player will just have to close everything and re-open the patchfile if their client disconnects from the lua.
    
        async def reconnect_lua(self):
        if self.lua_writer:
            try:
                self.lua_writer.close()
                await self.lua_writer.wait_closed()
            except Exception:
                pass

        self.lua_reader = None
        self.lua_writer = None

        logger.error("Waiting for BizHawk...")

        await self.connect_lua()
        await self.lua_handshake()

        logger.error("Lua reconnected.")
    '''    
    
    async def lua_to_ap(self): #How to Talk to the APServer: A Memoir.
        while True: #Keep talkin' buddy.
            try:                                                
                line = await asyncio.wait_for(self.lua_reader.readline(), timeout = 5) #Get a goodiebag from Lua every 5 seconds.                                                    
                if not line: #Absolutely flip out if we don't get a goodiebag.
                    
                    #Actually I think we never reach inside this cuz the reached timeout throws the TimeoutError, so it always defaults to the except & never disconnects from a stalling Lua server as long as it still exists.
                    
                    logger.error("BizHawk disconnected. Please re-launch Wario's Woods Client to reconnect.")
                    if self.lua_writer: #Close everything ahead of time. Show's over. Go home.
                        try:
                            self.lua_writer.close()
                            await self.lua_writer.wait_closed()
                        except Exception:
                            pass
                    self.lua_reader = None
                    self.lua_writer = None
                    await self.connect_lua()
                    #await self.reconnect_lua()
                    continue
                else:
                    if self.check_still_connected == 0:
                        self.check_still_connected = 1
                        logger.error("K I see it now. Good to keep goin'.")
                        continue
            except asyncio.TimeoutError: #I'm eat banan. Om Om Om Om Nom.
                self.check_still_connected = 0
                logger.error("Hey. Lua stalled. I don't see it anymore. Is the script still running?") 
                continue
                
            decoded = line.decode().strip() #Ooo what's in our goodiebag? 
            if decoded in ("", "1", "[]"): #Empty...?
                continue #...Sometimes it's nothing and that's okay.

            data = json.loads(decoded) #NOT EMPTY NOT EMPTY AAAUUAUHGHGGHGH so good
            location_name_to_id = self.lua_location_name_to_id() #Run that cool function I wrote.
            location_ids = [] #Instantiate a PHAT array.

            for item in data: #For every location Lua wants to send to the APServer...
                #Goal handling.
                if item.get("type") == "VICTORY": #Is it the winner?
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]) #Tell the APServer that we won!!
                    continue
                #Location handling.                                   
                if item.get("type") in location_name_to_id: #Which location is it, man?
                    location_ids.append(location_name_to_id[item["type"]]) #...Ah, it's this one. Convert it to an ID so the APServer will recognize it for what it truly is.
                    
            if location_ids: #If we got locations to send to the APServer...
                await self.check_locations(location_ids) #...Send'em. Use the superclass's function to do it.

    #You still good homie? k good.                                  
    async def heartbeat(self): #Client's heartbeat. Tells Lua we're okay.
        while True: #Needs a task to run over and over.
            await asyncio.sleep(3) #Every 3 seconds.
            if not self.lua_writer: #If we haven't made the listener yet, don't try the next part yet.
                continue
            try:
                self.lua_writer.write(json.dumps([{"type": "PING"}]).encode() + b"\n") #Lub dub. Lub dub. Lub dub.
                await self.lua_writer.drain() #Send it to Lua.
            except Exception:
                logger.error("Lua disconnected. Please re-launch Wario's Woods Client to reconnect.") #Couldn't send it to Lua. AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                #Actually I'm not sure it ever reaches here but it doesn't hurt to have extensive error handling.



    #ap_to_lua, broken up into async functions where necessary. Superclass's implementation of on_package is nothing. But we need it.
    def on_package(self, cmd: str, args: dict): #Here's the complex stuff. This is all game-specific logic, so it's the meat that'll change between implementations. I really should try to push it all to the Lua.
        if cmd == "Connected": #APServer sends the Connected command the first time Client connects to it.
            self.atype_count = 3 #Variable upkeep. In case we disconnect then reconnect without closing Client.
            self.btype_count = 3
            self.location_reminder = 0
            asyncio.create_task(self._connected()) #We need an async function that asks the APServer for all the locations we've sent and all the items we've received.
        elif cmd == "DataPackage": #We got a goodie package.
            self.data_package_ready.set() #Superclass's item_name_to_id is set now.
        elif cmd == "ReceivedItems": #APServer sent us an item. Let's open it up!
            #print("ReceivedItems: ", args)                  
            asyncio.create_task(self._received_items(args)) #Pop that sucka open. APServer put our new items into args, so pass those thru to the async function.

    async def _connected(self): #An async function that asks the APServer for all the locations we've sent and all the items we've received.
        await self.send_msgs([{"cmd": "GetDataPackage", "games": [self.game]}]) #Cool! We're connected. Now, gimmie the goodie package.

    async def _received_items(self, args: dict): #The APServer puts our new items into args.
        #Ey we got some items here!...
        if not self.lua_writer: #Don't do anything if disconnected from Lua.
            return
            
        await self.data_package_ready.wait() #Wait for super's item_name_to_id to get set.
        
        new_items = args.get("items", []) #Parse the args so we can play with our items.
        if not new_items:
            #...Or maybe we don't got items here??                                   
            return

        #Game logic below.
        
        atype_trigger = 0 #Instantiate triggers that tell us what items we received.
        btype_trigger = 0

        for item in new_items: #For every item the APServer sent...
            item_id = item[0] #Each is an array, so get the item ID out of the first index.
            item_name = self.item_names.lookup_in_game(item_id) #Use the Superclass's item_id_to_name to identify the item.
            if item_name == "Progressive A-Type Round":
                self.atype_count += 5 #If the item is an A-Type, give the player 5 more A-Type levels to play.
                atype_trigger = 1 #We got an A-Type!! SOUND THE ALARM WOOP WOOP WOOP WOOP
            elif item_name == "Progressive B-Type Round": #Yeah same thing here for B-Type.
                self.btype_count += 5
                btype_trigger = 1

        if atype_trigger == 1 and self.atype_count > 3: #If we sounded the alarm AND WE DIDN'T LITERALLY JUST START PLAYING THE GAME...
            await self.send_lua_object([ #...Tell Lua about our shiny new item, and how many rounds the player can play now.
                {"type": "WRITE", "item_name": "Progressive A-Type Round", "value": base64.b64encode(bytes([self.atype_count])).decode("utf-8")},
                {"type": "DISPLAY_MESSAGE", "message": "Received Progressive A-Type Round!"}
            ])

        if btype_trigger == 1 and self.btype_count > 3: #Same as above but for B-Type.
            await self.send_lua_object([
                {"type": "WRITE", "item_name": "Progressive B-Type Round", "value": base64.b64encode(bytes([self.btype_count])).decode("utf-8")},
                {"type": "DISPLAY_MESSAGE", "message": "Received Progressive B-Type Round!"}
            ])

        if self.location_reminder == 0: #Here's where we remind Lua which locations we've already sent, after Client finds out from the APServer.
            self.location_reminder = 1 #And don't remind Lua again. It'll remember.
            for location_id in self.checked_locations: #Superclass's checked_locations.
                location_name = self.location_names.lookup_in_game(location_id) + "_location" #Append _location to the location name so Lua can tell what we're trying to say.
                await self.send_lua_object([{"type": "WRITE", "item_name": location_name}]) #Send it off.

    async def shutdown(self): #What happens when Client is closed. Needs an override of the Superclass's shutdown due to the listeners. Boring stuff.
        for task in (self.lua_task, self.heartbeat_task):
            if task:
                task.cancel()
        if self.lua_writer:
            try:
                self.lua_writer.close()
                await self.lua_writer.wait_closed()
            except Exception:
                pass
        await super().shutdown() #Make sure Superclass also gets a final word in.

    async def connect(self, address): #Async function so everything doesn't stall while the Superclass is connecting Client to the APServer.
        Utils.persistent_store("WariosWoods", "last_server", address) #Save whatever the player put in as the port.
        await super().connect(address)

    def make_gui(self): #I wanted my own Client. Crazy, right?
        ui = super().make_gui() #Do it up like one of yours, but
        ui.base_title = "Archipelago Wario's Woods Client" #Put my name on it B)
        return ui #Ship it.
        
    async def server_auth(self, password_requested = False): #Superclass's server_auth doesn't ask for the slot name...
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username() #...Gotta do it ourselves.
        await self.send_connect()


def main(*launch_args): #Most important part. Whole Client runs from here.
    Utils.init_logging("Wario's Woods Archipelago Client") #Tells the Archipelago Launcher what name to give the text file in the Logs folder if Client crashes.

    parser = get_base_parser() #This helps patch the player's dump.
    parser.add_argument( #And it does so by adding an additional option, which the patchfile will supply, to Client's opening sequences.
        "diff_file", #Argument's name.
        default = "",
        type = str,
        nargs = "?", #Any amount of args. Optional.
        help = "I love you like a golden banana, my brother." #Would absolutely peel.
    )

    args = parser.parse_args(launch_args) #Yep, add it in. Just like that.

    async def _main(): #Main main in my main in an estimate.
        opened_thru_patchfile = 0 #Used to tell if the player opened Client via the patchfile/Open Patch (gets set to 1 in _main), or via the Wario's Woods Client (stays as 0).
        
        if args.diff_file: #If we got hit wid dat snazzy option we added...
            _, romfile = Patch.create_rom_file(args.diff_file) #...Patch the player's vanilla dump file using the patchfile.
            Utils.persistent_store("WariosWoods", "patched_rom_path", romfile) #And store the location of that so I don't have to pass the path through like 5 different function args just to get it to the BizHawk launcher function.
            opened_thru_patchfile = 1 #This only gets hit if the player opened Client via the patchfile. launch_bizhawk() gets affected.

        ctx = WWNESContext(args.connect, args.password) #Instantiate the class as an object.
        ctx.launch_bizhawk(opened_thru_patchfile) #Fire off the launch_bizhawk function. Pass through whether or not Client was opened via patchfile.

        await ctx.connect_lua() #Connect to Lua, and wait for success.
        await ctx.lua_handshake() #Wait for Lua to finish opening its eyes for the first time. Welcome to the world, darling.

        ctx.server_task = asyncio.create_task(server_loop(ctx), name = "ServerLoop") #Superclass's...thing. Alright you got me, I forget what this does and I don't feel like looking it up again. Sorry! 
        if gui_enabled: 
            ctx.run_gui() #This prevents the player from connecting to the APServer before Lua is ready to receive anything from it, basically by just not loading the interface yet.

        ctx.run_cli() #Another Superclass thing that's necessary but I don't remember precisely what it does.
        ctx.lua_task = asyncio.create_task(ctx.lua_to_ap(), name = "LuaToAP") #Kick off listener 1.
        ctx.heartbeat_task = asyncio.create_task(ctx.heartbeat(), name = "Heartbeat") #Kick off listener 2.

        await ctx.exit_event.wait() #Now we sit and watch. Until Client is prompted to close.
        await ctx.shutdown() #Client was prompted to close. Turn off the lights and close the door on your way out. See you next time! <33

    asyncio.run(_main()) #Run _main, now that we've finished defining it.


if __name__ == "__main__": #__init__.py adds the game's name to the archipelago launcher, so when the archipelago launcher is used to open a patchfile, it knows to open Client with it, and Client takes care of everything it's built to do.
    main() #Run main, now that we've finished defining it.
