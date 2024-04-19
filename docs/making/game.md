# game.json

Game.json contains the most fundamental details about your Manual Game, the details about the game itself.

At its most basic, it needs the name of the game, and name of the creator (you).
It also contains the name of the auto-generated filler item, and details about Starting Inventory (see below for more details)

```json
{
    "game": "Snolf",
    "creator": "YourNameHere",
    "filler_item_name": "Gold Rings"
}
```

## Starting Inventory

The [example world](/src/data/) covers every use of it, so here's a breakdown of each entry:
```json
{
    "game": "UltimateMarvelVsCapcom3",
    "player": "ManualTeam",

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
```json
        {
            "items": ["Ryu", "Akuma"]
        },
```
There's no `random:` argument here - this is a straight up list, not a raffle. If you list `"Items": ["X", "Y", "Z"]` without an extra argument, the player starts with __all of them__.

```json
        {
            "item_categories": ["Left Side"],
            "random": 1
        },
```
Here, it's shown `"item_categories"`: is a valid argument as well. More importantly, `"random": 1` - we're adding __1 random item from the category__. If that wasn't there, this would _add the entire category into the starting inventory_.

```json
        {
            "items": ["Wolverine", "Storm", "Phoenix"],
            "random": 1
        },
```
Back to individual items, now with `"random": 1` as well. This will add 1 of those items, randomly. If you had `"random": 2`, it would add 2 instead, and so on. So we get Wolverine, OR Storm, OR Phoenix.

```json
        {
            "item_categories": ["Trash"]
        },
```
This works like the first one, except with categories instead of items. There's no `"random": X` argument, so you're getting __every single item in the Trash category__.

```json

        {
            "random": 3
        }
```
Lastly, this gives you three completely random items.


Next: Add your [items](/docs/making/items.md)
