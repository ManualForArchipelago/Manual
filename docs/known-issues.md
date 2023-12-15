As with upcoming features, we figured it would be useful to have a list of known issues and fixes.

**The "All" and "Manual" tabs of Manual Client displays multi-item names with the counter (e.g. "Received Power Stars:80").**
Update your "Count" items to the latest stable version, as per https://canary.discord.com/channels/1097532591650910289/1097532592355545130/1099457296486109285

**I'm getting an Invalid Slot error when I try to connect with the ManualClient.**
Invalid Slot means that either your YAML player name is wrong or that it doesn't exist in the server you're trying to join. Make sure that you're using the right generated AP multiworld and that you're typing your player name exactly as it is in your YAML file. If all else fails, clear out your `output` and `Players` directories in your AP install and generate from scratch with a new YAML.

**I'm getting an error when trying to generate my custom apworld.**
Check your game.json, items.json, and locations.json in an online JSON validator like: https://jsonlint.com/

**I can't connect (to a game that has Categories).**
The latest client pulls from a local .apworld for its categories. Make sure you have a copy of the .apworld you're connecting to in your lib/worlds folder of your client. This is intended behavior.

If fixing those issues doesn't resolve it, make sure that you don't have both a folder and an apworld -- with the same names -- in your worlds folder. Also check that your YAML game name and the key for your YAML options are both `Manual_Game_Player`, where `Game` is your "game" entry from game.json and `Player` is your "player" entry from game.json. Also make sure that your apworld filename is that same format, but lowercase. Same with the directory inside the apworld.
If the issues remain, check <#1101275452464693408>, then ask in <#1098306155492687892> or <#1098306190414450779> if needed.

**The buttons in the manualclient don't work.** (With the errors below)
After reconnecting in any form, including failing to connect or closing the program, the problem should fix itself.