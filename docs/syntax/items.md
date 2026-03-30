# Items - items.json
Your items.json contains the details about all of the items in your world. 

This file contains multiple objects, so you'll want to have a `[]` surrounding the `{}` objects to be valid JSON. If your items.json has a "$schema" property at the top, use the `[]` in the "data" property instead.

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the items.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.items.schema.json).

## The items.json structure
The properties for this file are broken down into these headings below:
- [Naming and categorizing](#naming-and-categorizing)
  - `name`
  - `category`
- [Item classification](#item-classification)
  - `filler` / `trap` / `useful` / `progression` / `progression_skip_balancing`
  - `classification_count`
- [Total number of items](#total-number-of-items)
  - `count`
- [Early Items](#early-items)
  - `early`
- [Local Items](#local-items)
  - `local`
- [Custom sorting of items in the Manual client](#custom-sorting-of-items-in-the-manual-client)
  - `sort-key`
- [Assigning custom point values](#assigning-custom-point-values)
  - `value`

---

### Naming and categorizing
The minimum information you need to provide for an item is its name. Here's an example of that simple item definition:

```json
{
    "name": "Button Activation"
}
```

(A name cannot contain the characters `:` or `|`, and it's not recommended to use non-english characters not supported by Archipelago's default font.)

If you then want to categorize that item, you can assign it one or more "category" names to be assigned to. See the [Categories for Items and Locations](categories-for-various-objects.md) page for more information.

---

### Item classification
Items that you define are filler items by default. For your Manual world's logic to work correctly, any items that are listed in logical requirements must be progression items, not filler items. (For more information on item classifications in AP, visit [their documentation on world items here](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items).)

#### Setting a different classification
The valid classifications are `"trap"`, `"filler"`, `"useful"`, `"progression"`, `"progression_skip_balancing"`. They all default to `false` and, in the absence of a classification, Manual will create them as filler.

You will typically want to set only one or two of these, using similar lines to the example below:

```json
{
    "name": "Button Activation",
    "filler": true,
    "trap": true,
    "useful": true,
    "progression": true,
    "progression_skip_balancing": true
}
```

#### Setting a variety of classifications for the same item
Sometimes, you don't just want all copies of an item to be a certain classification. Maybe you want a mix of a dozen progression items, 5 progression AND useful items, and 2 filler items. Well, you can do that using the `classification_count` property on an item.

Here's an example demonstrating the mix described above:

```json
{
    "name": "Button Activation",
    "classification_count": {
        "progression": 12,
        "useful + progression": 5,
        "filler": 2
    }
}
```

**NOTE:** When using `classification_count` on an item, the `count` property (detailed below) and any other classification properties (mentioned previously, like `trap`, `useful`, etc.) have no effect. `classification_count` overrides all of them.

---

### Total number of items
Your world is likely to have multiple copies of non-unique items. To accommodate that, you can specify a `count` property to tell Manual how many of that item to create.

Here's an example:

```json
    {
        "name": "Comically Large Oversized Novelty Key",
        "count": 7
    }
```

---

### Early Items
Sometimes an item is very important, and you really don't want to leave it up to progression balancing. In that case, use the `early` property:

```json
    {
        "name": "Oak's Parcel",
        "progression": true,
        "early": true
    }
```

This ensures the item is placed somewhere in Sphere 1.

---

### Local Items
Do you have a lot of items you don't want to flood the multiworld with? Use the `local` property to keep them in your own world:

```json
    {
        "name": "Tiny Key Fragment",
        "count": 800,
        "local": true
    }
```

I'm sure glad these are contained within our own world, and other people aren't complaining that they're picking up nothing but fragments of tiny keys.

---

### Custom sorting of items in the Manual client
By default, item names are sorted by natural sorting (alphabetical, but numbers sort numerical) or to the preference set in your Manual client. If you want to sort items in a more custom way, you can assign your items a `sort-key`, which is then sorted according to the value you provide there.

Here's an example where the second item would be sorted above the first item in the Manual client:

```json
{
    "name": "Button Activation",
    "sort-key": "row-1-1"
},
{
    "name": "Lever Activation",
    "sort-key": "row-0-8"
}
```

---

### Assigning custom point values
In some cases, you might have items that should be treated as part of a larger goal, like an accumulated set of points/currency or a weight/power level of upgrades. In cases like that, you can use the `value` property to create an item value for that item. When each copy of that item is received, Manual will also keep track of the total accumulated value(s) set by that property.

Here's an example that sets a couple different values for an item:
```json
    {
        "name": "Large Bag of Money",
        "value": {
            "coins": 100,
            "bags": 3
        }
    }
```

These values can also be used in logical requirements, which is covered in the shared section about requires.

