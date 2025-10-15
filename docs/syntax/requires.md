# Requires for Locations and Regions

_Let's start with the bad:_

If you don't put requires on your locations and/or regions, every location in your world will be in sphere 0. As in, any multiworld you play in will expect you to complete your entire world as soon as the multi starts.

So it's really important to have requires! But what are they?

Location/region requires tell the world what the logic is for accessing that location or region. Example: If you're playing Link to the Past and you have a region for Thieves Town, one of the dungeons in the Dark World. Your requires for that region would say that it requires Moon Pearl (for navigating the Dark World in human form) and either Hammer + Power Glove or just Titan's Mitt (for getting to the Dark World at all). Until you get the bare minimum of those items, that location will not be in logic, so the multi will not expect you to do that location yet.

Okay, so we know what requires are. Let's talk about the different ways you can write out those requirements!

## Boolean Logic (AND/OR)

**Boolean logic is the default way to write requires in Manual.** It's called "boolean logic" because you're writing your logic much like you'd describe it normally: with a series of AND/OR combos.

For example, from the example above about Link to the Past and Thieves Town in the Dark World, let's assume that the first chest location in the dungeon has no additional requirements. So, we'd describe our logic for that first chest location as being "Moon Pearl and (either (Hammer and Power Glove) or Titan's Mitt)", same as the region itself. In Manual's boolean logic syntax, that would be:

```json
{
    "name": "First chest in Thieves Town",
    "requires": "|Moon Pearl| and ((|Hammer| and |Power Glove|) or |Titan's Mitt|)"
}
```

**You use `|pipes|` around item names and `(parentheses)` around your layers of nesting, if needed.**

- Pipes tell Manual where to look for entire item names.
- Parentheses tell Manual exactly how you're grouping your logic, since there's a difference between "Hammer and Power Glove or Titan's Mitt" and "(Hammer and Power Glove) or Titan's Mitt".
  - The former essentially evaluates to "Hammer and either Power Glove or Titan's Mitt", while the latter is very explicit about what the logic should be and evaluates correctly.
  - There's no theoretical limit to how many parentheses you can use, but try to not get past the practical limit of how many sets of parentheses you can reliably keep track of.

### Additional Examples of Boolean Logic

Boss 1 Requires Ladder and Gloves, OR Sword and Shield, OR Bow and Quiver and Arrow (separate items): a simple case of various successful item sets. It's a few sets of ANDs separated by ORs.

```json
{
    "name": "Boss 1",
    "requires": "(|Ladder| and |Gloves|) or (|Sword| and |Shield|) or (|Bow| and |Quiver| and |Arrow|)"
}
```

Boss 2 simply requires one heart, a way to strike it (Sword, Spear or Club) and a way to dodge it (Double Jump, Dash or Slide): we're looking at different sets, and picking one item from which. It's many ORs inside a big set of ANDs.

```json
{
    "name": "Boss 2",
    "requires": "|Heart| and (|Sword| or |Spear| or |Club|) and (|Double Jump| or |Dash| or |Slide|)"
}
```

Now, say the final boss is a big dragon with a glaring weakness to Blizzard. However, if you don't have blizzard, you will need a spear for its reach and a way to dodge it, which is one of the three mobility from before. This is an OR (the mobility), inside an AND (Spear and Mobility), inside an OR (Blizzard it or fight it legitimately). Layered logic is as such:

```json
{
    "name": "Final Boss",
    "requires": "|Blizzard| or (|Spear| and (|Double Jump| or |Dash| or |Slide|))",
    "victory": true
}
```

## Item Counts

