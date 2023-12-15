Manual is a customizable apworld for Archipelago that allows you to make a custom multiworld integration for any game by specifying a list of items that you can receive and a list of locations that you can check.

The name "Manual" comes from the fact that it doesn't automatically randomize anything. Rather, you manually handle when locations are checked off the list, and you limit the items that you can use in-game until they are sent to you in the multiworld. Some call it the "honor system"!

Locations can be locations in the game, goals that you have in a bingo-style format, or even timer-based goals like ArchipIdle might use! Same with items... They can be actual items in the game, or limiting factors to add more of a challenge, or even arbitrary keys that gate certain areas of the game to create a keysanity-like play mode!

This system understandably doesn't work for very linear games, since you have to have some method of navigating the game to unlock items and locations normally. However, it does work well for a wide variety of use cases, including:

- Video games across multiple genres
   - Especially games with open locations or new game plus modes
- Board or card games, or other physical games
- Even things that aren't even games!

Check out the FAQ section in this forum for more information on questions that you might have!

When using Manual, there are a few files that you'll frequently need to update when creating your own custom Manual apworld. 

Below, we'll talk about the purpose of each of those files. Once you have a good understanding of the "what" from the info below, you can hop over to <#1100815840808542278> to get the "how". 😄 

**The Game file - data/game.json**
Your game file defines important identifiers for what your game should be called. There's a game and a player entry, because the player entry is used as a suffix to differentiate your version of a game's apworld from someone else's -- in case you both had the same great idea!

If you were making an apworld for Link to the Past, for example, your game.json might have  `LinkToThePast` for the game entry and `You` for the player entry.

**The Items file - data/items.json**
Your items file lists things that you can be sent in your custom Manual randomizer. These can be items in the game, or can be things that you made up to gate certain paths in your playthrough.

Your items file also keeps up with whether those items are progression (unlocks a check), useful (nice to have and shouldn't be excluded), a trap (basically filler but dangerous to the player), or filler (the default, which is something that can fill space or be excluded). You can also keep up with multiples of an item by giving the item a count.

**The Locations file - data/locations.json**
Your locations file lists anything that is a "check" in your randomizer. You get a freebie check at the start? It's a location. You do something to get an item? It's a location.

If your location requires you to have certain items first, you can use requires to state that it should only be possible once you have them.

The victory location that triggers the end of the seed is added for you automatically by Manual. If you want requires for the victory location, you can add a custom victory location with its own requires.

**The Regions file -- data/regions.json**
Your regions file is responsible for specifying world layout groups in your world that locations would belong to. Think of regions as being like countries in the real world, and locations as cities in those countries.

Regions are optional, but can help to group together locations. When you specify region names, you'll need to update your locations file to make sure some locations have their region set to the region name that you specified.

Examples of regions in games might be "Overworld" / "Nether" / "The End" for Minecraft, or "Hyrule Castle" / "Eastern Palace" / "Death Mountain" for Link to the Past.

--------------------------------------

Now that you know all about Manual, it's time to make your own custom world! Jump over to <#1100815840808542278>  to get started. 😁
