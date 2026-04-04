## Yaml Pick and Choose

People often ask "Is it possible to make a yaml option where you choose a list of things to enable/disable".

This is usually in the context of a live-service game, where your manual has a large roster of possible characters.

## Items.json
For a manual like this, it makes sense to start with our champions.  We're going to pick the cast of League of Legends for this example.

```json
[
  { "name": "Aatrox", "category": ["Champion", "Fighter"], "progression": true },
  { "name": "Ahri",   "category": ["Champion", "Mage", "Assassin"], "progression": true },
  { "name": "Akali",  "category": ["Champion", "Assassin"], "progression": true },
  { "name": "Ashan",  "category": ["Champion", "Marksman", "Assassin"], "progression": true },
]
```

Note that each champion has the category "Champion".  We'll be using that later.

## Locations.json
Next, let's set up some locations.
```json
[
    {"name": "Win a game with any champion", "category": ["Wins"]},
    {"name": "Win a game with Aatrox", "category": ["Aatrox", "Wins"]},
    {"name": "Jungle with Ahri", "category": ["Ahri", "Jungling"]},
    {"name": "Fully Equip Teemo", "category": ["Teemo", "Shopping"]},
]
```

Note that some locations have a category with a champion's name.  We'll also use this later.

## hooks/Options.py

The next thing we need to do is to define our option.  We're going to use a hook, because it's more versatile than using options.json

```py
from Options import OptionSet
from ..Items import item_name_groups

class EnabledChampions(OptionSet):
    """Champions that will be in your world."""  # Description of the yaml option in the template
    display_name = "Enabled Champions"           # Name of the option in the spoiler
    valid_keys = item_name_groups["Champion"]    # This is the bit that matters.  Our yaml option wants you to pick names of items in the Champion category
    default = frozenset(valid_keys)              # This makes the default value list all of them.  It's easier for a player to delete ones they don't have than it is to guess what should be added.

def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["enabled_champions"] = EnabledChampions  # This registers the yaml option as `enabled_champions`
    return options
```

This does one thing very efficiently.  It takes the list of every item name in the Champions category, and puts it in a yaml option:

```yaml
  enabled_champions:
  - Aatrox
  - Ahri
  - Akali
  - Ashan
```

## hooks/Helpers.py

So, we have our items, we have our locations.  We even have a yaml option.  All that's left is to wire it all up.

Thankfully, this is also very easy.  We're going to use two hooks here:
```py
from ..Items import item_name_groups
def before_is_item_enabled(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    # Remove unwanted champions from the item pool
    if "Champion" in item["category"]:
        from ..Helpers import get_option_value
        enabled_champions = get_option_value(multiworld, player, "enabled_champions")
        return item["name"] in enabled_champions  # True if they're in the yaml, false if they're not
    return None

def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if category_name in item_name_groups["Champion"]:
        # This category is the name of a champion
        from ..Helpers import get_option_value
        enabled_champions = get_option_value(multiworld, player, "enabled_champions")
        return category_name in enabled_champions
    return None
```

Our first hook toggles the champions themselves.  You could technically skip this by putting each champion in their category, but if your manual doesn't have champion-specific locations (And instead just needs any champion of a given category) that would be overcomplicating things for no benefit.

Our second hook toggles any other items/locations that have the champion's category.  This is to remove anything that needs them in the pool to be relevant.

#### A note about the `from ..Helpers import get_option_value` import

I'm sure some of you are wondering why we're importing it within the function body, rather than doing it once at the top of the file.

This is a quirk that comes from trying to import a function from Helpers.py from within hooks/Helpers.py.  We need to import them when the function is run, because doing so any earlier would lead to a circular reference and your manual will fail to load.  

It looks weird and awkward, but it's what you need to do.  Sorry.
