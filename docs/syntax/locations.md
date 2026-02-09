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
- [Manipulating what item can/will be in this location](#manipulating-what-item-canwill-be-in-this-location)
  - [`place_item` / `place_item_category`](#pre-placing-items)
  - `dont_place_item` / `dont_place_item_category`
    - [when `place_item` / `place_item_category` present](#removing-items-from-those-pre-placed)
    - [when `place_item` / `place_item_category` not present](#forbiding-items-from-a-location)
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

```json
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

```json
{ 
    "name": "Final Door", 
    "region": "Last Dungeon"
}
```

---

### Logical requirements
Logical requirements ensure that your location is not put into logic before it should be reachable. See the [Requires](requires.md) page for more information.

---

### Manipulating what item can/will be in this location
#### Pre-placing items
If you want to pre-place items (a.k.a. force locations to have a specific item, or an item from a specific set), you have two resources for this: `place_item` and `place_item_category`

The simplest example is a one-to-one situation. Say a boss fight, "Boss A", gives an in-game key, "Key X". You want "Key X" as an item to use for your logic, but you want to keep it tied to "Boss A".

```json
{   
    "name": "Kill Boss A", 
    "place_item": ["Key X"] 
}
```

This will ensure that the "Kill Boss A" location will always award your "Key X" item.

If you had multiple keys you wanted as possible rewards, you could list them all, separated by commas:

```json
{   
    "name": "Kill Boss A", 
    "place_item": ["Key X", "Key Y", "Key Z"] 
}
```

This doesn't give all three keys: It guarantees one random drop, selected between those 3 keys.

If you wanted it to give any key from a category you already have, you would use `place_item_category` instead:

```json
{   
    "name": "Kill Boss A", 
    "place_item_category": ["Boss Keys"] 
}
```

The location will award any item in the "Boss Keys" category. Like `place_item`, you can list multiple categories - it will place a random item from all of those category.

The following will work:

```json
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
},
```

This will distribute your 2 keys and 2 boots randomly between the locations.

`place_item` and `place_item_category` can be combined together if you want to specify some specific item(s) that could be picked on top of those from the category(ies)

```json
{   
    "name": "Area E",
    "place_item": ["Sword"],
    "place_item_category": ["Keys", "Boots"]
},
```

In this example the item that could be placed there is either the "Sword" or any items from either category "Keys" or "Boots"

If you want to exclude some item(s) from those possible picked you can use [`dont_place_item` or `dont_place_item_category`](#removing-items-from-those-pre-placed) and those will be explained just below.

#### Removing items from those pre-placed

`dont_place_item` or `dont_place_item_category` work mostly like [`place_item` or `place_item_category`](#pre-placing-items) but instead of deciding which item will be placed in a location, It stop the specified item/item_category from being placed in this location.  
Depending on if either `place_item` or `place_item_category` are present the logic behind is slightly different but the result is the same either way, the specified item/item_category wont be placed there.

When `place_item` or `place_item_category` are present items that could be randomly picked will be filtered by those in `dont_place_item/_category`.

```json
{   
    "name": "Area F",
    "place_item": ["Sword"],
    "place_item_category": ["Keys", "Boots"],
    "dont_place_item": ["Key Z"]
},
```

In this example the item that will be placed in the "Area F" location will either be the "Sword", an item from the "Boots" category, an item from the "Keys" category but not the "Key Z".

Like place_item_category, dont_place_item_category can be used to filter out an entire category worth of item.

```json
{
    "name": "Heroes Recruit 1",
    "place_item_category": ["Heroes"],
    "dont_place_item_category": ["Magic Users"]
},
```

This "Heroes Recruit 1" location will have an Hero but not any from the "Magic Users" category.

And finally,

#### Forbiding items from a location

AKA `dont_place_item` or `dont_place_item_category` but [`place_item` or `place_item_category`](#pre-placing-items) are not present.

When included in a location without pre-placement of items, the player's own copy of item(s) specified will be blocked from generating there.  
**Warning:** Usage of `dont_place_item` or `dont_place_item_category` can lead to some impossible logic if you forbid too many items and generation run out of things to place in a location so use carefully and sparingly.

(For the AP dev enjoyers reading this: Its done using the forbid_items_for_player function.)

```json
{
    "name": "Quest Rewards A",
    "dont_place_item": ["Death Trap"]
},
```

This "Quest Rewards A" location would let any item be placed there in generation **Except** the player's own "Death Trap".

Its usefull if you feel like the reward for the quest shouldn't be to die to your own trap.

```json
{
    "name": "Quest Rewards B",
    "dont_place_item_category": ["Trap"]
},
```

Same as above but any item from the Trap category.

```json
{
    "name": "Quest Rewards C",
    "dont_place_item_category": ["Trap"],
    "dont_place_item": ["Master Sword"]
},
```

Also like [`place_item` and `place_item_category`](#pre-placing-items) you can combine them together to forbid both the "Master Sword" and all the items from the "Trap" category.

---

### Pre-hinting this location
Sometimes, you may find yourself making locations where the player knows their contents in advance.  This is a thing APWorlds will commonly do for Shops.

This can be done by marking a location as prehinted:

```json
{
    "name": "Shop Item 1",
    "prehint": true
},
```

---

### Add hint text for useful info
If you want to show custom information in the "Entrance" portion of the Hints tab in the client, you can set the `hint_entrance` property.

Here's an example where you tell the player how to get to the "Area A" location:

```json
{   
    "name": "Area A",
    "hint_entrance": "Reachable via the West Bridge" 
},
```
