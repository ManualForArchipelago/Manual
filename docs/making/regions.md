# Regions

Regions are a powerful and simple way to organize your game logic and make it easier to understand and edit. In essence, regions allow you to take large groups of locations that have something in common and make them share the same logic and requires.

```json
[
    "Overworld": {
        "starting": true,
        "connects_to": ["Lonely Island","Spooky Manor"]
    },
    "Lonely Island": {
        "connects_to": [],
        "requires": "|Ferry Ticket|"
    },
    "Spooky Manor": {
        "connects_to": ["Manor Basement"],
        "requires": "|Manor Key| OR |Wall Climb|"
    },
    "Manor Basement": {
        "connects_to": [],
        "requires": "|Basement Key| AND |Lantern|"
    }
]
```

## The basics

When you create a [location](./locations.md), you can optionally assign it to a region. When you do this, the location will inherit ALL logic from the region it is in. This means that access to that location is not _only_ determined by that location's requires, but it now _also_ obeys the requires of the region it is in, _as well as_ that region's connection requirements (see below). If you have a location that is set to require Item A, and that location is in region "Cool Region", and "Cool Region" is set to require Item B, __that location will now require both Item A AND Item B before it is considered accessible__.

_In locations.json:_

```json
    {
        "name": "My Location",
        "region": "Cool Region",
        "requires": "|Item A|"
    },
```

_In regions.json:_

```json
    "Cool Region": {
        "requires": "|Item B|"
    }
```

This allows you to really simplify the requires for your locations. If you have 50 different locations that all require at least Item B, then you can assign them all to Cool Region, _and you no longer have to write "Item B" in 50 different locations_!

You can learn more about how to write requires for both locations and regions in our [requires syntax guide](/docs/syntax/requires-for-locations-and-regions.md).

## Region connections

Once you've created some regions, it is now possible to chain them together in ways that allows them to be dependent on each other. You can use the `"connects_to"` and `"starting"` keys to establish a pathway to move from one region to another. When these paths are made, the regions are considered to be __not accessible unless it is a starting region or you have access to a region that connects to it__. (If no starting region is defined, then all regions are considered to be starting.)

Consider the following example we showed earlier:

```json
[
    "Overworld": {
        "starting": true,
        "connects_to": ["Lonely Island","Spooky Manor"]
    },
    "Lonely Island": {
        "connects_to": [],
        "requires": "|Ferry Ticket|"
    },
    "Spooky Manor": {
        "connects_to": ["Manor Basement"],
        "requires": "|Manor Key| OR |Wall Climb|"
    },
    "Manor Basement": {
        "connects_to": [],
        "requires": "|Basement Key| AND |Lantern|"
    }
]
```

These regions represent the major areas of an adventure game we just made up. Our hero starts off in the overworld, and then can go to two other major areas of the map -- either the island, or the manor -- depending on whether they can get a ferry ride to the island, or can break into the manor somehow (in this case, either with the key to the house, or by climbing up the side and into the chimney). We see these connections written in the `"connects_to"` line of the Overworld region.

Observe that the Overworld does _not_ connect to Manor Basement, but Spooky Manor does. There's no way in this game to go straight from the Overworld to the Basement _without_ going through the rest of the manor first. This means that you require the items necessary to get into the manor _and_ the items to get into the basement before you can access any locations in the basement.

Please note that `connects_to` connections are _one-directional_ when defined, because it is implied that you can travel backwards across a connection that you already used. If you had some other way to access the Manor Basement without going through Spooky Manor, it would NOT necessarily give you access to the Spooky Manor as well, unless you specifically define it in Manor Basement's `connects_to`.
