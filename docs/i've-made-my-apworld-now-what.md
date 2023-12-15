Next is generation testing and running the apworld to make sure what you have works.
Navigate to the archipelago folder you will be using to generate, and place your apworld(s) in [ap folder]/lib/worlds, like so:

Then, place the yaml you created (see: <#1100815840808542278>) in the Players folder, and run `ArchipelagoGenerate.exe`.

If you have an error, you can head to <#1101275452464693408> . Otherwise, you can check your [ap folder]/output folder for a ZIP file, as such:

At this point, you can check the spoiler log inside the .ZIP file, if you want. It's not a necessary part of the step but can help you ensure all of your logic is working as intended, if you generated with a playthrough (on by default).

Run `ArchipelagoGenerate.exe` a couple more times to make sure you have no solo generation issues. Then, head into [ap folder]/Players/Templates and grab some template yamls, pasting them into your Players folder, like so: (Make sure not to grab the yamls for Rom games you don't have, since those will fail generation due to no file path)

Run `ArchipelagoGenerate.exe` 2~3 more times after copying the template .yamls
If all generations go well, your world should be stable to run.

Open `ArchipelagoServer.exe` and select the first output .zip you generated earlier, in [ap folder]/output.
(alternatively, you can drag the .zip onto `ArchipelagoServer.exe`)

Once the server is started, open `ArchipelagoManualClient.exe`. Copy the port as you normally would (e.g. `archipelago.gg:[port]` on the main site, `127.0.0.1:[port]` if running locally). Your Manual Game ID is whatever you have set as your game name in your Yaml (based on the contents on your game.json).

Enter your slot name, and you'll be connected. You can click the `Tracker and Locations` tab to see something like this (some locations collected to better illustrate it):

When you complete the requirements for a location in-game, you can click it to mark that location as checked to the server.
If you want to play a solo run, you can continue from here normally as a test. If you want to join a multiworld session, you can click your locations to see if your item distribution is as intended (optional). Then, separate your .apworld and .yaml to send to the host of the session you are joining.

With your Manual world created, you can also head to <#1097565430442365019>, <#1097565687272177804> or <#1097565784248696903> to share it with others.
