# Options - options.json
Your options.json contains the details about any options that you've created for your world. 

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the options.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.options.schema.json).

## Definitions of "core" options versus "user" options
You may have noticed in the example options.json (contained within each stable Manual release apworld) or in the schema above that there are two sections where you can specify option properties: a "core" section and a "user" section.

The "core" section allows you to modify some portions of existing core options that are defined by Manual. Don't use this section to create your own options, as they'll be ignored. For a list of the core options that you can modify, reference the examples in the "core" section of the options.json example provided in every stable Manual release apworld.

The "user" section allows you to create your own custom options.

## The options.json structure
The properties for this file are broken down into these headings below:
- [Naming and assigning an option type](#naming-and-assigning-an-option-type)
  - `name`
  - `type`
- [Setting a formatted display name](#setting-a-formatted-display-name)
  - `display_name`
- [Setting the option description](#setting-the-option-description)
  - `description`
  - `rich_text_doc`
- [Setting a default option value](#setting-a-default-option-value)
  - `default`
- [Showing or hiding options in the YAML](#showing-or-hiding-options-in-the-YAML)
  - `hidden`
  - `visibility`
- [Adding the option to an option group](#adding-the-option-to-an-option-group)
  - `group`
- [Settings specific to Toggle types](#settings-specific-to-toggle-types)
  - (none)
- [Settings specific to Choice types](#settings-specific-to-choice-types)
  - `values`
  - `aliases`
  - `allow_custom_value`
- [Settings specific to Range types](#settings-specific-to-range-types)
  - `range_start`
  - `range_end`
  - `values`

### Naming and assigning an option type
The minimum information you need to provide for an option is its name and its option type. For its name, you'll need to refrain from using spaces or starting the name with a number; just use letters, numbers, and underscores. For its option type, the only supported option types (currently) are "Toggle", "Choice", and "Range". For more information on these default Archipelago option classes, see [their documentation here](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md#basic-option-classes).

Here's an example of an option definition with the minimum required information:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle"
        }
    }
}
```

### Setting a formatted display name
If you want to customize the way that an option name is displayed in the YAML / spoiler log, you can use the `display_name` property.

Here's an example of an option definition that customizes its display name:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "display_name": "Add Bonus Characters To Items"
        }
    }
}
```

### Setting the option description
It's recommended to add a description to your option so that people configuring their YAML have some idea of what your option does. To add a description, you'd use the `description` property. To support multiline descriptions, you specify the description as an array of each line of the description.

Here's an example of an option definition that adds a description:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "description": [
                "Only turn on this option if you have the bonus characters from the 'Time Banana' DLC.",
                "This option adds Prehistoric Banana, Renaissance Banana, and Skynet Banana to the item pool."
            ]
        }
    }
}
```

If you want your description to be formatted as rich text on a webhost, you can set the `rich_text_doc` property to true.

Here's an example of setting a description to be rich text on a webhost:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "description": [
                "Only turn on this option if you have the bonus characters from the 'Time Banana' DLC.",
                "This option adds Prehistoric Banana, Renaissance Banana, and Skynet Banana to the item pool."
            ],
            "rich_text_doc": true
        }
    }
}
```

### Setting a default option value
If you want your option to have a default value, use the `default` property.

Here's an example of giving a Toggle option a default value:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "default": true
        }
    }
}
```

(For the AP dev enjoyers reading this: Yes, we turn that into a `DefaultOnToggle` in the background.)

### Showing or hiding options in the YAML
If you want to hide an option from showing in the YAML, you'd set the `hidden` property to true. 

Here's an example of hiding an option in the YAML:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "hidden": true
        }
    }
}
```

If you want more fine-grained control over the situations in which an option is shown -- including in YAMLs and spoiler logs -- you'd use the `visibility` property. You can use any of the visibility flags shown in [AP's documentation about Visibility](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md#option-visibility).

Here's an example of setting more fine-grained visibility settings on an option:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "visibility": [
                "simple_ui",
                "complex_ui",
                "template"
            ]
        }
    }
}
```

### Adding the option to an option group
If you'd like to show one or more options in a option group in the YAML, you can set the `group` property to the name of the option group it should show up in. If the option group doesn't exist, it will be created.

Here's an example of setting an option group for an option:

```json
{
    "user": {
        "add_bonus_characters": {
            "type": "Toggle",
            "group": "DLC-Only Content"
        }
    }
}
```

### Settings specific to Toggle types
There are no specific settings for Toggle types that aren't shared by all other option types.

### Settings specific to Choice types
Choice option types have a few settings that are specific to Choices only.

#### Specifying a list of valid values
Choices should have a specific set of values that they expect the user to choose from for the option value in their YAML. You can specify these using the `values` property.

Here's an example of a Choice option defining what values it accepts:

```json
{
    "user": {
        "starting_thing": {
            "type": "Choice",
            "values": {
                "none": 0,
                "purple_thing": 1,
                "thing2": 2,
                "raspberry_flavored_thing": 3
            }
        }
    }
}
```

#### Specifying a list of aliases that can be used instead of values
Choices can also define a number of aliases that map back to values. This can be helpful if you want to allow the user to specify any of multiple names to mean the same value.

Here's an example of a Choice option defining what aliases it accepts as values:

```json
{
    "user": {
        "starting_thing": {
            "type": "Choice",
            "aliases": {
                "you_know_that_purple_one": 1,
                "the_second_thing_bro": 2
            }
        }
    }
}
```

#### Allowing a custom value instead of choosing a pre-defined one
Most Choice options require picking from a list of pre-defined possible values... but, if you instead want the player to supply a text string in their YAML that you use as the chosen value, you can set the `allow_custom_value` property to true. 

Here's an example of a Choice option that allows the player to supply a custom text value in their YAML:

```json
{
    "user": {
        "starting_thing": {
            "type": "Choice",
            "allow_custom_value": true
        }
    }
}
```

(Internally, this changes the option from a Choice to a TextChoice.)

### Settings specific to Range types
Range option types have a few settings that are specific to Ranges only.

#### Specifying the bounds for your range's values
A Range option lets you pick a number in a range of numbers, so you need to be able to specify that range. For that, you'd use the `range_start` and `range_end` properties to define the start of the range and the end of it, respectively.

Here's an example of a Range option that defines the upper and lower bounds of its possible numeric values:

```json
{
    "user": {
        "how_many_potatoes": {
            "type": "Range",
            "range_start": 0,
            "range_end": 25
        }
    }
}
```

#### Specifying custom names for specific values in the range
If there are common values that you'd expect a user to choose within your Range option's bounds, you could name those for convenience by using the `values` property.

Here's an example of a Range option that defines some common values by name for use by players in their YAML:

```json
{
    "user": {
        "how_many_potatoes": {
            "type": "Range",
            "range_start": 0,
            "range_end": 25,
            "values": {
                "a_pair": 2,
                "one_bowl_of_mashed": 5,
                "im_gonna_be_sick": 15,
                "i_am_100_percent_potato_now": 25
            }
        }
    }
}
```

