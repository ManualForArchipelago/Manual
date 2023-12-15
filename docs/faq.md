**Q: What is Manual?**
**A:** Manual is a customizable apworld for Archipelago that can be applied to any game. You tell it what locations you want to be able to check and what items you want randomized, and it gets rolled into a multiworld as normal. Using the ManualClient program, you can manually check off locations that you've checked, and the client will tell you what items you now have access to use. Limiting what items you use is done manually by you until you see the item in the list. The victory condition is also up to you and, once you've completed it, there's a "Victory!" location at the bottom of the location list that you can click to end your seed.

**Q: Is the Manual apworld or this Discord server endorsed by Archipelago?**
**A:** No. Archipelago does not endorse or maintain any portion of Manual. Manual exists as an apworld because Archipelago allows non-endorsed game implementations to do so. This Discord server primarily exists because the main Archipelago server does not want to have a dedicated Manual section at this time. 

**Q: ... But, like, how does it work? What mods do I need?**
**A:** There are no mods. You're the engine that makes it work! You manually perform the checks with the client, and you manually limit the items you can use in-game using the item list in the client.

**Q: What games can I make a Manual apworld from?**
**A:** Literally anything. Since you are manually performing checks and manually limiting your items, you just do it alongside whatever game you're playing. It was originally built to help with AP integrations for games that either disallow modding or that are difficult to mod (like some console games).

It's also been noted that Manual may not work as well for more linear games.

**Q: Okay, cool! Where do I get started with making my own apworld?**
**A:** Check out the "I want to make my own custom apworld..." thread to get started!

**Q: How can I get a channel for the Manual apworld that I created?**
**A:** Start with making your own apworld by following the thread at <#1100815840808542278>, then follow the instructions in <#1101234026125217792>.

**Q: I'm having an issue with Manual in general. Where should I post that?**
**A:** Post in <#1098306155492687892> .

**Q: My game, or my Manual apworld's locations and items, are 18+. Is that allowed?**
**A:** 
There's only two things to avoid here:
     1. Game names, location names or item names of a sensitive nature
     2. Screenshots or descriptions of game content of a sensitive nature

If the game name itself is 18+, you can't include it here. 
If the locations/items would normally be 18+, you'll need to change those. 

Beyond that, you can make a Manual apworld of anything, even something that's 18+.

**Q: What is the difference between a progression item, a useful item, and a filler item?**
**A:**
- Progression items unlock or help to unlock a location check. Any location can have an important item, so these unlocking items need to be marked as progression.
- Useful items are items that you would prefer to get in the game, but that don't unlock any location checks. Stronger armor and weapons would be examples of things in this category.
- Filler items are items that can be found, but these items neither unlock location checks or meaningfully assist the player in completing the game.

In terms of generation, the world generation will prioritize progression items to make a beatable world, and progression items + useful items to make a properly seeded world for a normal playthrough. Filler items may or may not be excluded when the world runs out of locations to place items in.
** **

**Q: Is the code for Manual publicly available?**
**A:** Yes! The code for Manual exists in a fork of the public Archipelago repo, and that fork (and the Manual branch) is on Gitub here: https://github.com/FuzzyGamesOn/Archipelago/tree/manual

**Q: I found a Manual apworld that I want to play. The game name for that apworld has someone else's name in it. Do I need to change that to my name?**
**A:** Nope! The only part of the process that's unique to you is your YAML file. Just set your player name in there like you would with any other game, and you're good to go.

For reference, the user's name in the game name of an apworld is the person that *created* the apworld. This is only so that multiple people can have their own fundamentally different approaches to making a randomizer for their favorite game. You should only ever need to change this if you're creating an apworld from scratch, not when you play one.

**Q: The Manual client comes with a full AP build. Should I use that for generating my multiworlds?**
**A:** No. Use your normal AP install for generating multiworlds. The AP build that comes with the Manual client is just needed for the client to function currently, and is not intended or recommended for generation.
