

DEBUG = false



--I want a banana.

--CCtheOwl 9/10/2026




--Todo: 
--Rankings are good places to get required times. In case we wanna add the one thing. Yeah the one thing. Uhh what was it called? It was a uhhh...Yeah, time attack rounds! As locations! In case we want to add that.
--Reconnect Client to Lua if Client disconnected from Lua instead of making the player reopen the patchfile. Help with this is welcome. It's already totally fine if Lua disconnects from Client, cuz Client can just pick that right back up.
---Drag BizHawk around your screen. Client will notice it can't see it anymore, until you release BizHawk. Now drag Client around your screen. Game over, dude...


--Begin Wario's Woods logic module.



--[[
WRAM 0x0082 = coins?
1B6A WRAM = coins, updated at end of round
]]
--[[
coin positions:
0EFE WRAM	
0F08 WRAM	
0F12 WRAM	
0F1C WRAM	
0F26 WRAM	
]]
--[[
1B40 WRAM = how many levels beaten A-side, updated at end of round. Stops at 0x63 = 99
]] WRAM_ATYPE = 0x1B40
--[[
1B41 WRAM = how many levels beaten B-side, updated at end of round
]] WRAM_BTYPE = 0x1B41
--[[
0291 WRAM = current level, playmode-agnostic.
]] WRAM_CURRENTLEVEL = 0x0291
--[[
1B42 WRAM = which A-Type round you have selected, from 0 to 20. Well, you can set it higher. FF starts you off on round 203.
1B43 WRAM = same as above but for B-Type.
1B59 WRAM = which round type you hovered over last.
]]
--[[
0291 WRAM = Currently playing level in any mode.
]]
--[[
1B6B WRAM = continue count
]]
--[[
player name:
1B00 WRAM
1B01 WRAM	
1B02 WRAM	
1B03 WRAM	
128=A
153=Z
154=a
179=z
180=-
255=space
]]
--[[
ACTUALLY THERE'S NO EASY WAY TO TELL IF YOU FR CLEARED THE LESSON SO FRICK IT
learn moves:
0283 WRAM = the lesson level, set when lesson is entered. combine with the two below to determine which lesson got beat
0291 WRAM = 0 for first level in lesson set
1B60 WRAM = prolly don't need this one
starts at 0, first clear sets to 1, etc.
lessons will need to be progressive to be items
intercept a "start" input and replace with "space+start" if next lesson isn't unlocked yet. fire off a bizhawk msg.

2R time race timer:
1B10 = EASY
1B11
1B18 = MEDIUM
1B19 WRAM
1B20 WRAM = HARD
1B21 WRAM
Okay so the timers are big endian

3R:
1B12 = EASY
1B13
1B1A = MEDIUM
1B1B WRAM
1B22 WRAM = HARD
1B23 WRAM

4R:
1B14 = EASY
1B15
1B1C = MEDIUM
1B1D WRAM
1B24 WRAM = HARD
1B25 WRAM

5R:
1B16 = EASY
1B17
1B1E = MEDIUM
1B1F WRAM
1B26 WRAM = HARD
1B27 WRAM


]]
WRAM_START = 0x06000
--WRAM_END   = 0x023FFFFF  I DON'T KNOW.





--Items and Locations:
MONITORS = {
    {
        name = "Progressive A-Type Round",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "Progressive B-Type Round",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 4",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 9",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 14",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 19",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 24",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 29",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 34",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 39",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 44",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 49",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 54",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 59",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 64",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 69",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 74",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 79",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 84",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 89",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 94",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "A-Type Round 99",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_ATYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_ATYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 4",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 9",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 14",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 19",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 24",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 29",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 34",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 39",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 44",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 49",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 54",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 59",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 64",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 69",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 74",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 79",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 84",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 89",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 94",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "B-Type Round 99",
        read_mem = function()	
			local ok, v = pcall(memory.readbyte, WRAM_BTYPE, "WRAM")
			if ok then return v end
			return nil
		end,
        write_mem = function(value_to_write)	
			local ok, v = pcall(memory.writebyte, WRAM_BTYPE, value_to_write, "WRAM")
			if ok then return v end
			return nil
		end,
        send_location = 0,
        location_sent = 0
    },
	{
        name = "Out of the Woods",
		victory = true,
        read_mem = function()	
			return 0
		end,
        location_shield = 1,
        location_sent = 0
    },
}
client_atype = 3 --It's a weird number but I swear it's necessary. I only know this through trial & error though...
client_btype = 3 --Half of the logic for these two is in the client code. ehfjbwerufykbhefn
function get_round_type()
	local ok, v = pcall(memory.readbyte, 0x1B59, "WRAM")
	if v == 0 then
		return "A"
	else--if v == 1 then
		return "B"
	end
end






--Good stuff









