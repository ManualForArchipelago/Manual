# Categories for Items and Locations

Categories are an argument like "victory" and "count", except it requires [Square Brackets] because it can contain multiple items. Their syntax is the same for both locations and items (respectively):
```
{ 
    "name": "Coins",
    "category": ["Currencies"]
    "count": 25, 
    "progression": true
}
```
```
{ 
    "name": "Kill First Boss", 
    "category": ["First Dungeon", "Boss Fight"], 
    "requires": "|Sword|"
}
```

Categories do not affect logic, but will group items up as they display in the client, and locations will be able to be set to give an item from a specific category
Above, Kill First Boss is part of two categories at the same time, while Coins is only part of Currencies. 

