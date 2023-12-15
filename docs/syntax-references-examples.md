This is a thread to collect Syntax References for various features that users may be uncertain about.
**"OR" arguments:** TBD
**Items with quantities:** TBD
**Victory location:** TBD
**Categories:** TBD
**Regions:** TBD
**Boolean Logic:** TBD
**Pre-placing Items:** TBD
**Advanced Starting Inventory:** TBD

# "OR" arguments in logic
Say Chest requires Sword, and either Bombs, Magic or a Shield
The implementation of a location with an OR without Boolean Logic is as such:
```json
  { 
        "name": "Chest", 
        "requires": [
            "Sword",
            "Bombs"
            { 
                 "or": [
                    "Sword",
                     "Shield"
                ]
            },
            { 
                 "or": [
                    "Sword",
                    "Magic"
                ]
            }
        ] 
    }```
Essentially, every possible set of items that can open the check is contained within one "OR".

This can also be handled with Boolean Logic, as such:
```json
    { 
        "name": "Chest",
        "requires": "|Sword| and (|Bombs| or |Shield| or |Magic|)"
    }```
Essentially, it's how you would write it out as a sentence, plus parenthesis to group "layers" of logic, and |Pipes| surrounding item names to indicate to the parser when an item starts an ends. If you misplace your pipes, it may read incorrectly:
```json
     "requires": "|Sword| and (|Bombs| or |Shield or Magic|)"```
for example, will search for two items: `"Bombs"`, or `"Shield or Magic"`
For further details on Boolean Logic, see the Boolean Logic section.

# "Count" Items
There are two parts to a count item: the item and the requirement. Let's say there are 50 Stars in the game, and Door 1 requires 12 of them or a Door 1 Key.
The syntaxes are as such:

in items.json
```json
    { 
        "name": "Star",
        "count": 50, 
        "progression": true
    },
    { 
        "name": "Door 1 Key",
        "progression": true
    }```
You can have non-progression count-items, but in this case, Star is progression since it's part of a location's requirements.

in locations.json
```json
    { 
        "name": "Door 1", 
        "requires": [
            "Star:12",
            { 
                "or": [
                    "Door 1 Key"
                ]
            }
        ] 
    }```
As you see, it's written the same as any other item in a location, without a `"count": X` argument. You simply write in `Item:Amount` as opposed to just `Item`.

# Victory Locations
Victory is a singular argument, like "count", but in a location. If you had a Final Door requiring Key 1, Key 2 and Key 3 as your Victory location, you could write it as such:
```json
{ 
        "name": "Final Door", 
        "requires": [ "Key 1", "Key 2", "Key 3" ],
        "victory": true 
    }```
You can combine a Victory location with any other logic, but you **can only have one victory location.**

# Categories
Categories are an argument like "victory" and "count", except it requires [Square Brackets] because it can contain multiple items. Their syntax is the same for both locations and items (respectively):

```json
{ 
        "name": "Kill First Boss", 
        "category": ["First Dungeon", "Boss Fight"], 
        "requires": [ "Sword" ]
    }```

```json
{ 
        "name": "Coins",
        "category": ["Currencies"]
        "count": 25, 
        "progression": true
    }```

Categories do not affect logic, but will group items up as they display in the client, and locations will be able to be set to give an item from a specific category
Above, Kill First Boss is part of two categories at the same time, while Coins is only part of Currencies.

# Regions
Regions are a combination of their own thing (in regions.json), and a feature for Locations.
Say I have three locations, with the following requirements:
Grasslands Ledge: Grasslands Map, First Key, Double Jump
Grasslands Lake: Grasslands Map, First Key, Swim
Grasslands Boss: Grasslands Map, First Key, Sword

However, Grasslands Map and First Key are just what I use to get to the Grasslands. If I'm already _in_ the region, those items only require Double Jump, Swim and Sword respectively. My option, with Regions, is as such:

in regions.json
```json
    "Grasslands": {
        "requires": [ "Grasslands Map", "First Key" ]
    }```

in locations.json
```json
{ 
        "name": "Grasslands Ledge", 
        "region": "Grasslands", 
        "requires": [ "Double Jump" ]
    },
{ 
        "name": "Grasslands Lake", 
        "region": "Grasslands", 
        "requires": [ "Swim" ]
    },
{ 
        "name": "Grasslands Boss", 
        "region": "Grasslands", 
        "requires": [ "Sword" ]
    }```
As such, all locations still keep their three requirements. However, two of them are part of their "region", rather than the specific location.