function ProgATypeWatcher(mon)
	if mon.name == "Progressive A-Type Round" and get_round_type() == "A" then
		local ok, read_value = pcall(memory.readbyte, WRAM_CURRENTLEVEL, "WRAM")
		local round_clear = 0
		local jump_round_select = 0

		local ok, v = pcall(memory.readbyte, 0x014E, "CIRAM (nametables)") --Is the R for Round Clear there?
		local ok2, v2 = pcall(memory.readbyte, 0x0319, "CIRAM (nametables)") --Is the bottom right of the tree trunk open?
		if 
		v == 0xE9 and 	--0xE9 is the tile for R.
		v2 == 0x0F		--0x0F is the tile for black square.
		then
			round_clear = 1 --If we see an R and the trunk is open, assume the round was won.
		end
		
		
		local ok3, v3 = pcall(memory.readbyte, 0x04CA, "CIRAM (nametables)") --JU
		local ok4, v4 = pcall(memory.readbyte, 0x04CB, "CIRAM (nametables)") --UM
		local ok5, v5 = pcall(memory.readbyte, 0x04CC, "CIRAM (nametables)") --MP
		if
		v3 == 0xD8 and	--JU
		v4 == 0xD9 and	--UM
		v5 == 0xDA		--MP
		then
			jump_round_select = 1
		end
		
		
		
		--[[
		if DEBUG == true then
			print("A-Type")
			print("A: " .. string.format("%X", emu.getregister("A")))
			print("Flag B: " .. string.format("%X",emu.getregister("Flag B")))
			print("Flag C: " .. string.format("%X",emu.getregister("Flag C")))
			print("Flag D: " .. string.format("%X",emu.getregister("Flag D")))
			print("Flag I: " .. string.format("%X",emu.getregister("Flag I")))
			print("Flag N: " .. string.format("%X",emu.getregister("Flag N")))
			print("Flag T: " .. string.format("%X",emu.getregister("Flag T")))
			print("Flag V: " .. string.format("%X",emu.getregister("Flag V")))
			print("Flag Z: " .. string.format("%X",emu.getregister("Flag Z")))
			print("PC: " .. string.format("%X",emu.getregister("PC")))
			print("S: " .. string.format("%X",emu.getregister("S")))
			print("X: " .. string.format("%X",emu.getregister("X")))
			print("Y: " .. string.format("%X",emu.getregister("Y")))
		end
		]]
		--if emu.getregister("PC") == 0x98CA then
		--	;
		--else
		if round_clear == 1 then
			for _, mon2 in ipairs(MONITORS) do
				if read_value == 3 then
					if mon2.name == "A-Type Round 4" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 8 then
					if mon2.name == "A-Type Round 9" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 13 then
					if mon2.name == "A-Type Round 14" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 18 then
					if mon2.name == "A-Type Round 19" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 23 then
					if mon2.name == "A-Type Round 24" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 28 then
					if mon2.name == "A-Type Round 29" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 33 then
					if mon2.name == "A-Type Round 34" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 38 then
					if mon2.name == "A-Type Round 39" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 43 then
					if mon2.name == "A-Type Round 44" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 48 then
					if mon2.name == "A-Type Round 49" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 53 then
					if mon2.name == "A-Type Round 54" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 58 then
					if mon2.name == "A-Type Round 59" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 63 then
					if mon2.name == "A-Type Round 64" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 68 then
					if mon2.name == "A-Type Round 69" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 73 then
					if mon2.name == "A-Type Round 74" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 78 then
					if mon2.name == "A-Type Round 79" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 83 then
					if mon2.name == "A-Type Round 84" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 88 then
					if mon2.name == "A-Type Round 89" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 93 then
					if mon2.name == "A-Type Round 94" then
						mon2.send_location = 1
						break
					end
				elseif read_value == 98 then
					if mon2.name == "A-Type Round 99" then
						mon2.send_location = 1
						break
					end
				end
			end
		end


		--Paint sent locations white & purple.
		if jump_round_select == 1 then
				
			pcall(memory.writebyte, 0x27D2, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27D3, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27D4, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27D5, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DA, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DB, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DC, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DD, 0x55, "PPU Bus")

			local okok1, block1 = pcall(memory.readbyte, 0x27D2, "PPU Bus")
			local okok2, block2 = pcall(memory.readbyte, 0x27D3, "PPU Bus")
			local okok3, block3 = pcall(memory.readbyte, 0x27D4, "PPU Bus")
			local okok4, block4 = pcall(memory.readbyte, 0x27D5, "PPU Bus")
			
			local okok5, block5 = pcall(memory.readbyte, 0x27DA, "PPU Bus")
			local okok6, block6 = pcall(memory.readbyte, 0x27DB, "PPU Bus")
			local okok7, block7 = pcall(memory.readbyte, 0x27DC, "PPU Bus")
			local okok8, block8 = pcall(memory.readbyte, 0x27DD, "PPU Bus")
		
			for _, mon2 in ipairs(MONITORS) do
				if mon2.location_sent == 1 then
					if mon2.name == "A-Type Round 4" then
						block1 = block1 + 1
						pcall(memory.writebyte, 0x27D2, block1, "PPU Bus")
					end
					if mon2.name == "A-Type Round 9" then
						block1 = block1 + 4
						pcall(memory.writebyte, 0x27D2, block1, "PPU Bus")
					end
					if mon2.name == "A-Type Round 14" then
						block2 = block2 + 5
						pcall(memory.writebyte, 0x27D3, block2, "PPU Bus")
					end
					if mon2.name == "A-Type Round 19" then
						block3 = block3 + 1
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
					end
					if mon2.name == "A-Type Round 24" then
						block3 = block3 + 4
						block4 = block4 + 1
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
						pcall(memory.writebyte, 0x27D5, block4, "PPU Bus")
					end
					if mon2.name == "A-Type Round 29" then
						block4 = block4 + 4
						pcall(memory.writebyte, 0x27D5, block4, "PPU Bus")
					end
					if mon2.name == "A-Type Round 34" then
						block1 = block1 + 80
						pcall(memory.writebyte, 0x27D2, block1, "PPU Bus")
					end
					if mon2.name == "A-Type Round 39" then
						block2 = block2 + 16
						pcall(memory.writebyte, 0x27D3, block2, "PPU Bus")
					end
					if mon2.name == "A-Type Round 44" then
						block2 = block2 + 64
						block3 = block3 + 16
						pcall(memory.writebyte, 0x27D3, block2, "PPU Bus")
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
					end
					if mon2.name == "A-Type Round 49" then
						block3 = block3 + 64
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
					end
					if mon2.name == "A-Type Round 54" then
						block4 = block4 + 80
						pcall(memory.writebyte, 0x27D5, block4, "PPU Bus")
					end
					if mon2.name == "A-Type Round 59" then
						block5 = block5 + 5
						pcall(memory.writebyte, 0x27DA, block5, "PPU Bus")
					end
					if mon2.name == "A-Type Round 64" then
						block6 = block6 + 1
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
					end
					if mon2.name == "A-Type Round 69" then
						block6 = block6 + 4
						block7 = block7 + 1
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
					end
					if mon2.name == "A-Type Round 74" then
						block7 = block7 + 4
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
					end
					if mon2.name == "A-Type Round 79" then
						block8 = block8 + 5
						pcall(memory.writebyte, 0x27DD, block8, "PPU Bus")
					end
					if mon2.name == "A-Type Round 84" then
						block5 = block5 + 80
						pcall(memory.writebyte, 0x27DA, block5, "PPU Bus")
					end
					if mon2.name == "A-Type Round 89" then
						block6 = block6 + 16
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
					end
					if mon2.name == "A-Type Round 94" then
						block6 = block6 + 64
						block7 = block7 + 16
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
					end
					if mon2.name == "A-Type Round 99" then
						block7 = block7 + 64
						block8 = block8 + 80
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
						pcall(memory.writebyte, 0x27DD, block8, "PPU Bus")
					end
				end			
			end
		end
		
	end
end



