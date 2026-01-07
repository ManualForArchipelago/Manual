# Categories for Items, Locations, and Events

The primary uses of categories are to:

1. Group together items/locations/events in the Manual client
2. [Use groups of items as logical requirements for locations or events](docs/syntax/requires.md#requiring-categories)
3. [Force locations to give an item from a specific category when checked](docs/syntax/locations.md#pre-placing-items)
4. [Create easy YAML options using the categories.json](docs/syntax/categories.md#simple-toggling-of-items-and-locations)

Categories are a property like "victory" and "count", except it requires square brackets `[]` because it can contain multiple items. Their syntax is the same for items, locations and events.

Here are examples of assigning categories to an item, a location, and an event (respectively):

```
{ 
    "name": "Coins",
    "category": ["Currencies"],
    "count": 25, 
    "progression": true
}
```

```
{ 
    "name": "Kill First Boss", 
    "category": ["First Dungeon", "Boss Fight"], 
    "requires": "|Sword|"
}
```

```
{ 
    "name": "First Boss Defeated", 
    "category": ["First Dungeon", "Boss Fight"], 
    "requires": "|Sword|"
}
```

