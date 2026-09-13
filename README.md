My name is CCtheOwl. I've cobbled these goodies together from myriad sources; mostly my brain, but credited either right here or in-line where otherwise.


To have been there to ask the questions;
And maybe I never learn the answers.
And maybe it's because you don't know the answers.
If all I can give you is a reason to find the answers, then being there was worth it.
Your soul is full of light.


Credit to Manual for Archipelago from which I directly used all .py files in root and hooks that isn't the init or client. I like the architecture.

Credit to my friends, for being supportive of the time and effort I put into this project despite how annoying it is to hear about Archipelago every other day.

Credit to my mother, my role model, and one of the smartest people I know. I've never met anyone more selfless. If the goal of life is to stay young for as long as possible, you've never lost your first place status.
I love my momma.


------------------------------------------------------------------------

QUICK REF

------------------------------------------------------------------------


- To play, double-click the patchfile (slotname_AP_123456789.wwnes) and select Always Run With ArchipelagoLauncher.exe. Then, pick the files it asks for until everything opens up. Connect to the APServer and enjoy.


- Followed all the instructions below, but APWorld won't work? BizHawk configuration preventing you from enjoying the Archipelago? An update somewhere broke something somewhere?
-- Reach out to me in the game's future-game-design post within Archipelago's official Discord server. I'll put together a solution that'll get you and anyone else with the problem fixed right up.

- .yaml's in the .apworld if you don't have it or need a clean copy. Rename to .zip and extract to pull it out.

- I only have one version of the game. If you play the game with a different officially released revision and the Archipelago does not work, reach out to me. I can't be given the dump of your game, so we'll have to work together for a minute.


------------------------------------------------------------------------

COMPREHENSIVE HOW TO USE

------------------------------------------------------------------------


PRE-REQS:

- You need Windows 11, probably. Untested on other operating systems; don't got any, sorry. Happy to update this line if others test and confirm functionality/non-functionality.
- You need Archipelago version 0.6.7 or greater installed. There's a nifty guide at https://archipelago.gg/tutorial/Archipelago/setup_en.
- You need BizHawk version 2.11.1. Won't work with earlier versions. I got mine from https://tasvideos.org/Bizhawk.
- You need water and a snack and maybe attention for your posture because I care about you. Fingers crossed you know where to find these things.
- You need a vanilla ROM, a dump of your legally obtained copy of the game cartridge. I don't understand the law well enough to feel comfortable providing instructions for this. I'm sorry.


STEPS:


1) Generate Archipelago Multiword

- Double-click the .apworld file. It'll install into your Archipelago installation's custom_worlds folder, usually around C:\ProgramData\Archipelago\.

- Adjust the game's .yaml in the way that you prefer, then place it in your Archipelago installation's Players folder. It has its own instructions in it.
-- If you don't have the .yaml, you can rename the game's .apworld file to be .zip instead, then right-click to extract all. The game's .yaml will be inside.

- Open ArchipelagoLauncher.exe, find the list item "Generate", and press its Open button.

- Go to https://archipelago.gg, click GET STARTED in the top right, and click HOST GAME. In the page that loads, click the Upload File button.

- In the filepicker that opens up, navigate to your Archipelago installation's Output folder.
-- If you can't tell which multiworld you just generated, you can right-click them and select Properties to see when the .zip file was created!

- Select the multiworld you generated. Archipelago.gg will handle the rest, creating a https://archipelago.gg/room/.


2) Video Gaming

- If you're not the host that generated the multiworld, double-click the .apworld package to install it, then have your host extract all from the multiworld & send you the patchfile from within it.
-- [yourYAMLslotname]_AP_[123456789].[gamefiletype] is what the patchfile is named like.

- Double-click the patchfile to open it. The first time you open a patchfile with the game's filetype, you'll need to open it with ArchipelagoLauncher.exe, and make sure to select "Always open with this"!
-- Alternatively, you can open ArchipelagoLauncher.exe, click the Open button on the Open Patch list item, and select the patchfile. That'll basically do the same thing as double-clicking it.

- The first time you open the patchfile, it'll open a filepicker for you to select your EmuHawk.exe, and then it'll open another filepicker for you to select the vanilla dump of your game.
-- It'll remember where those are for next time, so you won't have to do that again the next time you double-click the patchfile. The game and all the necessities should open right up!

- The patchfile will create a patched rom, and place it in the same folder as the patchfile, named the same thing as the patchfile, but with the console's filetype instead of the game's filetype.
- Don't open the game with that. None of the things Archipelago needs in order to connect to the APServer will open along with it. You should always open the game by double-clicking the patchfile.

- After everything opens and starts running, the Archipelago GUI client will manifest itself. 
-- Go to the https://archipelago.gg/room/ you or the host created earlier & retrieve the port (the five numbers at the end of the /connect archipelago.gg:##### found in the room).
-- Paste it overtop the placeholder port in the URL bar at the top of the Archipelago GUI Client.

- Hit the Connect button, and when it asks for it, type in your slot name, also found in the https://archipelago.gg/room/. Then hit enter.

- The Client will connect, bridging the actively running Lua to the actively listening APServer hosted on Archipelago.gg. You're all set up! Happy gaming!


3) Upkeep

- If the Lua and Client disconnect from each other, close BizHawk and the Client, then reopen the patchfile. You'll know if they're disconnected. BizHawk will totally freak out.


------------------------------------------------------------------------

AI DISCLOSURE

------------------------------------------------------------------------


To my knowledge, this APWorld contains nothing that was generated by an AI. I have spent a great deal of effort in avoiding AI usage for this.
If there is a mistake, it was my mistake to make, and it is my mistake to fix. Bring bugs to me; I will make an attempt to fix them.

If there is a best practice or standard that was not followed, it is because that best practice or standard was buried, or unwritten in a location where it would be obvious for the average individual to look for it.
I have read a lot, and I have understood little. The current Archipelago instructional documentation is not friendly. Where it is not sparse, it is vague. There is no reason it cannot suggest typical approaches to problems every AP dev faces.
My entire stack is Notepad++, for the same reason as above. I'm still a bit salty about that. Do not bring formatting practices to my attention.
Bring programming practices to my attention. I will hear those, and make an attempt to incorporate them.