function ProgBTypeWatcher(mon)
	if mon.name == "Progressive B-Type Round" and get_round_type() == "B" then
		local ok, read_value = pcall(memory.readbyte, WRAM_CURRENTLEVEL, "WRAM")
		local round_clear = 0
		local jump_round_select = 0

		local ok, v = pcall(memory.readbyte, 0x014E, "CIRAM (nametables)") --Is the R for Round Clear there?
		local ok2, v2 = pcall(memory.readbyte, 0x0319, "CIRAM (nametables)") --Is the bottom right of the tree trunk open?
		if 
		v == 0xE9 and 	--0xE9 is the tile for R.
		v2 == 0x0F		--0x0F is the tile for black square.
		then
			round_clear = 1 --If we see an R and the trunk is open, assume the round was won.
		end
		
		local ok3, v3 = pcall(memory.readbyte, 0x04CA, "CIRAM (nametables)") --JU
		local ok4, v4 = pcall(memory.readbyte, 0x04CB, "CIRAM (nametables)") --UM
		local ok5, v5 = pcall(memory.readbyte, 0x04CC, "CIRAM (nametables)") --MP
		if
		v3 == 0xD8 and	--JU
		v4 == 0xD9 and	--UM
		v5 == 0xDA		--MP
		then
			jump_round_select = 1
		end
		
		
		--[[
		if DEBUG == true then
			print("B-Type"	)
			print("A: " .. string.format("%X", emu.getregister("A")))
			print("Flag B: " .. string.format("%X",emu.getregister("Flag B")))
			print("Flag C: " .. string.format("%X",emu.getregister("Flag C")))
			print("Flag D: " .. string.format("%X",emu.getregister("Flag D")))
			print("Flag I: " .. string.format("%X",emu.getregister("Flag I")))
			print("Flag N: " .. string.format("%X",emu.getregister("Flag N")))
			print("Flag T: " .. string.format("%X",emu.getregister("Flag T")))
			print("Flag V: " .. string.format("%X",emu.getregister("Flag V")))
			print("Flag Z: " .. string.format("%X",emu.getregister("Flag Z")))
			print("PC: " .. string.format("%X",emu.getregister("PC")))
			print("S: " .. string.format("%X",emu.getregister("S")))
			print("X: " .. string.format("%X",emu.getregister("X")))
			print("Y: " .. string.format("%X",emu.getregister("Y")))
		end
		]]
		--if emu.getregister("PC") == 0x98CA then
		--	;
		--else
		if round_clear == 1 then
			for _, mon2 in ipairs(MONITORS) do
				if mon2.location_sent == 0 then
					if read_value == 3 then
						if mon2.name == "B-Type Round 4" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 8 then
						if mon2.name == "B-Type Round 9" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 13 then
						if mon2.name == "B-Type Round 14" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 18 then
						if mon2.name == "B-Type Round 19" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 23 then
						if mon2.name == "B-Type Round 24" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 28 then
						if mon2.name == "B-Type Round 29" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 33 then
						if mon2.name == "B-Type Round 34" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 38 then
						if mon2.name == "B-Type Round 39" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 43 then
						if mon2.name == "B-Type Round 44" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 48 then
						if mon2.name == "B-Type Round 49" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 53 then
						if mon2.name == "B-Type Round 54" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 58 then
						if mon2.name == "B-Type Round 59" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 63 then
						if mon2.name == "B-Type Round 64" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 68 then
						if mon2.name == "B-Type Round 69" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 73 then
						if mon2.name == "B-Type Round 74" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 78 then
						if mon2.name == "B-Type Round 79" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 83 then
						if mon2.name == "B-Type Round 84" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 88 then
						if mon2.name == "B-Type Round 89" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 93 then
						if mon2.name == "B-Type Round 94" then
							mon2.send_location = 1
							break
						end
					elseif read_value == 98 then
						if mon2.name == "B-Type Round 99" then
							mon2.send_location = 1
							break
						end
					end
				end
			end
		end
		
		
		
		--Paint sent locations white & purple.
		if jump_round_select == 1 then
			
			pcall(memory.writebyte, 0x27D2, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27D3, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27D4, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27D5, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DA, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DB, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DC, 0x55, "PPU Bus")
			pcall(memory.writebyte, 0x27DD, 0x55, "PPU Bus")
		
			local okok1, block1 = pcall(memory.readbyte, 0x27D2, "PPU Bus")
			local okok2, block2 = pcall(memory.readbyte, 0x27D3, "PPU Bus")
			local okok3, block3 = pcall(memory.readbyte, 0x27D4, "PPU Bus")
			local okok4, block4 = pcall(memory.readbyte, 0x27D5, "PPU Bus")
			
			local okok5, block5 = pcall(memory.readbyte, 0x27DA, "PPU Bus")
			local okok6, block6 = pcall(memory.readbyte, 0x27DB, "PPU Bus")
			local okok7, block7 = pcall(memory.readbyte, 0x27DC, "PPU Bus")
			local okok8, block8 = pcall(memory.readbyte, 0x27DD, "PPU Bus")
			
			for _, mon2 in ipairs(MONITORS) do
				if mon2.location_sent == 1 then
					if mon2.name == "B-Type Round 4" then
						block1 = block1 + 1
						pcall(memory.writebyte, 0x27D2, block1, "PPU Bus")
					end
					if mon2.name == "B-Type Round 9" then
						block1 = block1 + 4
						pcall(memory.writebyte, 0x27D2, block1, "PPU Bus")
					end
					if mon2.name == "B-Type Round 14" then
						block2 = block2 + 5
						pcall(memory.writebyte, 0x27D3, block2, "PPU Bus")
					end
					if mon2.name == "B-Type Round 19" then
						block3 = block3 + 1
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
					end
					if mon2.name == "B-Type Round 24" then
						block3 = block3 + 4
						block4 = block4 + 1
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
						pcall(memory.writebyte, 0x27D5, block4, "PPU Bus")
					end
					if mon2.name == "B-Type Round 29" then
						block4 = block4 + 4
						pcall(memory.writebyte, 0x27D5, block4, "PPU Bus")
					end
					if mon2.name == "B-Type Round 34" then
						block1 = block1 + 80
						pcall(memory.writebyte, 0x27D2, block1, "PPU Bus")
					end
					if mon2.name == "B-Type Round 39" then
						block2 = block2 + 16
						pcall(memory.writebyte, 0x27D3, block2, "PPU Bus")
					end
					if mon2.name == "B-Type Round 44" then
						block2 = block2 + 64
						block3 = block3 + 16
						pcall(memory.writebyte, 0x27D3, block2, "PPU Bus")
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
					end
					if mon2.name == "B-Type Round 49" then
						block3 = block3 + 64
						pcall(memory.writebyte, 0x27D4, block3, "PPU Bus")
					end
					if mon2.name == "B-Type Round 54" then
						block4 = block4 + 80
						pcall(memory.writebyte, 0x27D5, block4, "PPU Bus")
					end
					if mon2.name == "B-Type Round 59" then
						block5 = block5 + 5
						pcall(memory.writebyte, 0x27DA, block5, "PPU Bus")
					end
					if mon2.name == "B-Type Round 64" then
						block6 = block6 + 1
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
					end
					if mon2.name == "B-Type Round 69" then
						block6 = block6 + 4
						block7 = block7 + 1
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
					end
					if mon2.name == "B-Type Round 74" then
						block7 = block7 + 4
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
					end
					if mon2.name == "B-Type Round 79" then
						block8 = block8 + 5
						pcall(memory.writebyte, 0x27DD, block8, "PPU Bus")
					end
					if mon2.name == "B-Type Round 84" then
						block5 = block5 + 80
						pcall(memory.writebyte, 0x27DA, block5, "PPU Bus")
					end
					if mon2.name == "B-Type Round 89" then
						block6 = block6 + 16
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
					end
					if mon2.name == "B-Type Round 94" then
						block6 = block6 + 64
						block7 = block7 + 16
						pcall(memory.writebyte, 0x27DB, block6, "PPU Bus")
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
					end
					if mon2.name == "B-Type Round 99" then
						block7 = block7 + 64
						block8 = block8 + 80
						pcall(memory.writebyte, 0x27DC, block7, "PPU Bus")
						pcall(memory.writebyte, 0x27DD, block8, "PPU Bus")
					end
				end			
			end
		end
		
	end
end


function init()
	print("ya")
	--Set the selected level in A-Type and B-Type Round select menu to be 0, so the player can't choose a level they haven't received.
	pcall(memory.writebyte, 0x1B42, 0, "WRAM")
	pcall(memory.writebyte, 0x1B43, 0, "WRAM")
end




