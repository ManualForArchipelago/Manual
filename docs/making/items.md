# Items

Items.json contains the details of all your items.

Here's a simple example:

```json
[
    {
        "name": "Button Activation",
        "progression": true
    },
    {
        "name": "Feeling of Satisfaction",
        "useful": true
    },
    {
        "name": "Hey wait, isn't this just Clique?",
        "filler": true
    }
]
```

## The basics

An item contains at least it's name and a classification.

A name cannot contain the characters `:` or `|`, and it's not recommended to use non-english characters not supported by Archipelago's default font.

The valid classifications are `"trap"`, `"filler"`, `"useful"`, `"progression"`, `"progression_skip_balancing"`.  See [here](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items) for details on what each means.

## Categories

Having all your items in the "(No Category)" section is messy and hard to read.  We can organize them by adding categories.

```json
    {
        "name": "Sword",
        "progression": true,
        "category": ["Weapons"]
    }
```

An item can have as few or as many of these as you want, and they can have other uses in addition to organizing the client UI [(read more)](./categories.md)

## Count

Most games have non-unique items, yours is probably no different.

```json
    {
        "name": "Comically Large Oversized Novelty Key",
        "useful": true,
        "category": ["Keys"],
        "count": 7
    }
```

Our game has seven oversized novelty keys.  Not really much more to explain here.

## Classification Count

This special property let you manually override the counts of an item per classification.

With it you can specify that there should be some `progression` copies of an item while you have `useful` copies too

It can also be used to create multi classification items using a plus (`+`) sign eg. `"progression + useful"`

### Important to note that using `classification_count` in an item make Manual ignore the value of the `count` property and/or any classification properties in said item

*AKA properties like `"count"`, `"useful"`, `"progression"`, `"progression_skip_balancing"` or `"trap"` will be ignored in favour of classification_count*

```json
    {
        "name": "Jill",
        "category": [
            "Characters",
            "Left Side"
        ],
        "classification_count": {
            "useful + progression": 1,
            "useful": 1
        },
        "_comment": "In this example a copy of the 'Jill' item will be created that is useful & progression and another will be created just useful"
    },
```

## Early items

Sometimes an item is very important, and you really don't want to leave it up to progression balancing.

```json
    {
        "name": "Oak's Parcel",
        "progression": true,
        "early": true
    }
```

This ensures the item is placed somewhere in Sphere 1.

## Local Items

Do you have a lot of items you don't want to flood the multiworld with?  Good News!

```json
    {
        "name": "Tiny Key Fragment",
        "progression": true,
        "count": 800,
        "local": true
    }
```

I'm sure glad these are contained within our own world, and other people aren't complaining that they're picking up nothing but fragments of tiny keys.

Next: [Locations](./locations.md)
