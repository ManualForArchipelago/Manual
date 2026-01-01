# Categories - categories.json
Your categories.json can contain additional details about categories used in your world. 

This file contains multiple objects but uses the object names as keys, so you don't need to have a `[]` surrounding everything like in the items/locations JSON files. Instead, you'd have a `{}` surrounding everything, like in the game JSON file.

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the categories.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.categories.schema.json).

## The categories.json structure
The properties for this file are broken down into these headings below:
- [Naming](#naming)
- [Hiding in the Manual client](#hiding-in-the-manual-client)
  - `hidden`
- [Simple toggling of items and locations](#simple-toggling-of-items-and-locations)
  - `yaml_option`

### Naming
The minimum information you need to provide for a category listing here is its name. Here's an example of that simple listing:

```json
"My Weapons": {

}
```

... but this would be pointless without any additional details' properties, so let's cover those next.

### Hiding in the Manual client
If you only want to use categories for logical requirements or other reasons, you might want those categories to not show in the client. You can use the `hidden` property to change whether a category is shown there or not.

Here's an example where you make the category hidden in the client:

```json
"My Weapons": {
    "hidden": true
}
```

### Simple toggling of items and locations
Sometimes, you want a bit of flexibility in terms of what items and locations are included for a playthrough. A simple no-code version of this can be accomplished using the `yaml_option` property for a category listing. When used, the option key that you provide there will be created as a true/false option for use in the YAML.

If the option is set to false, the items and locations that have this category will not be included in the multiworld. If you want them to be removed when the option is set to true instead, negate the option key that you set above by putting a `!` in front of it.

Here's an example of two categories ("Hard Mode" and "Second DLC") that have YAML options, where the first removes items/locations on false and the second does it on true:
```json
"Hard Mode": {
    "yaml_option": ["enable_hard_mode"]
},
"Second DLC": {
    "yaml_option": ["!dont_include_dlc2"]
}
```

Additionally, if you provide multiple option keys inside the `[]` for a `yaml_option`, all of those options have to be true (or false for the ones that start with `!`) for the items/locations with that category to be included in the multiworld.

