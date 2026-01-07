# Comments on JSON objects

Sometimes, you might find it helpful to document information internally that helps you or others develop your Manual world. For that, you can use the `_comment` property inside any JSON object `{}` in Manual's JSON files. 

(Don't use any other property except `_comment` for comments, as there are some parts of validation that will error with invalid properties.)

Here's an example of adding a comment to a location that you've defined:

```
{ 
    "name": "Final Door", 
    "region": "Last Dungeon",
    "_comment": "This final location is accessible from 2 regions in the Overworld and one region in the Nether."
}
```

You can also add comments to the top-level portions of any Manual JSON file.

Here's an example of adding a comment near the top of your locations.json file:

```
{ 
	"$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.locations.schema.json",
    "_comment": "TODO: Come back and add the locations for The End and assign categories for them.",
    
    "data": [
        {
            "name": "Punch Tree",
            "region": "Overworld"
        },
        {
            "name": "Make Crafting Table",
            "region": "Overworld"
        },

        ...
    ]
}
```