--This gets run every frame we're connected to Client.
function update()
	local checks_found = {}
    for _, mon in ipairs(MONITORS) do
        local current_value = mon.read_mem()
		ProgATypeWatcher(mon)
		ProgBTypeWatcher(mon)
		if mon.name == "Progressive A-Type Round" and current_value ~= client_atype then
			pcall(memory.writebyte, WRAM_ATYPE, client_atype, "WRAM") --Set rounds every frame cuz lazy.
		elseif mon.name == "Progressive B-Type Round" and current_value ~= client_btype then
			pcall(memory.writebyte, WRAM_BTYPE, client_btype, "WRAM")
		end
        if mon.send_location == 1 then --Sending location checks.
			table.insert(checks_found, mon.name) --...append the name of the monitored address to the list of checks to send to Client.
            mon.location_sent = 1 --Track what we're at now with this monitored address.
        end
		
		local ok, current_level = pcall(memory.readbyte, WRAM_CURRENTLEVEL, "WRAM") --Get current level.
		if mon.name == "Progressive A-Type Round" and current_level > client_atype and get_round_type() == "A" --Stop player from playing rounds they don't have...
		and current_level < 98	--...Unless they're at the end. I'd never take your victory cutscene from you! <3
		then 
			joypad.set({["P1 Select"] = true, ["P1 Start"] = true}) --Select+Start to return to the main menu.
			pcall(memory.writebyte, WRAM_CURRENTLEVEL, 0, "WRAM")
		elseif mon.name == "Progressive B-Type Round" and current_level > client_btype and get_round_type() == "B"
		and current_level < 98
		then
			joypad.set({["P1 Select"] = true, ["P1 Start"] = true})
			pcall(memory.writebyte, WRAM_CURRENTLEVEL, 0, "WRAM")		
		end
		
		if mon.name == "Out of the Woods" then --Goal detection.
			local goal_typea = 0
			local goal_typeb = 0
			for _, mon2 in ipairs(MONITORS) do
				if mon2.name == "A-Type Round 99" and mon2.location_sent == 1 then
					goal_typea = 1
				elseif mon2.name == "B-Type Round 99" and mon2.location_sent == 1 then
					goal_typeb = 1
				end
				
				if goal_typea == 1 and goal_typeb == 1 then
					mon.send_location = 1
				end
				
			end
		end
		
    end
    return checks_found --Send the list of acquired checks this frame back to main().
end












































--Begin base64.lua


-- This file originates from this repository: https://github.com/iskolbin/lbase64
-- It was modified to translate between base64 strings and lists of bytes instead of base64 strings and strings.

package.preload["base64"] = function()
	local base64 = {}
	local extract = _G.bit32 and _G.bit32.extract -- Lua 5.2/Lua 5.3 in compatibility mode
	if not extract then
		if _G._VERSION == "Lua 5.4" then
			extract = load[[return function( v, from, width )
				return ( v >> from ) & ((1 << width) - 1)
			end]]()
		elseif _G.bit then -- LuaJIT
			local shl, shr, band = _G.bit.lshift, _G.bit.rshift, _G.bit.band
			extract = function( v, from, width )
				return band( shr( v, from ), shl( 1, width ) - 1 )
			end
		elseif _G._VERSION == "Lua 5.1" then
			extract = function( v, from, width )
				local w = 0
				local flag = 2^from
				for i = 0, width-1 do
					local flag2 = flag + flag
					if v % flag2 >= flag then
						w = w + 2^i
					end
					flag = flag2
				end
				return w
			end
		end
	end


	function base64.makeencoder( s62, s63, spad )
		local encoder = {}
		for b64code, char in pairs{[0]='A','B','C','D','E','F','G','H','I','J',
			'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y',
			'Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n',
			'o','p','q','r','s','t','u','v','w','x','y','z','0','1','2',
			'3','4','5','6','7','8','9',s62 or '+',s63 or'/',spad or'='} do
			encoder[b64code] = char:byte()
		end
		return encoder
	end

	function base64.makedecoder( s62, s63, spad )
		local decoder = {}
		for b64code, charcode in pairs( base64.makeencoder( s62, s63, spad )) do
			decoder[charcode] = b64code
		end
		return decoder
	end

	local DEFAULT_ENCODER = base64.makeencoder()
	local DEFAULT_DECODER = base64.makedecoder()

	local char, concat = string.char, table.concat

	function base64.encode( arr, encoder )
		encoder = encoder or DEFAULT_ENCODER
		local t, k, n = {}, 1, #arr
		local lastn = n % 3
		for i = 1, n-lastn, 3 do
			local a, b, c = arr[i], arr[i + 1], arr[i + 2]
			local v = a*0x10000 + b*0x100 + c
			local s
			s = char(encoder[extract(v,18,6)], encoder[extract(v,12,6)], encoder[extract(v,6,6)], encoder[extract(v,0,6)])
			t[k] = s
			k = k + 1
		end
		if lastn == 2 then
			local a, b = arr[n-1], arr[n]
			local v = a*0x10000 + b*0x100
			t[k] = char(encoder[extract(v,18,6)], encoder[extract(v,12,6)], encoder[extract(v,6,6)], encoder[64])
		elseif lastn == 1 then
			local v = arr[n]*0x10000
			t[k] = char(encoder[extract(v,18,6)], encoder[extract(v,12,6)], encoder[64], encoder[64])
		end
		return concat( t )
	end

	function base64.decode( b64, decoder )
		decoder = decoder or DEFAULT_DECODER
		local pattern = '[^%w%+%/%=]'
		if decoder then
			local s62, s63
			for charcode, b64code in pairs( decoder ) do
				if b64code == 62 then s62 = charcode
				elseif b64code == 63 then s63 = charcode
				end
			end
			pattern = ('[^%%w%%%s%%%s%%=]'):format( char(s62), char(s63) )
		end
		b64 = b64:gsub( pattern, '' )
		local t, k = {}, 1
		local n = #b64
		local padding = b64:sub(-2) == '==' and 2 or b64:sub(-1) == '=' and 1 or 0
		for i = 1, padding > 0 and n-4 or n, 4 do
			local a, b, c, d = b64:byte( i, i+3 )
			local s
			local v = decoder[a]*0x40000 + decoder[b]*0x1000 + decoder[c]*0x40 + decoder[d]
			table.insert(t,extract(v,16,8))
			table.insert(t,extract(v,8,8))
			table.insert(t,extract(v,0,8))
		end
		if padding == 1 then
			local a, b, c = b64:byte( n-3, n-1 )
			local v = decoder[a]*0x40000 + decoder[b]*0x1000 + decoder[c]*0x40
			table.insert(t,extract(v,16,8))
			table.insert(t,extract(v,8,8))
		elseif padding == 2 then
			local a, b = b64:byte( n-3, n-2 )
			local v = decoder[a]*0x40000 + decoder[b]*0x1000
			table.insert(t,extract(v,16,8))
		end
		return t
	end

	return base64
end


--Begin lua_5_3_compat.lua


package.preload["lua_5_3_compat"] = function()
	function bit.rshift(a, b)
	  return a >> b
	end
	function bit.lshift(a, b)
	  return a << b
	end
	function bit.bor(a, b)
	  return a | b
	end
	function bit.band(a, b)
	  return a & b
	end
end


--Begin socket.lua


