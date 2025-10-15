# Locations (locations.json) Syntax

## Victory Location
Victory is a singular argument, like "count", but in a location. If you had a Final Door requiring Key 1, Key 2 and Key 3 as your Victory location, you could write it as such:
```
{ 
    "name": "Final Door", 
    "requires": "|Key 1| and |Key 2| and |Key 3|",
    "victory": true 
}
```

You can combine a Victory location with any other logic, but your Victory locations cannot be assigned items.

You can also have multiple Victory locations, which a player can choose from using the built-in `goal` YAML option.

## Pre-Placing Items
If you want to pre-place items (a.k.a. force locations to have a specific item, or an item from a specific set), you have two resources for this: place_item and place_item_category

The simplest example is a one-to-one situation. Say a boss fight, "Boss A", gives an in-game key, "Key X". You want "Key X" as an item to use for your logic, but you want to keep it tied to "Boss A".
```
{   
    "name": "Kill Boss A", 
    "requires": "|The Items That Kill Boss A|",
    "place_item": ["Key X"] 
}
```

This will ensure that the "Kill Boss A" location will always award your "Key X" item.

If you had multiple keys you wanted as possible rewards, you could list them all, separated by commas:
```    
{   
    "name": "Kill Boss A", 
    "requires": "|The Items That Kill Boss A|",
    "place_item": ["Key X", "Key Y", "Key Z"] 
}
```

This doesn't give all three keys: It guarantees one random drop, selected between those 3 keys.

If you wanted it to give any key from a category you already have, you would use place_item_category instead:
```    
{   
    "name": "Kill Boss A", 
    "requires": "|The Items That Kill Boss A|",
    "place_item_category": ["Boss Keys"] 
}
```

The location will award any item in the "Boss Keys" category. Like place_item, you can list multiple categories - it will pick a random category, and place a random item from that category.

The following will work:
```
{   "name": "Area A",
    "place_item_category": ["Keys and Boots"] 
},
{   "name": "Area B",
    "place_item_category": ["Keys and Boots"] 
},
{   "name": "Area C",
    "place_item_category": ["Keys and Boots"] 
},
{   "name": "Area D",
    "place_item_category": ["Keys and Boots"] 
}
```

This will distribute your 2 keys and 2 boots randomly between the locations.
  
However, this will fail:
```
{   "name": "Area A",
       "place_item_category": ["Keys", "Boots"] 
},
{   "name": "Area B",
       "place_item_category": ["Keys", "Boots"] 
},
{   "name": "Area C",
       "place_item_category": ["Keys", "Boots"] 
},
{   "name": "Area D",
"place_item_category": ["Keys", "Boots"] 
}
```

The reason for this is that every location will pick a category randomly. If A, B and C all pick "Keys", for example, you'll be trying to divide 2 keys among 3 locations. One will be empty, and will error.

This is only really a risk if you are working with small item pools, or item pools of comparable size to the locations they're placed in: If you have 60 pieces of equipment and want your 12 bosses to each give a random piece guaranteed, you're extremely unlikely to run into any issues doing it that way.

