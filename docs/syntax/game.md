# Game (game.json) Syntax

## Starting Items
You can specify items that the player should start with using the `starting_items` key. This example demonstrates and shows some common properties, and I will explain them one by one:
```
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
}
```

There are five conditions here. Let's look at them one by one:
```
        {
            "items": ["Ryu", "Akuma"]
        },
```

There's no random: argument here - this is a straight up list, not a raffle. If you list "Items": ["X", "Y", "Z"] without an extra argument, the player starts with all of them.
```
        {
            "item_categories": ["Left Side"],
            "random": 1
        },
```

Here, it's shown "item_categories": is a valid argument as well. More importantly, "random": 1 - we're adding 1 random item from the category. If that wasn't there, this would add the entire category into the starting inventory.
```
        {
            "items": ["Wolverine", "Storm", "Phoenix"],
            "random": 1
        },
```

Back to individual items, now with "random": 1 as well. This will add 1 of those items, randomly. If you had "random": 2, it would add 2 instead, and so on. So we get Wolverine, OR Storm, OR Phoenix.
```
        {
            "item_categories": ["Trash"]
        },
```

This works like the first one, except with categories instead of items. There's no "random": X argument, so you're getting every single item in the Trash category.
```
        {
            "random": 3
        }
```

Lastly, this has a "random": X argument, but no set to pull it from. This will add any 3 random items to the start inventory.

So, in total, we're starting with:
- Ryu and Akuma
- 1 random item from the "Left Side" category
- 1 of ["Wolverine", "Storm", "Phoenix"]
- Every item in the "Trash" category
- 3 Random items

for a generic format of:
```
        {
            "items"/"item_categories": ["List"],
            "random": X
        },
```

As observed. if there is no "random": X it'll add every item it can find, and if there are no item sets specified, it will pick from every item in the world.

### Conditional Starting items

Sometimes you want to make a more complex set of starting items.  Let's take a game where not every character can equip every weapon:

```json
{
  "starting_items": [
    {
        "items": ["Cadence", "Link", "Zelda", "Yves", "Skull Kid"],
        "random": 1
    },
    {
        "if_previous_item": "Zelda",
        "items": ["Broadsword", "Spear", "Flail", "Dagger"],
        "random": 1
    },
    {
        "if_previous_item": "Cadence",
        "items": ["Broadsword", "Spear", "Flail", "Dagger", "Shovel"],
        "random": 1
    },
    {
        "if_previous_item": "Link",
        "items": ["Broadsword", "Spear", "Flail", "Short Sword"],
        "random": 1
    },
    {
        "if_previous_item": "Skull Kid",
        "items": ["Deku Mask", "Goron Mask", "Darknut Mask", "Skull Mask", "Zora Mask"],
        "random": 1
    }
  ]
}
```

This is a slightly more complicated example.

Firstly, We start by giving the player a random character.  Then, depending on the result of that random choice, we give a starting weapon that they can equip.

```json
    {
        "items": ["Cadence", "Link", "Zelda", "Yves", "Skull Kid"],
        "random": 1
    },
```

Then if the random character was Zelda, we give her a random weapon she can equip.
```json
    {
        "if_previous_item": "Zelda",
        "items": ["Broadsword", "Spear", "Flail", "Dagger"],
        "random": 1
    },
```
Note:  At this point, the value of the previous item is either a character other than Zelda, or it's a weapon.

We repeat this for Cadence and Link, each of whom have slight variations of the same human weapons.

Skull Kid uses masks instead of weapons, so they get an entirely different selection for their loadout

```json
    {
        "if_previous_item": "Skull Kid",
        "items": ["Deku Mask", "Goron Mask", "Darknut Mask", "Skull Mask", "Zora Mask"],
        "random": 1
    }
```

And finally, Yves has no hands, so they don't get a followup starting item :stuck_out_tongue:

Our end result is that we will start with one of the following:
* A human character and a weapon they can use
* Skull kid and a Mask
* Yves (who has nothing)