-----------------------------------------------------------------------------
-- LuaSocket helper module
-- Author: Diego Nehab
-- RCS ID: $Id: socket.lua,v 1.22 2005/11/22 08:33:29 diego Exp $
-----------------------------------------------------------------------------
package.preload["socket"] = function()
	local original_global_env = _ENV
	-----------------------------------------------------------------------------
	-- Declare module and import dependencies
	-----------------------------------------------------------------------------
	local base = _G
	local string = require("string")
	local math = require("math")

	function get_lua_version()
		local major, minor = _VERSION:match("Lua (%d+)%.(%d+)")
		assert(tonumber(major) == 5)
		if tonumber(minor) >= 4 then
			return "5-4"
		end
		return "5-1"
	end

	function get_os()
		local the_os, ext, arch
		if package.config:sub(1,1) == "\\" then
			the_os, ext = "windows", "dll"
			arch = os.getenv"PROCESSOR_ARCHITECTURE"
		else
			-- TODO: macos?
			the_os, ext = "linux", "so"
			arch = "x86_64" -- TODO: read ELF header from /proc/$PID/exe to get arch
		end

		if arch:find("64") ~= nil then
			arch = "x64"
		else
			arch = "x86"
		end

		return the_os, ext, arch
	end

	function get_socket_path()
		local the_os, ext, arch = get_os()
		-- for some reason ./ isn't working, so use a horrible hack to get the pwd
		local pwd = "C:/ProgramData/Archipelago/data/lua"
		return pwd .. "/" .. arch .. "/socket-" .. the_os .. "-" .. get_lua_version() .. "." .. ext
	end
	local lua_version = get_lua_version()
	local socket_path = get_socket_path()
	local socket = assert(package.loadlib(socket_path, "luaopen_socket_core"))()
	local event = event
	-- http://lua-users.org/wiki/ModulesTutorial
	local M = {}
	if setfenv then
		setfenv(1, M) -- for 5.1
	else
		_ENV = M -- for 5.2
	end

	M.socket = socket
	-- Bizhawk <= 2.8 has an issue where resetting the lua doesn't close the socket
	-- ...to get around this, we register an exit handler to close the socket first
	if lua_version == '5-1' then
		local old_udp = socket.udp
		function udp(self)
			s = old_udp(self)
			function close_socket(self)
				s:close()
			end
			event.onexit(close_socket)
			return s
		end
		socket.udp = udp
	end

	-----------------------------------------------------------------------------
	-- Exported auxiliar functions
	-----------------------------------------------------------------------------
	function connect(address, port, laddress, lport)
		local sock, err = socket.tcp()
		if not sock then return nil, err end
		if laddress then
			local res, err = sock:bind(laddress, lport, -1)
			if not res then return nil, err end
		end
		local res, err = sock:connect(address, port)
		if not res then return nil, err end
		return sock
	end

	function bind(host, port, backlog)
		local sock, err = socket.tcp()
		if not sock then return nil, err end
		sock:setoption("reuseaddr", true)
		local res, err = sock:bind(host, port)
		if not res then return nil, err end
		res, err = sock:listen(backlog)
		if not res then return nil, err end
		return sock
	end

	try = socket.newtry()

	function choose(table)
		return function(name, opt1, opt2)
			if base.type(name) ~= "string" then
				name, opt1, opt2 = "default", name, opt1
			end
			local f = table[name or "nil"]
			if not f then base.error("unknown key (".. base.tostring(name) ..")", 3)
			else return f(opt1, opt2) end
		end
	end

	-----------------------------------------------------------------------------
	-- Socket sources and sinks, conforming to LTN12
	-----------------------------------------------------------------------------
	-- create namespaces inside LuaSocket namespace


	sourcet = {}
	sinkt = {}

	BLOCKSIZE = 2048

	sinkt["close-when-done"] = function(sock)
		return base.setmetatable({
			getfd = function() return sock:getfd() end,
			dirty = function() return sock:dirty() end
		}, {
			__call = function(self, chunk, err)
				if not chunk then
					sock:close()
					return 1
				else return sock:send(chunk) end
			end
		})
	end

	sinkt["keep-open"] = function(sock)
		return base.setmetatable({
			getfd = function() return sock:getfd() end,
			dirty = function() return sock:dirty() end
		}, {
			__call = function(self, chunk, err)
				if chunk then return sock:send(chunk)
				else return 1 end
			end
		})
	end

	sinkt["default"] = sinkt["keep-open"]

	sink = choose(sinkt)

	sourcet["by-length"] = function(sock, length)
		return base.setmetatable({
			getfd = function() return sock:getfd() end,
			dirty = function() return sock:dirty() end
		}, {
			__call = function()
				if length <= 0 then return nil end
				local size = math.min(socket.BLOCKSIZE, length)
				local chunk, err = sock:receive(size)
				if err then return nil, err end
				length = length - string.len(chunk)
				return chunk
			end
		})
	end

	sourcet["until-closed"] = function(sock)
		local done
		return base.setmetatable({
			getfd = function() return sock:getfd() end,
			dirty = function() return sock:dirty() end
		}, {
			__call = function()
				if done then return nil end
				local chunk, err, partial = sock:receive(socket.BLOCKSIZE)
				if not err then return chunk
				elseif err == "closed" then
					sock:close()
					done = 1
					return partial
				else return nil, err end
			end
		})
	end


	sourcet["default"] = sourcet["until-closed"]

	source = choose(sourcet)
	
	local final_module = M
	
	_ENV = original_global_env

	return final_module
end


--Begin json.lua


--
-- json.lua
--
-- Copyright (c) 2015 rxi
--
-- This library is free software; you can redistribute it and/or modify it
-- under the terms of the MIT license. See LICENSE for details.
--

