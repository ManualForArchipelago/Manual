## Randomised Starting location

Randomising the starting location is one of the harder problems an open-world manual can run into.  

The way Archipelago handles regions and backtracking can be unintuitive, and often makes people feel like this is impossible.

It's not impossible, and it doesn't even require hooks!  Let's dive in.

## Items.json
Our example today is a hypothetical pokemon game.  It has towns, it has routes, it has HMs required to traverse the routes.  
I'm using kanto names for geographical convenience, but the logic will not line up with any of the five mainline appearances of Kanto.
```json
[
  {"name": "HM01 Cut",               "progression": true, "category": ["HMs"]},
  {"name": "HM03 Surf",              "progression": true, "category": ["HMs"]},
  {"name": "HM04 Strength",          "progression": true, "category": ["HMs"]},
  {"name": "HM05 Flash",             "progression": true, "category": ["HMs"]},
  {"name": "Starting Town: Pallet",   "progression": true, "category": ["Starting Town"]},
  {"name": "Starting Town: Viridian", "progression": true, "category": ["Starting Town"]},
  {"name": "Starting Town: Cerulean", "progression": true, "category": ["Starting Town"]},
  {"name": "Starting Town: Lavender", "progression": true, "category": ["Starting Town"]},
  {"name": "Starting Town: Cinnabar", "progression": true, "category": ["Starting Town"]},
]
```

## Game.json
Nothing too special here.  We just need to set up a starting town in starting items.
```json
{
  "game": "Kanto Example",
  "creator": "Manual Team",
  "filler_item_name": "Potion",
  "starting_items": [
    {
      "item_categories": ["Starting Town"],
      "random": 1
    }
  ]
}
```

## Regions.json
This is the part where things get interesting.  We're going to use `"entrance_requires"` to make traversal from the "Manual" region require your starting town.

```json
{
    "Pallet Town": {
        "connects_to": ["Route 1", "Route 21"],
        "starting": true, // This establishes a connection from the default "Manual" region to this region
        "requires": "",   // Getting here via routes is free
        "entrance_requires": {
            "Manual": "|Starting Town: Pallet|"  // Getting here from the start of the game requires the "Starting Town: Pallet" item.  This effectively nullifies the `"starting": true` for any region that wasn't your starting item.
        }
    },
    "Route 1": {
        "connects_to": ["Pallet Town", "Viridian City"],
    },
    "Viridian City": {
        "connects_to": ["Route 1", "Route 2", "Route 22"],
        "starting": true,
        "entrance_requires": {
            "Manual": "|Starting Town: Viridian|"
        }
    },
    "Route 2": {
        "connects_to": ["Pewter City", "Diglett Cave"],
        "requires": "|HM01 Cut|"
    },
    "Pewter City": {
        "connects_to": ["Route 2", "Route 3"],
        "starting": true,
        "entrance_requires": {
            "Manual": "|Starting Town: Pewter|"
        }
    },
    "Diglett Cave": {
        "connects_to": ["Route 2", "Route 11"],
        "requires": "|HM05 Flash|"  
    },
    "Route 21": {
        "connects_to": ["Pallet Town", "Cinnabar Island"],
        "requires": "|HM03 Surf|"
    },
    "Cinnabar Island": {
        "connects_to": ["Route 20", "Route 21"],
        "starting": true,
        "entrance_requires": {
            "Manual": "|Starting Town: Cinnabar|"
        }
    }
}
```

I hope this makes sense.  Every town is given `"starting": true`, and then given an additional entrance requirement when trying to enter the region via that starting link.

A couple important things to note:
* Unlike most manuals, all your links must be bidirectional.  Pallet links to Route 1, and Route 1 links to Pallet.
* For the sake of simplicity, I've kept all the logic on the routes.  You do not want to add any requirements that would stop your starting town from being usable as a starting town.