As demonstrated in the [Making Items: Count](making/items.md#count) docs, you can configure an item to have more than one copy of that item in the world's item pool. Sometimes, you want to use multiple copies of an item as a requirement for accessing a location or region, and Manual supports this as well.

The way to do this is a short suffix added to the end of any required item name separated by a colon, like this: `|Coin:25|`.

- That will tell Manual that the location/region requires 25 of that Coin item.

Now that we know how to require multiple of an item, we can revise our Boss 2 example from above to make the boss a little easier to handle in-logic:

> Boss 2 simply requires **FIVE hearts**, a way to strike it (Sword, Spear or Club) and a way to dodge it (Double Jump, Dash or Slide): we're looking at different sets, and picking one item from which. It's many ORs inside a big set of ANDs.
>
> ```json
>{
>    "name": "Boss 2",
>    "requires": "|Heart:5| and (|Sword| or |Spear| or |Club|) and (|Double Jump| or |Dash| or |Slide|)"
>}
> ```

In addition to specific item counts, you can also specify a broad relative amount like "all of this item" or "half of this item", or even percentages of that item versus the total in the pool. We'll demonstrate those briefly below as well.

- `|Coin:ALL|` will make a location/region require every `Coin` item in the world's item pool before being accessible. So, if you have 50 Coins in the pool, it will require all 50. (The "ALL" is not case sensitive, so it can be lowercase too.)
- `|Coin:HALF|` will make a location/region require half of the `Coin` items in the world's item pool before being accessible. So, if you have 50 Coins in the pool, it will require 25. (The "HALF" is not case sensitive, so it can be lowercase too.)
- `|Coin:90%|` will make a location/region require 90% of the `Coin` items in the world's item pool before being accessible. So, if you have 50 Coins in the pool, it will require 45. (Supports percentages between 0 and 100.)

## Requiring Categories

As demonstrated in the [Making Items: Category](making/items.md#categories) docs, you can configure an item to belong to a category, potentially with other related items. Sometimes, you want to use a category of items as a requirement for accessing a location or region, and Manual supports this as well.

The way to do this is a short @ ("at symbol") prefix added to the beginning of any required item name, like this: `|@Coins|`

- That will tell Manual that the location/region requires 1 item from the "Coins" category.

Additionally, you can use counts as described above for required categories, just as you would use them for required item names. Let's see the demonstrated counts from above in category form:

- `|@Coins:ALL|` will make a location/region require every item in the `Coins` category before being accessible. So, if you have 50 items in the `Coins` category, it will require all 50. (The "ALL" is not case sensitive, so it can be lowercase too.)
- `|@Coins:HALF|` will make a location/region require half of the items in the `Coins` category before being accessible. So, if you have 50 items in the `Coins` category, it will require any 25 of them. (The "HALF" is not case sensitive, so it can be lowercase too.)
- `|@Coins:90%|` will make a location/region require 90% of the items in the `Coins` category before being accessible. So, if you have 50 items in the `Coins` category, it will require any 45 of them. (Supports percentages between 0 and 100.)

## Requirement Functions

Requirement functions are functions that you write in the Rules hook file and can use in requires in locations/regions. We do provide a couple of default ones as examples, but only a couple of generic ones for very specific cases (more on that below \*). In most cases, you'll be working with hooks to take advantage of requirement functions.

You'd typically use requirement functions if you have requirements that are too cumbersome to type out by hand, have requirements that rely on some dynamic piece of information, or have requirements that don't fit into the templating syntax that Manual provides for requirements.

The way to do this is using curly braces around the function name that you want to call, like this: `{myFunction()}`

- Note the lack of pipes (`|`). Functions are processed entirely differently than items/categories used as requirements.
- Doing this will tell Manual that the function will either return a requires string to be processed, or will return true/false based on whether this requirement was met.

Requirement functions can have no function arguments, or have any number of function arguments separated by commas.

- Example with no function arguments: https://github.com/ManualForArchipelago/Manual/blob/main/src/hooks/Rules.py#L8-L15.
- Example with one argument, add str arguments to the end of the function for more: https://github.com/ManualForArchipelago/Manual/blob/main/src/hooks/Rules.py#L17-L24

Additionally, those functions can themselves return a dynamically-created requires string, which would then be processed normally in the spot where the function call was.

- Example of a returned requires string: https://github.com/ManualForArchipelago/Manual/blob/main/src/hooks/Rules.py#L26-L29

## Bundled functions

In addition to writing your own Requirement Functions, Manual comes with some helpful functions built in:

### `ItemValue(ValueName:Count)`

Checks if you've collected the specificed value of a value-based item.

For Example, `{ItemValue(Coins:12)}` will check if the player has collect at least 12 coins worth of items

### `OptOne(ItemName)`

Requires an item only if that item exists.  Useful if an item might have been disabled by a yaml option.

### `OptAll(ItemName)`

Takes an entire requires string, and applies the above check to each item inside it.

For example, `requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"` will be transformed into `"|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|"`

### `YamlEnabled(option_name)` and `YamlDisabled(option_name)`

These allow you to check yaml options within your logic.

You might use this to allow glitches

```json
{
    "name": "Item on Cliff",
    "requires": "|Double Jump| or {YamlEnabled(allow_hard_glitches)}"
}
```

Or make key items optional

```json
{
    "name": "Hidden Item in Pokemon",
    "requires": "|Itemfinder| or {YamlDisabled(require_itemfinder)}"
}
```

You can even combine the two in complex ways

```json
{
    "name": "This is probably a region",
    "requires": "({YamlEnabled(easy_mode)} and |Gravity|) or ({YamlDisabled(easy_mode)} and |Jump| and |Blizzard| and |Water|)"
}
```

### `YamlCompare(option_name comparator_symbol value)`

Verify that the result of the option called _option_name_'s value compared using the _comparator_symbol_ with the requested _value_

The comparator symbol can be any of the following: `== or =, !=, >=, <=, <, >`

The value can be of any type that your option supports

- Range: integer aka number
- Range with values aka NamedRange: integer or one of the value name in "values"
- Choice: either numerical or string representation of a value in the option's "values"
- Choice with allow_custom_value: either numerical or string representation of a value in the option's "values" or a custom string
- Toggle: a boolean value represented by any of the following not case sensitive:
  - True: "true", "on", 1
  - False: "false", "off", 0

The folowing example would check that the player.yaml value of the range option Example_Range is bigger than 5 or that the `Item A` item is present:

```json
{
    "name": "Example Region",
    "requires": "|Item A| or {YamlCompare(Example_Range > 5)}"
}
```
