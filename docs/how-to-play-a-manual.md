# Playing a Manual
This post assumes you are familiar with local generation of officially supported games, as that is outside the scope of Manual's documentation.
If you are not, please read through AP's guide on multiworld setup first: https://archipelago.gg/tutorial/Archipelago/setup/en

1. Download the latest Manual Client from <#1097538892023992350>. If you are playing with unstable-only client features, you may need to grab an unstable client in the <#1097891385190928504> pins instead.
2. Locate the worlds you want to play and their associated yamls, as well as the location of your Archipelago installation.
3. Go into your Archipelago folder, then into the `lib` folder, then the `worlds` folder. You should see all your existing worlds; move the Manual .apworlds here as well.
4. Place your Manual yamls into the `Players` folder, like you would with official Yamls
5. Run ArchipelagoGenerate.exe to generate a multiworld in the `output` folder.
6a. Upload that generation to the website, at https://archipelago.gg/start-playing, to host it on the webhost
6b. Run ArchipelagoServer.exe and select your output file from your `output` folder (or drag it onto ArchipelagoServer.exe), to host it locally
7. Open your Manual Client folder (from step 1) and open ArchipelagoManualClient.exe
8. Input the server address and port as usual, then input your game's full ID in the "Manual Game ID" field (this is the same one found in your yaml and .apworld name, **which you should not change**), then click "Connect".
9. You are now connected. Head to the Locations tab and click on location names as you complete them to send out their contents. Click on the "Victory" location once you reach your goal.

This is where you can find your Game ID.
In this case, you'd enter "Manual_ZMDebug_Owl", case sensitive.

# Updating a Manual
You should be able to play most Manuals just fine. Some, however, are old enough that they lack compatibility with the latest client. In these cases, you may need to update it yourself.

To update a Manual apworld:
1. Open your .apworld and write down the name of the folder inside it (for example, "manual_zmdebug_owl", always in all lowercase)
2. Download the latest example .apworld (not the manual client) from <#1097538892023992350> (for example, "manual_20230611_unstable.apworld")
3. Extract the .apworld (you may rename the file extension to .zip, but it's easier to just associate .apworld with your extractor of choice)
4. Go into the resulting folder, then into the `data` folder:
5. Delete the contents of this `data` folder
6. Extract the .apworld you're trying to play, and navigate to its own `data` folder
7. Copy the .jsons from the `data` folder of the .apworld you're trying to play to the now-empty `data` folder of the example world
8. Rename the example world's folder to the _exact same name_ you wrote down in Step 1 (in this case, I would rename "manual_20230611_unstable.apworld" to "manual_zmdebug_owl")
9. Add the newly renamed folder to a .zip file with the same name (in this case, "manual_zmdebug_owl.zip")
10. Rename the .zip extension to .apworld (in this case, "manual_zmdebug_owl.apworld"). You now have an updated world.
