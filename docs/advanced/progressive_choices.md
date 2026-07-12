# Progressive Choice options

Have you ever looked at your yaml and thought "That's five yes or no toggles that would be much easier to use if they were a single multiple-choice option"?

This is how you'd do that:

Our example is a manual that wants several tiers of fishing

## locations.json

First thing we're going to do is define some fishing checks.  We're giving each of them the Fish category, and we'll also give the harder fish a second category for their difficulty.

```json
[
    {"name": "Salmon", "category": ["Fish", "Common Fish"]},
    {"name": "Rainbow Trout", "category": ["Fish", "Rare Fish"]},
    {"name": "The Ruby Dragon", "category": ["Fish", "Legendary Fish"]},
]
```

## categories.json
(Optional):  The Rare/Legendary fish categories might be too noisy, and we only really need them for implementing the yaml option.  You can hide them if you want.

```json
{
    "Common Fish": { "hidden": true},
    "Rare Fish": { "hidden": true},
    "Legendary Fish": { "hidden": true},
}
```

## options.json

Next, we need to define our yaml option.

```json
{
    "user": {
        "fishsanity":{
            "type": "Choice",
            "description": [
                "Include fish-related checks"
            ],
            "values": {
                "disabled": 0,
                "common_fish": 1,
                "rare_fish": 2,
                "legendary_fish": 3
             },
            "default": 0
        }
    }
}
```

This is pretty simple.  We make a Choice, and make a value for each option.  Make sure they are in the order you want them to turn on.

## hooks/Helpers.py

Finally, we need a hook that toggles the categories on/off.

```py
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    from ..Helpers import get_option_value

    if category_name == "Common Fish":
        # If fishsanity == 0, all fish are disabled
        return get_option_value(multiworld, player, "fishsanity") >= 1
    if category_name == "Rare Fish":
        # Rare Fish needs either rare (2) or legendary (3)
        return get_option_value(multiworld, player, "fishsanity") >= 2
    if category_name == "Legendary Fish":
        return get_option_value(multiworld, player, "fishsanity") >= 3
    return None
```

A simple numerical comparison between the value of the yaml option lets us progressively turn categories on or off.
