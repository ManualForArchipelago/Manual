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
