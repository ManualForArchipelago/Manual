# Locations - locations.json
Your locations.json contains the details about all of the locations in your world. 

This file contains multiple objects, so you'll want to have a `[]` surrounding the `{}` objects to be valid JSON. If your locations.json has a "$schema" property at the top, use the `[]` in the "data" property instead.

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the locations.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.locations.schema.json).

## The locations.json structure
The properties for this file are broken down into these headings below:
- [Naming and categorizing](#naming-and-categorizing)
  - `name`
  - `category`
- [Victory locations](#victory-locations)
  - `victory`
- [Assigning a region](#assigning-a-region)
  - `region`
- [Logical requirements](#logical-requirements)
  - `requires`
- [Pre-placing items](#pre-placing-items)
  - `place_item` / `place_item_category`
- [Pre-hinting this location](#pre-hinting-this-location)
  - `prehint`
- [Add hint text for useful info](#add-hint-text-for-useful-info)
  - `hint_entrance`

---

### Naming and categorizing
The minimum information you need to provide for a location is its name. Here's an example of that simple location definition:

```json
{
    "name": "Press the Button"
}
```

(It's not recommended to use non-english characters not supported by Archipelago's default font.)

If you then want to categorize that location, you can assign it one or more "category" names to be assigned to. See the [Categories for Items and Locations](categories-for-various-objects.md) page for more information.

---

### Victory locations
Victory locations are locations that cannot have an item but, when the location is checked, your world reaches its goal in AP. 

Your world can have any number of victory locations, but only one is active for each playthrough. Manual's built-in `goal` YAML option allows your players to choose which goal location is active for that playthrough.

Here's an example that sets a location as a victory location:

```
{ 
    "name": "Final Door", 
    "victory": true 
}
```

Note: Be sure to add requirements to your victory location to prevent it from being in logic too quickly. See the [Requires](requires.md) page for more information.

---

### Assigning a region
Regions can be helpful to either establish a world layout for your world, or to group together locations that share logical requirements. Each location can only be assigned to a single region. Once you've determined which region you'd like to assign to a location, you can set the `region` property to the name of the region.

Here's an example that assigns the "Last Dungeon" region to the "Final Door" location:

```
{ 
    "name": "Final Door", 
    "region": "Last Dungeon"
}
```

---

### Logical requirements
Logical requirements ensure that your location is not put into logic before it should be reachable. See the [Requires](requires.md) page for more information.

---

### Pre-placing items
If you want to pre-place items (a.k.a. force locations to have a specific item, or an item from a specific set), you have two resources for this: `place_item` and `place_item_category`

The simplest example is a one-to-one situation. Say a boss fight, "Boss A", gives an in-game key, "Key X". You want "Key X" as an item to use for your logic, but you want to keep it tied to "Boss A".
```
{   
    "name": "Kill Boss A", 
    "place_item": ["Key X"] 
}
```

This will ensure that the "Kill Boss A" location will always award your "Key X" item.

If you had multiple keys you wanted as possible rewards, you could list them all, separated by commas:
```    
{   
    "name": "Kill Boss A", 
    "place_item": ["Key X", "Key Y", "Key Z"] 
}
```

This doesn't give all three keys: It guarantees one random drop, selected between those 3 keys.

If you wanted it to give any key from a category you already have, you would use place_item_category instead:
```    
{   
    "name": "Kill Boss A", 
    "place_item_category": ["Boss Keys"] 
}
```

The location will award any item in the "Boss Keys" category. Like place_item, you can list multiple categories - it will pick a random category, and place a random item from that category.

The following will work:
```
{   
    "name": "Area A",
    "place_item_category": ["Keys and Boots"] 
},
{   
    "name": "Area B",
    "place_item_category": ["Keys and Boots"] 
},
{   
    "name": "Area C",
    "place_item_category": ["Keys and Boots"] 
},
{   
    "name": "Area D",
    "place_item_category": ["Keys and Boots"] 
}
```

This will distribute your 2 keys and 2 boots randomly between the locations.
  
However, this will fail:
```
{   
    "name": "Area A",
    "place_item_category": ["Keys", "Boots"] 
},
{   
    "name": "Area B",   
    "place_item_category": ["Keys", "Boots"] 
},
{   
    "name": "Area C",
    "place_item_category": ["Keys", "Boots"] 
},
{   
    "name": "Area D",
    "place_item_category": ["Keys", "Boots"] 
}
```

The reason for this is that every location will pick a category randomly. If A, B and C all pick "Keys", for example, you'll be trying to divide 2 keys among 3 locations. One will be empty, and will error.

This is only really a risk if you are working with small item pools, or item pools of comparable size to the locations they're placed in: If you have 60 pieces of equipment and want your 12 bosses to each give a random piece guaranteed, you're extremely unlikely to run into any issues doing it that way.

---

### Pre-hinting this location
Sometimes, you may find yourself making locations where the player knows their contents in advance.  This is a thing APWorlds will commonly do for Shops.

This can be done by marking a location as prehinted:

```
{
    "name": "Shop Item 1",
    "prehint": true
},
```

---

### Add hint text for useful info
If you want to show custom information in the "Entrance" portion of the Hints tab in the client, you can set the `hint_entrance` property. 

Here's an example where you tell the player how to get to the "Area A" location:

```
{   
    "name": "Area A",
    "hint_entrance": "Reachable via the West Bridge" 
},
```