package.preload["json"] = function()
	-------------------------------------------------------------------------------
	-- Encode
	-------------------------------------------------------------------------------
	local json = { _version = "0.1.0" }
	local encode

	local escape_char_map = {
	  [ "\\" ] = "\\\\",
	  [ "\"" ] = "\\\"",
	  [ "\b" ] = "\\b",
	  [ "\f" ] = "\\f",
	  [ "\n" ] = "\\n",
	  [ "\r" ] = "\\r",
	  [ "\t" ] = "\\t",
	}

	local escape_char_map_inv = { [ "\\/" ] = "/" }
	for k, v in pairs(escape_char_map) do
	  escape_char_map_inv[v] = k
	end


	local function escape_char(c)
	  return escape_char_map[c] or string.format("\\u%04x", c:byte())
	end


	local function encode_nil(val)
	  return "null"
	end 


	local function encode_table(val, stack)
	  local res = {}
	  stack = stack or {}

	  -- Circular reference?
	  if stack[val] then error("circular reference") end

	  stack[val] = true

	  if val[1] ~= nil or next(val) == nil then
		-- Treat as array -- check keys are valid and it is not sparse
		local n = 0
		for k in pairs(val) do
		  if type(k) ~= "number" then
			error("invalid table: mixed or invalid key types")
		  end
		  n = n + 1
		end
		if n ~= #val then
		  error("invalid table: sparse array")
		end
		-- Encode
		for i, v in ipairs(val) do
		  table.insert(res, encode(v, stack))
		end
		stack[val] = nil
		return "[" .. table.concat(res, ",") .. "]"

	  else
		-- Treat as an object
		for k, v in pairs(val) do
		  if type(k) ~= "string" then
			error("invalid table: mixed or invalid key types")
		  end
		  table.insert(res, encode(k, stack) .. ":" .. encode(v, stack))
		end
		stack[val] = nil
		return "{" .. table.concat(res, ",") .. "}"
	  end
	end


	local function encode_string(val)
	  return '"' .. val:gsub('[%z\1-\31\\"]', escape_char) .. '"'
	end


	local function encode_number(val)
	  -- Check for NaN, -inf and inf
	  if val ~= val or val <= -math.huge or val >= math.huge then
		error("unexpected number value '" .. tostring(val) .. "'")
	  end
	  return string.format("%.14g", val)
	end


	local type_func_map = {
	  [ "nil"     ] = encode_nil,
	  [ "table"   ] = encode_table,
	  [ "string"  ] = encode_string,
	  [ "number"  ] = encode_number,
	  [ "boolean" ] = tostring,
	}


	encode = function(val, stack)
	  local t = type(val)
	  local f = type_func_map[t]
	  if f then
		return f(val, stack)
	  end
	  error("unexpected type '" .. t .. "'")
	end


	function json.encode(val)
	  return ( encode(val) )
	end


	-------------------------------------------------------------------------------
	-- Decode
	-------------------------------------------------------------------------------

	local parse

	local function create_set(...) 
	  local res = {}
	  for i = 1, select("#", ...) do
		res[ select(i, ...) ] = true
	  end
	  return res
	end

	local space_chars   = create_set(" ", "\t", "\r", "\n")
	local delim_chars   = create_set(" ", "\t", "\r", "\n", "]", "}", ",")
	local escape_chars  = create_set("\\", "/", '"', "b", "f", "n", "r", "t", "u")
	local literals      = create_set("true", "false", "null")

	local literal_map = {
	  [ "true"  ] = true,
	  [ "false" ] = false,
	  [ "null"  ] = nil,
	}


	local function next_char(str, idx, set, negate)
	  for i = idx, #str do
		if set[str:sub(i, i)] ~= negate then
		  return i
		end
	  end
	  return #str + 1
	end


	local function decode_error(str, idx, msg)
	  --local line_count = 1
	  --local col_count = 1
	  --for i = 1, idx - 1 do
	  --  col_count = col_count + 1
	  --  if str:sub(i, i) == "\n" then
	  --   line_count = line_count + 1
	  --    col_count = 1
	  --  end
	  -- end
	  -- emu.message( string.format("%s at line %d col %d", msg, line_count, col_count) )
	end


	local function codepoint_to_utf8(n)
	  -- http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=iws-appendixa
	  local f = math.floor
	  if n <= 0x7f then
		return string.char(n)
	  elseif n <= 0x7ff then
		return string.char(f(n / 64) + 192, n % 64 + 128)
	  elseif n <= 0xffff then
		return string.char(f(n / 4096) + 224, f(n % 4096 / 64) + 128, n % 64 + 128)
	  elseif n <= 0x10ffff then
		return string.char(f(n / 262144) + 240, f(n % 262144 / 4096) + 128,
						   f(n % 4096 / 64) + 128, n % 64 + 128)
	  end
	  error( string.format("invalid unicode codepoint '%x'", n) )
	end


	local function parse_unicode_escape(s)
	  local n1 = tonumber( s:sub(3, 6),  16 )
	  local n2 = tonumber( s:sub(9, 12), 16 )
	  -- Surrogate pair?
	  if n2 then
		return codepoint_to_utf8((n1 - 0xd800) * 0x400 + (n2 - 0xdc00) + 0x10000)
	  else
		return codepoint_to_utf8(n1)
	  end
	end


	local function parse_string(str, i)
	  local has_unicode_escape = false
	  local has_surrogate_escape = false
	  local has_escape = false
	  local last
	  for j = i + 1, #str do
		local x = str:byte(j)

		if x < 32 then
		  decode_error(str, j, "control character in string")
		end

		if last == 92 then -- "\\" (escape char)
		  if x == 117 then -- "u" (unicode escape sequence)
			local hex = str:sub(j + 1, j + 5)
			if not hex:find("%x%x%x%x") then
			  decode_error(str, j, "invalid unicode escape in string")
			end
			if hex:find("^[dD][89aAbB]") then
			  has_surrogate_escape = true
			else
			  has_unicode_escape = true
			end
		  else
			local c = string.char(x)
			if not escape_chars[c] then
			  decode_error(str, j, "invalid escape char '" .. c .. "' in string")
			end
			has_escape = true
		  end
		  last = nil

		elseif x == 34 then -- '"' (end of string)
		  local s = str:sub(i + 1, j - 1)
		  if has_surrogate_escape then 
			s = s:gsub("\\u[dD][89aAbB]..\\u....", parse_unicode_escape)
		  end
		  if has_unicode_escape then 
			s = s:gsub("\\u....", parse_unicode_escape)
		  end
		  if has_escape then
			s = s:gsub("\\.", escape_char_map_inv)
		  end
		  return s, j + 1
		
		else
		  last = x
		end
	  end
	  decode_error(str, i, "expected closing quote for string")
	end


	local function parse_number(str, i)
	  local x = next_char(str, i, delim_chars)
	  local s = str:sub(i, x - 1)
	  local n = tonumber(s)
	  if not n then
		decode_error(str, i, "invalid number '" .. s .. "'")
	  end
	  return n, x
	end


	local function parse_literal(str, i)
	  local x = next_char(str, i, delim_chars)
	  local word = str:sub(i, x - 1)
	  if not literals[word] then
		decode_error(str, i, "invalid literal '" .. word .. "'")
	  end
	  return literal_map[word], x
	end


	local function parse_array(str, i)
	  local res = {}
	  local n = 1
	  i = i + 1
	  while 1 do
		local x
		i = next_char(str, i, space_chars, true)
		-- Empty / end of array?
		if str:sub(i, i) == "]" then 
		  i = i + 1
		  break
		end
		-- Read token
		x, i = parse(str, i)
		res[n] = x
		n = n + 1
		-- Next token 
		i = next_char(str, i, space_chars, true)
		local chr = str:sub(i, i)
		i = i + 1
		if chr == "]" then break end
		if chr ~= "," then decode_error(str, i, "expected ']' or ','") end
	  end
	  return res, i
	end


	local function parse_object(str, i)
	  local res = {}
	  i = i + 1
	  while 1 do
		local key, val
		i = next_char(str, i, space_chars, true)
		-- Empty / end of object?
		if str:sub(i, i) == "}" then 
		  i = i + 1
		  break
		end
		-- Read key
		if str:sub(i, i) ~= '"' then
		  decode_error(str, i, "expected string for key")
		end
		key, i = parse(str, i)
		-- Read ':' delimiter
		i = next_char(str, i, space_chars, true)
		if str:sub(i, i) ~= ":" then
		  decode_error(str, i, "expected ':' after key")
		end
		i = next_char(str, i + 1, space_chars, true)
		-- Read value
		val, i = parse(str, i)
		-- Set
		res[key] = val
		-- Next token
		i = next_char(str, i, space_chars, true)
		local chr = str:sub(i, i)
		i = i + 1
		if chr == "}" then break end
		if chr ~= "," then decode_error(str, i, "expected '}' or ','") end
	  end
	  return res, i
	end


	local char_func_map = {
	  [ '"' ] = parse_string,
	  [ "0" ] = parse_number,
	  [ "1" ] = parse_number,
	  [ "2" ] = parse_number,
	  [ "3" ] = parse_number,
	  [ "4" ] = parse_number,
	  [ "5" ] = parse_number,
	  [ "6" ] = parse_number,
	  [ "7" ] = parse_number,
	  [ "8" ] = parse_number,
	  [ "9" ] = parse_number,
	  [ "-" ] = parse_number,
	  [ "t" ] = parse_literal,
	  [ "f" ] = parse_literal,
	  [ "n" ] = parse_literal,
	  [ "[" ] = parse_array,
	  [ "{" ] = parse_object,
	}


	parse = function(str, idx)
	  local chr = str:sub(idx, idx)
	  local f = char_func_map[chr]
	  if f then
		return f(str, idx)
	  end
	  decode_error(str, idx, "unexpected character '" .. chr .. "'")
	end


	function json.decode(str)
	  if type(str) ~= "string" then
		error("expected argument of type string, got " .. type(str))
	  end
	  return ( parse(str, next_char(str, 1, space_chars, true)) )
	end


	return json
