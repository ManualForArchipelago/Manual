# Meta - meta.json
Your meta.json mainly contains the descriptive meta details about your world. Additionally, it contains an option to visualize the regions for your world, which can be helpful when debugging world issues.

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the meta.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.meta.schema.json).

## The meta.json structure
The properties for this file are broken down into these headings below:
- [Visualizing region connections with UML](#visualizing-region-connections-with-uml)
  - `enable_region_diagram`
- [APWorld description](#apworld-description)
  - `apworld_description`
- [WebWorld - Tutorials](#webworld---tutorials)
  - `tutorials`
- [WebWorld - Theme](#webworld---theme)
  - `theme`
- [WebWorld - Game Info Languages](#webworld---game-info-languages)
  - `game_info_languages`
- [WebWorld - Options Presets](#webworld---options-presets)
  - `options_presets`
- [WebWorld - Options Page](#webworld---options-page)
  - `options_page`
- [WebWorld - Bug Report Page](#webworld---bug-report-page)
  - `bug_report_page`

### Visualizing region connections with UML
When troubleshooting region connections while building a world, it can be helpful to see that you've connected those regions (and their locations) properly. By setting the `enable_region_diagram` property to true, a UML file will be added to your Archipelago install folder when you generate this world. Open that UML file in a UML viewer (such as PlantUML), and it will lay out region connections with boxes and lines interconnecting them.

Here's an example of enabling the creation of a region diagram during generation:

```json
{
    "enable_region_diagram": true
}
```

### APWorld description
The world description describes the game that this APWorld was made for. This is the text that is shown for that game in the "Supported Games" listing of a running webhost.

Here's an example of setting that world description:

```json
{
    "docs": {
        "apworld_description": "This is a game about selling bananas. Sell all the bananas to be the banana time emperor of all time."
    }
}
```

### WebWorld - Tutorials
WebWorld contains properties that are shown on a running webhost. The `tutorials` property lists links to tutorial documents for that game.

Here's an example of defining a tutorial:

```json
{
    "docs": {
        "web": {
            "tutorials": [
                {
                    "name": "How to run the companion app",
                    "description": "A guide to running the companion app for Banana Time Emperor.",
                    "language": "English",
                    "file_name": "setup_en.md",
                    "link": "setup/en",
                    "authors": ["Ben Annatime"]
                }
            ]
        }
    }
}
```


### WebWorld - Theme
WebWorld contains properties that are shown on a running webhost. The `theme` property chooses from a list of available theme names for the background of this game's pages on the webhost.

Here's an example of setting a theme:

```json
{
    "docs": {
        "web": {
            "theme": "grass"
        }
    }
}
```

### WebWorld - Game Info Languages
WebWorld contains properties that are shown on a running webhost. The `game_info_languages` property lists the available languages for tutorials that you provide using the `tutorials` property above.

Here's an example of setting those languages:

```json
{
    "docs": {
        "web": {
            "game_info_languages": ["en", "fr"]
        }
    }
}
```

### WebWorld - Options Presets
WebWorld contains properties that are shown on a running webhost. The `options_presets` property defines preset names that players can choose from when on the options page, which will fill in a series of option values that fit that preset name. You might use this for difficulty presets, logic complexity, etc.

Here's an example of defining an options preset:

```json
{
    "docs": {
        "web": {
            "options_presets": {
                "Harder Enemies": {
                    "enemy_damage_random": true,
                    "boss_shuffle": true
                }
            }
        }
    }
}
```

### WebWorld - Options Page
WebWorld contains properties that are shown on a running webhost. The `options_page` property defines an optional link to a custom options page. If you plan to use the default webhost options page with this world, you don't need to set this property.

Here's an example of setting a custom options page:

```json
{
    "docs": {
        "web": {
            "options_page": "https://finalfantasyrandomizer.com/"
        }
    }
}
```

### WebWorld - Bug Report Page
WebWorld contains properties that are shown on a running webhost. The `bug_report_page` property defines an optional link where users can report bugs with the world. This would be a great place to link any Discord channels, GitHub issues links, etc.

Here's an example of setting a custom bug report page:

```json
{
    "docs": {
        "web": {
            "bug_report_page": "https://giphy.com/gifs/no-bugs-bunny-fXnRObM8Q0RkOmR5nf"
        }
    }
}
```

