# Hooks in Manual
If you've been on our Discord server for a while, you've probably heard about Manual hooks. And that has probably made you wonder **what hooks are**, or **what hooks are for**, or **what hooks are available**, or **how you would use hooks**. So let's clarify that some here.

## What are hooks?
Hooks are empty functions that we provide by default in Manual apworlds. Those empty functions are called at each stage of a Manual world's generation as part of a multiworld. So if you put your own custom code in those empty functions, you can do custom things at any stage during generation!

## Okay, but... what are hooks for?
The two main uses of hooks are to:

1. Add functionality to your apworld that isn't possible through Manual's template syntax in its JSON files
2. Add custom functionality to your apworld that would only be possible with custom code, like further randomization or customization of the generated world

(Also, if you don't know why you need hooks, you probably don't need them.)

## What hooks are available?
Manual provides hooks for the most important steps in Manual's own processing of your templated world, and hooks at AP generation steps leading up to the actual fill step (which marks the end of generation, for our purposes).

Hooks are organized into the files that they would affect in the Manual apworld, and those hook files are broken down as follows:

- **\_\_init\_\_.py** - This is typically unused, but can be useful for code that should run on world import. Like registering a custom client.
- **World.py** - <ins>This is where the majority of your hooks code will likely go</ins>. Includes functions for the main AP generation steps leading up to the actual fill step. These hook functions are called from the Manual apworld's top level \_\_init\_\_.py file.
- **Data.py** - Includes functions that can be used to customize the raw data coming in from your Manual template JSON files. These hook functions are called from the Manual apworld's top level Data.py file.
- **Helpers.py** - Includes functions that can be used to add custom logic for helper methods used by Manual, which is currently limited to checking if items/locations/categories should be enabled or not. These hook functions are called from the Manual apworld's top level Helpers.py file.
- **Items.py** - Includes functions that can be used to modify the raw item table before the Manual apworld uses it. In a lot of cases, using this and using the item table functionality in Data.py will be the same. These hook functions are called from the Manual apworld's top level Items.py file.
- **Locations.py** - Includes functions that can be used to modify the raw location table before the Manual apworld uses it. In a lot of cases, using this and using the location table functionality in Data.py will be the same. These hook functions are called from the Manual apworld's top level Locations.py file.
- **Options.py** - Includes functions that can be used to create or customize options for your apworld, including the default options that Manual provides. These hook functions are called from the Manual apworld's top level Options.py file.
- **Regions.py** - Includes functions that can be used to modify the raw region table before the Manual apworld uses it. In a lot of cases, using this and using the region table functionality in Data.py will be the same. These hook functions are called from the Manual apworld's top level Regions.py file.
- **Rules.py** - This hook file operates differently from the others. It is here for you to define your own custom requirement functions, which you'll find a few examples of at the top of the file. Once you define those custom requirement functions, they can be used in the requires syntax of locations and regions.

I know that was a lot of info. For simplicity's sake, you will want to focus on the hook files **World.py**, **Options.py**, and maybe **Rules.py** to start. The others are for more niche usage.

## Okay... how would I use hooks?
This depends on what you want to do. Let's talk through **some common scenarios** below and see where you might want to dig in with hooks. (In all cases, assume that the explanation ends with "and then you write custom code to accomplish this.")

### "I want to add a YAML option that will do something custom for my world."
I'm not sure you need my help finding the place for this one. :) Either hook in Options.py works for this, and you'd put your option definition there too. I'd recommend using the `after_options_defined` hook in Options.py, though, so you have the option to both create your own options or customize Manual options.

The custom thing that happens when the option is accounted for, however, would just go wherever that functionality would go normally. As in, when it's not controlled by an option.

### "I want to change the quantity of an item or items dynamically, or split that item's classification between two classifications."
Sounds like you want to change items in the item pool during generation, so you want World.py. The item pool is handled in the "create_items" step of generation. The likely hook you want is `before_create_items_filler` in World.py, so that you still let Manual properly add filler items at the end.

### "I want to dynamically change the requirements of a location or region."
Sounds like you want to change regions or their locations during generation, so you want World.py. The regions and their locations are handled in the "create_regions" step of generation. The hook you want is `after_create_regions` in World.py, so that you can take the AP regions and locations that were created from Manual's template JSONs and modify them.

### "I want to dynamically change my world's starting items."
Sounds like you want to change items in the player's state and in the item pool during generation, so you want World.py. The item pool is handled in the "create_items" step of generation. Since you want to affect starting items, you'd have to do it right after the hook that comes before starting items... so you're likely looking at using the `before_create_items_filler` hook in World.py.

### "I want to dynamically change my world's filler items."
Sounds like you want to change items in the item pool during generation, so you want World.py. The item pool is handled in the "create_items" step of generation.  From here, there's a split depending on what you want to do. 

If you want to just customize your filler entirely, use the `before_create_items_filler` hook in World.py. 

If you want Manual to place filler as it normally would, and then you want to customize that somewhat, use the `after_create_items` in World.py.

### "I want to reduce duplication with my location/region requires, or I want to dynamically handle those requires."
Sounds like you want to use requirement functions to either simplify your requirements or apply some custom code to them, so you want Rules.py. Unlike with the other suggestions, there is no specific function to look for. You'll be writing your own function in the hook file Rules.py, and you'll likely want to reference the few functions at the top of that hook file as examples.

## BONUS: How to find objects to use in hooks
You have to read some code. Some Manual code, some Archipelago code.

These steps will get you there:

1. Open `\_\_init\_\_.py` (the non-hook folder one) in your Manual apworld and look for the hook function calls. Read what Manual is doing around those. Then read the rest of the file.
2. Download Archipelago source from their GitHub (linked in the site's FAQ).
3. In that AP source folder, open `BaseClasses.py`. Look for and read through the following classes:
    - Item
    - ItemClassification
    - Location
    - Region
    - Entrance
    - CollectionState
    - MultiWorld
4. In that same AP source folder, open `AutoWorld.py`. Look for and read through the following classes:
    - World
5. In that same AP source folder, open `Main.py`. Do a find for "generate_early" and start reading the main() function from there.
6. For any questions you have about the code inside the Manual apworld, ask in the Manual Discord.
7. For any questions you have about code in the AP source folder, ask in the Archipelago Discord. (Or in the Manual Discord, we generally try to help with that too!)
8. Go back to step 1 and do the steps again until you're comfortable enough to mess around and experiment with hooks. **Nobody writes hooks without experimenting and getting it wrong first.**

Good luck!
