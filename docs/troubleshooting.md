1. Check that the game name specified in your YAML is `Manual_Game_Player`, where `Game` is the `game` entry in your game.json and `Player` is the `player` entry in your game.json.
1b. Check that the game tag (directly above your YAML options) matches the game name in the YAML.
1c. Do **not** change the "player" segment to your own name, unless you are trying to create a completely different version of the world.
2. Check that the filename of your apworld is the game name in lowercase, e.g. manual_game_player (NOT Manual_Game_Player), following the same construction rules from above.
3. Check that your apworld file contains a directory that is named the same as the apworld file (minus the .apworld extension).
4. Verify that the JSON files in your apworld's data directory are correctly formatted using this online validator: https://jsonlint.com/
5. Verify that you have specified no more than 1 Victory location in your locations.json file.
6. Verify that you have as many or more locations than you do items.
7. Verify that you have enough semi-open locations to generate the required items into locations before they end up being needed.
7b. Victory locations do not contain checks. If your amount of items is equal to your total locations including your victory location, you will fail placement due to being one location short.
8. Verify that all items listed in region/location requirements are marked as progression.
9. Make sure you have the latest version from <#1097538892023992350> or <#1097891385190928504>, depending on what you're using. If unsure, you can update again with no issue. This is done by dragging your .json files into the example world for a version.
10. If all of your Boolean Logic requirements are completely broken and all items fail placement: make sure they're not in brackets.
11. If you cannot connect to a world with categories, make sure you have a copy of it in the lib/worlds folder for the manualclient you are connecting from.

If your issue persists, head to <#1098306155492687892> or <#1098306190414450779> for help, depending on the version you are using. There, people willingly take their time to help you, so please be ready to share the .apworld and .yaml of your game for troubleshooting, and see that you have already checked all the steps above. We are here to help, not develop your world for you.