end


--Begin connector_bizhawk_generic.lua
--But I had to change a bunch of stuff so don't expect it to match as closely as the others.


--[[
Copyright (c) 2023 Zunawe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
]]



--I forget what SCRIPT_VERSION does.
local SCRIPT_VERSION = 1


--BizHawk version check
local bizhawk_version = client.getversion()
local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
bizhawk_major = tonumber(bizhawk_major)
bizhawk_minor = tonumber(bizhawk_minor)
if bizhawk_patch == "" then bizhawk_patch = 0 else bizhawk_patch = tonumber(bizhawk_patch) end

--Lua version check
local lua_major, lua_minor = _VERSION:match("Lua (%d+)%.(%d+)")
lua_major = tonumber(lua_major)
lua_minor = tonumber(lua_minor)

--Requires; these pull from the in-lined scripts above.
if lua_major > 5 or (lua_major == 5 and lua_minor >= 3) then
    require("lua_5_3_compat")
end
local base64 = require("base64")
local socket = require("socket")
local json = require("json")

--Client (client) connectivity variables
local SOCKET_PORT_FIRST = 43055 --Lua's port.
local SOCKET_PORT_RANGE_SIZE = 0 --Lua's port can go up by this many if Lua's port is already taken. I've left this at 0 because I don't want to test it. I'll change it if anybody complains.
local SOCKET_PORT_LAST = SOCKET_PORT_FIRST + SOCKET_PORT_RANGE_SIZE --The tallest glass of beer that Lua can drink before Client won't talk to it.
local STATE_NOT_CONNECTED = 0 --An attempt at self-documenting code, I guess. I'm not a fan of not just writing things down, personally.
local STATE_CONNECTED = 1
local server = nil
local client_socket = nil
local current_state = STATE_NOT_CONNECTED
local timeout_timer = 0 --How long to wait between Client heartbeats before Lua stops caring.
local message_timer = 0 --How long between emulator display popups.
local message_interval = 0 --Same as above but for when they get received at the same time?
local prev_time = 0 --I don't know
local current_time = 0
local locked = false --Should Lua be waiting for Client? y/n
local rom_hash = nil --What game we're playing (Diddy Kong Racing DS hopefully).


--I pretty much left these alone. They help the Client stay connected.
function queue_push (self, value)
    self[self.right] = value
    self.right = self.right + 1
end
function queue_is_empty (self)
    return self.right == self.left
end
function queue_shift (self)
    value = self[self.left]
    self[self.left] = nil
    self.left = self.left + 1
    return value
end
function new_queue ()
    local queue = {left = 1, right = 1}
    return setmetatable(queue, {__index = {is_empty = queue_is_empty, push = queue_push, shift = queue_shift}})
end
local message_queue = new_queue()
function lock ()
    locked = true
    client_socket:settimeout(2)
end
function unlock ()
    locked = false
    client_socket:settimeout(0)
end



--These tell Lua how to interpret words received from Client, and also, tells Lua what to send back to Client.
--I only use PING, WRITE, and DISPLAY_MESSAGE in this APWorld integration.
request_handlers = {
    ["PING"] = function (req) --Sends & receives this every couple seconds to keep Client and Lua connected. It's the heartbeat; Lua checking Client's pulse. It knows it's disconnected when it stops receiving these.
        local res = {}
        res["type"] = "PONG"
        return res
    end,
    ["SYSTEM"] = function (req) --Tells Client what console is being emulated.
        local res = {}
        res["type"] = "SYSTEM_RESPONSE"
        res["value"] = emu.getsystemid()
        return res
    end,
    ["PREFERRED_CORES"] = function (req) --Tells Client what emulator core is being used.
        local res = {}
        local preferred_cores = client.getconfig().PreferredCores
        local systems_enumerator = preferred_cores.Keys:GetEnumerator()
        res["type"] = "PREFERRED_CORES_RESPONSE"
        res["value"] = {}
        while systems_enumerator:MoveNext() do
            res["value"][systems_enumerator.Current] = preferred_cores[systems_enumerator.Current]
        end
        return res
    end,
    ["HASH"] = function (req) --Tells Client what game we're playing. Thanks for playing by the way!
        local res = {}
        res["type"] = "HASH_RESPONSE"
        res["value"] = rom_hash
        return res
    end,
    ["MEMORY_SIZE"] = function (req) --How big we talkin'? Hahaha jokes aside I never use this.
        local res = {}
        res["type"] = "MEMORY_SIZE_RESPONSE"
        res["value"] = memory.getmemorydomainsize(req["domain"])
        return res
    end,
    ["GUARD"] = function (req) --I don't know what this is for.
        local res = {}
        return res
    end,
    ["LOCK"] = function (req) --Client tells Lua, "hey buddy I'm doing something intensive so don't expect a heartbeat for a couple seconds okay?"
        local res = {}
        res["type"] = "LOCKED"
        lock()
        return res
    end,
    ["UNLOCK"] = function (req) --Puts Lua's finger back on Client's pulse.
        local res = {}
        res["type"] = "UNLOCKED"
        unlock()
        return res
    end,
    ["READ"] = function (req) --Client asks to know something about the game, Lua checks the game, Lua sends info back to Client.
		local res = {}
		return res
    end,
    ["WRITE"] = function (req) --Client tells Lua to update the game in some way.

        local res = {}
        res["type"] = "WRITE_RESPONSE"
        local req_item = req["item_name"]
        local bytes_to_write = nil 
		if req["value"] then
			bytes_to_write = base64.decode(req["value"])
        end


		--Handle writing progressives.
		if req_item == "Progressive A-Type Round" or req_item == "Progressive B-Type Round" then
			--Extract the value from the table array index.
			local target_val = 0
			if type(bytes_to_write) == "table" then
				target_val = bytes_to_write[1] or 0
			else
				target_val = string.byte(bytes_to_write, 1) or 0
			end

			for _, mon in ipairs(MONITORS) do
				if mon.name == "Progressive A-Type Round" and req_item == "Progressive A-Type Round" then
					client_atype = target_val
					mon.write_mem(target_val)
					break
				end
				if mon.name == "Progressive B-Type Round" and req_item == "Progressive B-Type Round" then
					client_btype = target_val
					mon.write_mem(target_val)
					break
				end
			end
			
		--Handle writing location_sent values.
		else
			for _, mon in ipairs(MONITORS) do
				if mon.name .. "_location" == req_item then
					mon.location_sent = 1
				end
			end
		end
		
		return res
    end,
    ["DISPLAY_MESSAGE"] = function (req) --Client tells Lua to pop a message to the player up on the emulator. Nifty.
        local res = {}
        res["type"] = "DISPLAY_MESSAGE_RESPONSE"
        message_queue:push(req["message"])
        return res
    end,
    ["SET_MESSAGE_INTERVAL"] = function (req) --When Client wants Lua to tell the emulator to tell the player something after a delay. Could be used for sneakysneaky...
        local res = {}
        res["type"] = "SET_MESSAGE_INTERVAL_RESPONSE"
        message_interval = req["value"]
        return res
    end,
    ["default"] = function (req) --CLIENT HELP I DON'T KNOW WHAT THIS IS
        local res = {}
        res["type"] = "ERROR"
        local command_type = req and tostring(req["type"]) or "nil"
        res["err"] = "Unknown command: " .. command_type
        return res
    end,
}
--Tells Lua which of the above words Client just sent it.
function process_request (req)
    if request_handlers[req["type"]] then
        return request_handlers[req["type"]](req)
    else
        return request_handlers["default"](req)
    end
