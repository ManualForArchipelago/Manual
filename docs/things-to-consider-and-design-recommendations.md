# Before you start creating your manual
There are a few things you can do before you start working on your manual that can make your life easier in the long run, such as checking <#1100829137830150145> for things that may help you develop or keep track of your world.

## Avoiding Syntax Errors
You can always run your .jsons through a program such as the Json Validator (see: <#1101275452464693408> step 4) to find syntax errors in your json, but it's even easier to have them pointed out to you right as they happen. You have options such as VSCode (https://code.visualstudio.com) you can use to open the .json files with. Whatever you choose, you can then see trailing or missing commas, wrong syntax, etc. as it happens, saving you time later.

## How does your Manual work?
Deciding some things about your game beforehand can save you future headaches.
One major one is how your progression is handled. Is it vanilla, with the Manual items acting as "permission" to use the items you got naturally? Is your player maybe starting from a 100% save file, but with limited access defined by their items? Are there cheat tables, mods or in-game consoles they can use to cheat items in instead? Maybe you're working on a challenge-focused rando, like a move randomizer, or a meta-game with its own rules. You could even be implementing a game where the "Items" are more of an illusion to begin with, like characters in fighting games. Point is: what are your options, and what do you want to do with them?

## What is the intended flow of your Manual?
Think of your logic- not exactly, just in broad terms. Are you designing something line a linear platformer or metroidvania, with a lot of hard requirements? Or are you making something where most things don't have a requirement, with a giant sphere 1? Is your goal to win the game? A Macguffin hunt? Or completion of a set of goals? Bingo boards?
This can be a good time to add artificial logic to space out your spheres, as well (detailed later).

# Development recommendations
How is your Manual affecting the multiworld? It's easy to think of it in a vacuum, but if everyone does so, a session gets increasingly more disorganized the more Manuals are added to it.

## Minimize Filler Items
Specifically, literal nothing items, not Filler items that do something minor. Your amount of Junk items doesn't necessarily impact you. However, it will impact the experience of other players, in a similar way to settings like Hollow Knight Geosanity or Ocarina of Time Potsanity: sending trash more often than not. Except, in this case, it's a literal nothing.

There are occasionally games where junk is simply inevitable by limitations of design. However, there are usually ways to address this:

- Add duplicates of your progression items (or extra copies of your progressive/count items). This also helps if you are having pacing issues, or a game with very frequent BK issues.
- Add better filler. You looked up cheat sheets in a prior step. Can you add free ammo refills? Extra lives? Free powerups? Anything that is minorly helpful, but still fulfills its role as filler.
- Reduce your locations. You may want to check as many locations as possible, but sometimes a game with very few items should have just as few locations. Sometimes a game has few items and a ton of natural, obvious locations. Sometimes, it's avoidable location bloat.
- Rethink the details of your implementation. Was there a type of item you didn't randomize before? Maybe it wouldn't add new locations, but would add more items and logic variety. Did you have an item that could be subdivided for a more interesting implementation? (e.g Weapons, "Cut Rope", etc. into specifics)
- Traps

## What is your pacing, and is it consistent?
Some games are just async-only by nature. Some are really short. Whatever it is, it's important to be aware of it and have some consistency with it.

One source of pacing issues can be an excessively large sphere 1, leading the playthrough logic to expect you to go everywhere at once, leaving others in extended BK. To deal with this, you can add artificial logic gating- anything that makes sense within your world's context, such as stronger gear, area keys, etc. (See <#1098029985048055948> for an example in practice)

Your game might just be too long, especially if you _want_ to play it in a sync. In these cases, it can help to cut down and make your own goal. If you're designing a Manual for an 8-chapter game that you want to be sync-viable, but it's just way too long, then maybe your solution is a "Short" version that only goes up to Chapter 4 as the victory condition. 

On the flipside, you could be randomizing a retro platformer that doesn't last that long. Do you have a level select cheat? You could lock areas with keys, again. If not, there's always move rando to add difficulty instead. Maybe if there's multiple short games you want to play, but you can't see yourself extending their length artificially in any fun way, you could group them together (See <#1097683627992678430> for an example in practice).

## Is something unclear?
Normally, it would be ideal for as much of a world as possible to be self-explanatory. Sometimes, however, that's just not possible without sacrificing something else, like overly verbose names, messy victory conditions, etc.

You can append to this with your documentation: explain the rules, explain how your world works, its limitations, it's mechanics. Ideally, you can make as much as possible self-explanatory in a reasonable way, and then document away whatever doubt is left. Documentation can also have other uses, such as pointing to the mods or cheat sheets you may have found earlier, or favoring specific versions of a game for its compatibility.

Your documentation should fit your Manual's needs, but if you're struggling for ideas, I've attached three of mine as a reference: Quackshot (open-world short platformer using a cheat table), Desktop Dungeons (Level-based Dungeon Crawler with very open design), and Achorepelago (Chore-based metagame)

# The world is done, now what?
With the world done, you have little left to do in terms of design or decisions. However, there are a few things left to keep in mind.

## Distribution
If you want others to play your manual world as well, your template .yaml, .apworld and documentation need to reach players. You can create a thread in <#1097565430442365019>, <#1097565687272177804> or <#1097565784248696903> for it. Your documentation can all go in the thread, but this can lack portability of your Manual, as messages in threads can be missed, especially if they're not the first post. As such, I would recommend providing one download for all your files, including your .yaml and .apworld, but especially any other external tools or documentation necessary to fully play the Manual. How you do this may vary, but I believe the simplest form is to include all in a .ZIP file.

## Pinning
With your thread made and your Manual distributed, you can also request a <@&1097537168047620237>  to pin messages in your thread for ease of visibility.
