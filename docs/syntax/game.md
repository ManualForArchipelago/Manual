# Game - game.json
Your game.json contains all of the top-level game-specific details about your world. 

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the game.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.game.schema.json).

## The game.json structure
The properties for this file are broken down into these headings below:
- [Defining your game name](#defining-your-game-name)
  - `game`
  - `creator`
- [The name of a default filler item](#the-name-of-a-default-filler-item)
  - `filler_item_name`
- [Death Link](#death-link)
  - `death_link`
- [Starting Index for items and locations](#starting-index-for-items-and-locations)
  - `starting_index`
- [Starting Items](#starting-items)
  - `starting_items`

---

### Defining your game name
Your game.json needs to at least contain the identifying information for your Manual game, so it can be differentiated from other games. This includes the "game" property (which details what video game / board game / etc. that you're making this Manual for) and the "creator" property (which helps identify a Manual you created for a game versus one that someone else did).

Here's an example with the minimum required info:

```json
{
    "game": "Snolf",
    "creator": "YourNameHere"
}
```

---

### The name of a default filler item
Your game.json can contain the name of a default filler item, which Manual will create when it needs more items to place at your unfilled locations. If you omit this, a generic "Filler" item name is used.

Here's an example of defining your filler item name along with the above info for a game:

```json
{
    "game": "Snolf",
    "creator": "YourNameHere",
    "filler_item_name": "Gold Rings"
}
```

---

### Death Link
By default, deathlink is not enabled in Manual apworlds, but a world creator can enable using the option by adding a `death_link` property to this file.

Here's an example of setting deathlink along with the above required info for a game:

```json
{
    "game": "Snolf",
    "creator": "YourNameHere",
    "death_link": true
}
```

Once added, this allows you to use the normal `death_link` option in your YAML. Additionally, once this YAML option is enabled, a new fancy button will show up in the client for sending deathlinks.

**NOTE:** If you turn this on, make sure you have a clear (and documented) understanding of what a death is, when players should send one, and what it means to receive it.

---

### Starting Index for items and locations
By default, all of the ids for your items and locations start at 1 before counting up for each item/location. If you want to customize this starting number, you can use the `starting_index` property.

Here's an example of defining your starting index along with the above required info for a game:

```json
{
    "game": "Snolf",
    "creator": "YourNameHere",
    "starting_index": 67
}
```

---

### Starting Items
You can specify items that the player should start with using the `starting_items` key. This example demonstrates and shows some common properties, and I will explain them one by one:

```json
{
    "game": "20230611",
    "creator": "Unstable",

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

There's no random: argument here - this is a straight up list, not a raffle. If you list "Items": ["X", "Y", "Z"] without an extra argument, the player starts with all of them.

```json
        {
            "item_categories": ["Left Side"],
            "random": 1
        },
```

Here, it's shown "item_categories": is a valid argument as well. More importantly, "random": 1 - we're adding 1 random item from the category. If that wasn't there, this would add the entire category into the starting inventory.

```json
        {
            "items": ["Wolverine", "Storm", "Phoenix"],
            "random": 1
        },
```

Back to individual items, now with "random": 1 as well. This will add 1 of those items, randomly. If you had "random": 2, it would add 2 instead, and so on. So we get Wolverine, OR Storm, OR Phoenix.

```json
        {
            "item_categories": ["Trash"]
        },
```

This works like the first one, except with categories instead of items. There's no "random": X argument, so you're getting every single item in the Trash category.

```json
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

```json
        {
            "items"/"item_categories": ["List"],
            "random": X
        },
```

As observed. if there is no "random": X it'll add every item it can find, and if there are no item sets specified, it will pick from every item in the world.

#### Conditional Starting items

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