end

--Handling for getting the above words from Client.
function send_receive ()
    client_socket:settimeout(0) --No room for error.
    local message, err = client_socket:receive() --Get the word from Client.

	--Connectivity error handling:
    if err == "timeout" then --What if we don't get the word from Client?
        unlock() --Nothing changes, really. Not here, anyway. Leaving this as a placeholder.
        return
    elseif err == "closed" then --What if war is all over now?
		if current_state == STATE_CONNECTED then
			print("Connection to client closed")
		end

		client_socket:close()
		client_socket = nil
		current_state = STATE_NOT_CONNECTED
		return
    elseif err ~= nil then --Wow I have NO idea what just happened...
        print(err) --Here help me figure this out, chief.
        current_state = STATE_NOT_CONNECTED
        unlock() --Placeholder 2. Unlocktric boogaloo.
        return
    end
    
	
    timeout_timer = 5 --Lua gets 5 seconds to send this next part out.
	
    if message == "VERSION" then --Client sends the VERSION word as the initial handshake, and never again.
        client_socket:send(tostring(SCRIPT_VERSION).."\n") --Oh...here's where SCRIPT_VERSION gets used! It's for Client to know what path to take. Yeah, I don't use that.
    else --If not VERSION, then JSON. 
        local res = {} --Build a response.
        local data = json.decode(message) --What's the content?
        for i, req in ipairs(data) do --For every word Client sent...
			local status, response = pcall(process_request, req) --...run the handling for the word. The handlings can be found above the process_requests() function declaration right up there.
			if status then --If we got status then we got a response to send back to Client from Lua.
				res[i] = response --"This is the response for the first word you sent, which will not be the response for the other word you sent, but I'll send that one too on this next iteration give me a sec."
			else --If you don't have status then I won't talk to you.
				if type(response) ~= "string" then response = "Unknown error" end
				res[i] = {type = "ERROR", err = response}
			end
        end
        client_socket:send(json.encode(res).."\n") --Lua tells Client what it wants to say here. In classic Python format. (Yuck.)
    end
end


--This makes Lua able to be connected to by Client. It uses localhost to stay loopback so it isn't open to LAN or wider.
function initialize_server ()
    local err
    local port = SOCKET_PORT_FIRST --Lua's port.
    local res = nil
    server, err = socket.socket.tcp4() --A socket for my socket.
    while res == nil and port <= SOCKET_PORT_LAST do
        res, err = server:bind("localhost", port) --Try to claim the port.
        if res == nil and err ~= "address already in use" then --If the port is already claimed...
            print(err)
            return
        end
        if res == nil then port = port + 1 end --...try the next one.
    end
    if port > SOCKET_PORT_LAST then --Nothing worked. All ports are claimed.
        print("Too many instances of connector script already running. Exiting.")
        return
    end
    res, err = server:listen(0)
    if err ~= nil then print(err) return end
    server:settimeout(0)
end

function main ()
	init()
    while true do
        if server == nil then initialize_server() end --If no Lua server, Lua server.
		
		--Cooldown times for stuff.
        current_time = socket.socket.gettime()
        timeout_timer = timeout_timer - (current_time - prev_time)
        message_timer = message_timer - (current_time - prev_time)
        prev_time = current_time
        
		--Pop messages to the player up on the emulator.
        if message_timer <= 0 and not message_queue:is_empty() then
            gui.addmessage(message_queue:shift())
            message_timer = message_interval
        end
        
        if current_state == STATE_NOT_CONNECTED then --When we're not connected yet, just try to connect.
            if emu.framecount() % 60 == 0 then
                local client, timeout = server:accept()
                if timeout == nil then
                    print("Client connected")
                    current_state = STATE_CONNECTED
                    client_socket = client
                    server:close()
                    server = nil
                    client_socket:settimeout(0)
				end
            end
        else
			if current_state == STATE_DISCONNECTED then --If Client disconnected from the Lua, panic and freak out.
				print("Client disconnected. Please close BizHawk and re-launch Wario's Woods Client to reconnect.")
				message_queue:push("Client disconnected. Please close BizHawk and re-launch Wario's Woods Client to reconnect.")
            elseif current_state == STATE_CONNECTED then
                local checked_items = update() --Do so much stuff.
                if #checked_items > 0 then
					--print("there's items in checked_items")
                    for _, item_name in ipairs(checked_items) do
				        for _, mon in ipairs(MONITORS) do
							if item_name == mon.name then --If A-Type Round 4 == A-Type Round 4...
							
								if DEBUG == true then print("[LUA]: " .. mon.name .. " collected!") end
								
								mon.send_location = 0
								
								--Goal location handling.
								if mon.victory then
									local notify = {type = "VICTORY"}
									client_socket:send(json.encode({notify}) .. "\n") --Send VICTORY to Client instead.
								--Regular location handling.
								else
									local notify = {type = mon.name}
									client_socket:send(json.encode({notify}) .. "\n") --...send A-Type Round 4 to Client.
								end
								
								
							end
						end
                    end
                end
            end

            repeat
                send_receive() --I never set locked=true, so this only fires once.
            until not locked
            
            if timeout_timer <= 0 then
                print("Client timed out. Probably didn't receive a heartbeat from it.")
                current_state = STATE_DISCONNECTED
            end
        end
        coroutine.yield() --I have 0 idea what this does. I don't need to know, really. Something to do with making the script run every frame?
    end
end


--Disable the script to see this message and to turn off the localhost Lua loopback server.
event.onexit(function ()
    print("\n-- Script stopped. Please close BizHawk and re-launch Diddy Kong Racing DS Client to reconnect. --\n")
    if server ~= nil then server:close() end
end)


--The top of the chain. Everything fires from here.
if bizhawk_major < 2 or (bizhawk_major == 2 and bizhawk_minor < 7) then
    print("Must use BizHawk 2.7.0 or newer")
else
    if emu.getsystemid() == "NULL" then
        print("No ROM is loaded. Please load a ROM.")
        while emu.getsystemid() == "NULL" do emu.frameadvance() end
    end
    rom_hash = gameinfo.getromhash()
    local co = coroutine.create(main)
    function tick ()
        local success, err = pcall(function() --Lua's equivalent of a Try/Catch
            local status, coroutine_err = coroutine.resume(co)
            if not status and coroutine_err ~= "cannot resume dead coroutine" then
                error(coroutine_err)
            end
        end)
        if not success then
            print("oh hey your script died")
            print(err)
        end
    end

    event.onframeend(tick)
    while true do emu.frameadvance() end
end