Regions can also connect to each other. Say we have a linear game with 4 Worlds, requiring 0/5/10/15 coins and their "World Key" to enter, except for the first world:
```json
{
    "World 1": {
        "requires": [],
        "starting": true,
        "connects_to": [
            "World 2"
        ]
    },
    "World 2": {
        "requires": [ "Coin:5", "World 2 Key" ],
        "connects_to": [
            "World 3"
        ]
    },
    "World 3": {
        "requires": [ "Coin:10", "World 3 Key" ],
        "connects_to": [
            "World 4"
        ]
    },
    "World 4": {
        "requires": [ "Coin:15", "World 4 Key" ]
    }
}```
Now, every time I make a level, I can assign it to a region. Of note, access to the starting region is assumed to always be possible, and connects only move "forwards" from there.

if no regions are marked as "starting", Manual will assume they can all be reached from anywhere once their requirements are met, while if at least one region is marked as "starting", any non-starting region will have to be reached through connecting regions.

So, if Level 4-1 requires access to World 4 and Double Jump, instead of
```json
{ 
        "name": "Clear 4-1",  
        "requires": [ "Coin: 15", "World 4 Key", "Double Jump" ]
    }```
I can do the simplified form of
```json
{ 
        "name": "Clear 4-1",  
        "region": "World 4",
        "requires": [ "Double Jump" ]
    }```Which simplifies the formatting of the logic, especially for more complex games.

Regions can be used for any recurring logic set. Biomes are the obvious usage, but if you have a puzzle game with 5 tools and it's very common for Puzzle Type A to need Tools 1, 2 and 4:
```json
    "Puzzle Type A": {
        "requires": [ "Tool 1", "Tool 2", "Tool 4" ]
    }``````json
{ 
        "name": "Puzzle 34", 
        "region": "Puzzle Type A", 
        "requires": []
    }```

Or if have an RPG with logic based on player strength and encounter levels...
```json
    "Level 20s": {
        "requires": [ "Stat Up:4", "Progressive Weapon:2", "Skill Point:7" ]
    }``````json
{ 
        "name": "Dungeon 3 Wooden Chest", 
        "region": "Level 20s", 
        "requires": ["Key"]
    }```
In essence, regions can have many uses depending on what you need for logic grouping in your world.

# Boolean Logic
Boolean logic is written similarly to how you would describe it in a sentence, with (parentheses) for layers and |pipes| for item names. Let's look at three examples:

Boss 1 Requires Ladder and Gloves, OR Sword and Shield, OR Bow and Quiver and Arrow (separate items): a simple case of various successful item sets. It's a few sets of ANDs separated by ORs.
```json
  { 
        "name": "Boss 1",
        "requires": "(|Ladder| and |Gloves|) or (|Sword| and |Shield|) or (|Bow| and |Quiver| and |Arrow|)"
    }```

Boss 2 simply requires five hearts, a way to strike it (Sword, Spear or Club) and a way to dodge it (Double Jump, Dash or Slide): we're looking at different sets, and picking one item from which. It's many ORs inside a big set of ANDs.
```json
  { 
        "name": "Boss 2",
        "requires": "|Hearts:5| and (|Sword| or |Spear| or |Club|) and (|Double Jump| or |Dash| or |Slide|)"
    }```

Now, say the final boss is a big dragon with a glaring weakness to Blizzard. However, if you don't have blizzard, you will need a spear for its reach and a way to dodge it, which is one of the three mobility from before. This is an OR (the mobility), inside an AND (Spear and Mobility), inside an OR (Blizzard it or fight it legitimately). Layered logic is as such:
```json
  { 
        "name": "Final Boss",
        "requires": "|Blizzard| or (|Spear| and (|Double Jump| or |Dash| or |Slide|))",
        "victory": true
    }```

To illustrate (for ease of understanding, will not work in the code):
`|Blizzard| or (|Spear| and (|Double Jump| or |Dash| or |Slide|))` represents `|Blizzard| or (|Spear| and <some form of mobility>)`, which itself represents `|Blizzard| or <fight it legitimately>`.
You can build your logic in layers this way. There's no theoretical limit to how many you use, but try to not get past the practical limit of how many sets of parentheses you can reliably keep track of.

# Preplacing Items
If you want to pre-place items (a.k.a. force locations to have a specific item, or an item from a specific set), you have two resources for this: `place_item` and `place_item_category`

The simplest example is a one-to-one situation. Say a boss fight, "Boss A", gives an in-game key, "Key X". You want "Key X" as an item to use for your logic, but you want to keep it tied to "Boss A".

