**Video Instructions**
This video gives an overview of a step-by-step approach to creating an apworld, and it is *highly* recommended that you watch this before asking questions.

https://www.youtube.com/watch?v=oK-gHpwuJZQ

Made it through the video? Great! Below is a rundown of text instructions for the step-by-step.

**Text instructions - Creating your world**
1. Get the compiled custom ManualClient for AP from the pins in <#1097538892023992350> .

2. Get the example YAML file from the pins in <#1097538892023992350> . Any YAML will work, since we'll talk about how to modify it.

3. Get the example Manual apworld file from the pins in <#1097538892023992350> and extract it like a zip to its own directory. In this case, you will always want the most recent apworld pin.

4. In the folder within, navigate to the "data" directory and update the game.json, items.json, locations.json, and regions.json files. It's okay to have an empty regions.json file (with just `{}` inside).
  - Game name and player name should have no spaces
  - Player name does not have to match the player name in a multi
  - List of locations should be equal in length or longer than items. If you need duplicate items, use a suffix. 

5. Once you've updated the JSON files, rename the `manual_xx_xx` directory that "data" is in to `manual_<your game name>_<your player name>`.

At this point, you can test out generation with your world to see if it works! Once you have it working, keep reading below for instructions on prepping the world for sharing.

**Text instructions - Sharing your world**
1. Right-click the `manual_<your game>_<your player>` directory and zip it. You *must* create a .zip file. .rar or others will not work.

2. Change the extension from .zip to .apworld. Delete or move the f`manual_<your game>_<your player>` directory that you created the .zip file from, so there aren't duplicate world definitions.

3. Update your YAML file of choice to replace `Manual_xx_xx` with `Manual_<your game>_<your player>`. You'll need to update this in 2 places in the YAML.

4. Place your apworld in the `lib/worlds` directory underneath the extracted client zip from step 1.

5. Open the ManualClient from the extracted client zip from step 1, and replace the game name text field with your `Manual_<your game>_<your player>` string from the YAML. 

6. Connect as normal using the player name in your YAML. Use the "Tracker and Locations" tab to keep track of collected items and to check off locations.

7. If you want to test out how a playthrough might go, click some location buttons to see! You can even click the Victory button to finish your seed.