```json
    {   "name": "Kill Boss A", 
        "requires": ["The Items That Kill Boss A"],
        "place_item": ["Key X"] }```

This will ensure that the "Kill Boss A" location will always award your "Key X" item.

If you had multiple keys you wanted as possible rewards, you could list them all, separated by commas:
```json
    {   "name": "Kill Boss A", 
        "requires": ["The Items That Kill Boss A"],
        "place_item": ["Key X", "Key Y", "Key Z"] }```
This doesn't give all three keys: It guarantees one random drop, selected between those 3 keys.

If you wanted it to give _any_ key from a category you already have, you would use `place_item_category` instead:
```json
    {   "name": "Kill Boss A", 
        "requires": ["The Items That Kill Boss A"],
        "place_item_category": ["Boss Keys"] }```
The location will award any item in the "Boss Keys" category. Like `place_item`, you can list multiple categories - it will pick a random category, and place a random item from that category.

The following will work:
```json
{   "name": "Area A",
        "requires": [],
        "place_item_category": ["Keys and Boots"] 
},
{   "name": "Area B",
        "requires": [],
        "place_item_category": ["Keys and Boots"] 
},
{   "name": "Area C",
        "requires": [],
        "place_item_category": ["Keys and Boots"] 
},
{   "name": "Area D",
        "requires": [],
        "place_item_category": ["Keys and Boots"] 
}```
This will distribute your 2 keys and 2 boots randomly between the locations.

However, this will fail:
```json
{   "name": "Area A",
        "requires": [],
        "place_item_category": ["Keys", "Boots"] 
},
{   "name": "Area B",
        "requires": [],
        "place_item_category": ["Keys", "Boots"] 
},
{   "name": "Area C",
        "requires": [],
        "place_item_category": ["Keys", "Boots"] 
},
{   "name": "Area D",
        "requires": [],
        "place_item_category": ["Keys", "Boots"] 
}```

The reason for this is that every location will pick a category randomly. If A, B and C all pick "Keys", for example, you'll be trying to divide 2 keys among 3 locations. One will be empty, and will error.

This is only really a risk if you are working with small item pools, or item pools of comparable size to the locations they're placed in: If you have 60 pieces of equipment and want your 12 bosses to each give a random piece guaranteed, you're extremely unlikely to run into any issues doing it that way.

# Advanced Starting Inventory
This is the first feature to reside in game.json instead of items, locations or regions.
Fuzzy's example world covers every use of it, so I will just show them and explain one by one:
```json
{
    "game": "20230611",
    "player": "Unstable",

    "filler_item_name": "Free Character of Your Choice",

    "starting_items": [
        {
            "items": ["Ryu", "Akuma"]
        },
        {
            "item_categories": ["Left Side"],
            "random": 1
        },
        {
            "items": ["Wolverine", "Storm", "Phoenix"],
            "random": 1
        },
        {
            "item_categories": ["Trash"]
        },
        {
            "random": 3
        }
    ]
}```

There are five conditions here. Let's look at them one by one:
```json
        {
            "items": ["Ryu", "Akuma"]
        },```
There's no `random:` argument here - this is a straight up list, not a raffle. If you list `"Items": ["X", "Y", "Z"]` without an extra argument, the player starts with __all of them__.

```json
        {
            "item_categories": ["Left Side"],
            "random": 1
        },```
Here, it's shown `"item_categories"`: is a valid argument as well. More importantly, `"random": 1` - we're adding __1 random item from the category__. If that wasn't there, this would _add the entire category into the starting inventory_.

```json
        {
            "items": ["Wolverine", "Storm", "Phoenix"],
            "random": 1
        },```
Back to individual items, now with `"random": 1` as well. This will add 1 of those items, randomly. If you had `"random": 2`, it would add 2 instead, and so on. So we get Wolverine, OR Storm, OR Phoenix.

```json
        {
            "item_categories": ["Trash"]
        },```
This works like the first one, except with categories instead of items. There's no `"random": X` argument, so you're getting __every single item in the Trash category__.

```json
        {
            "random": 3
        }```
Lastly, this has a `"random": X` argument, but no set to pull it from. This will add __any 3 random items__ to the start inventory.

So, in total, we're starting with:
- Ryu and Akuma
- 1 random item from the "Left Side" category
- 1 of ["Wolverine", "Storm", "Phoenix"]
- Every item in the "Trash" category
- 3 Random items

for a generic format of:
```json
        {
            "items"/"item_categories": ["List"],
            "random": X
        },```
As observed. if there is no `"random": X` it'll add every item it can find, and if there are no item sets specified, it will pick from every item in the world.
