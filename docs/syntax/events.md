# Events - events.json
Your events.json contains the details about any events that you have in your world. 

This file contains multiple objects, so you'll want to have a `[]` surrounding the `{}` objects to be valid JSON. If your events.json has a "$schema" property at the top, use the `[]` in the "data" property instead.

## Wait, what are events and why are they useful?
Events are essentially "fake" items that you configure like you would a location, which can then be referenced in logical requirements. Events are often used to simplify complicated logic chains, or to reduce redundant locations using placed items. As a "fake" item, it doesn't need to be placed on a location to be "received", as it's automatically received when its requirements are met. 

Basically, using an event, you can track a set of requirements without having to have an extra location or extra "gating" items, then use that event as a logical requirement (as if it was an item) for your other locations/regions. It's pretty handy!

(This is also the recommended replacement for `CanReachLocation` usage, as events don't have any of the shortcomings and are faster during generation.)

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the events.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.events.schema.json).

## The events.json structure
The properties for this file are broken down into these headings below:
- [Naming and categorizing](#naming-and-categorizing)
  - `name`
  - `category`
- [Assigning a region](#assigning-a-region)
  - `region`
- [Logical requirements](#logical-requirements)
  - `requires`
- [Using an accessible location as an event](#using-an-accessible-location-as-an-event)
  - `copy_location`
- [Hiding the event in the Manual client](#hiding-the-event-in-the-manual-client)
  - `visible`

### Naming and categorizing
The minimum information you need to provide for an event is its name. Here's an example of that simple event definition:

```json
{
    "name": "All Purple Buttons Found"
}
```

(A name cannot contain the characters `:` or `|`, and it's not recommended to use non-english characters not supported by Archipelago's default font.)

If you then want to categorize that event, you can assign it one or more "category" names to be assigned to. See the [Categories for Items and Locations](syntax/categories-for-items-and-locations.md) page for more information.

### Assigning a region
Regions can be helpful to either establish a world layout for your world, or to group together events that share logical requirements. Each event can only be assigned to a single region. Once you've determined which region you'd like to assign to a event, you can set the `region` property to the name of the region.

Here's an example that assigns the "Last Dungeon" region to the "All Purple Buttons Found" event:

```
{ 
    "name": "All Purple Buttons Found", 
    "region": "Last Dungeon"
}
```

### Logical requirements
Just like with locations, logical requirements define what should be required for the event to be "active". However, unlike locations, you don't need to check off events in the client for them to be "completed". Events are completed as soon as their logical requirements are met.

See the [Requires for Locations and Regions](syntax/requires-for-locations-and-regions.md) page for more information.

### Using an accessible location as an event
Another use case for events is to reduce the number of duplicate locations that you would've previously used to give a "gating" item for logic.

Instead of duplicate locations, you can use the `copy_location` property to specify a location name that this event should copy. Then, when the location that it copies is logically accessible, the event will be too!

When you use this property to copy a location, it copies all applicable properties (`requires`, `region`, etc.). If you specify any of these properties on the event, the event's properties will override the copied ones from the location.

Here's an example that creates an event that copies the "Player Level Up - Level 10" location:

```
{ 
    "name": "Player Level 10", 
    "copy_location": "Player Level Up - Level 10"
}
```

That way, you can have a randomized item on the "Player Level Up - Level 10" location, but also track when the player's level reached 10.

### Hiding the event in the Manual client
By default, events are shown in the items half of the Manual client. If you'd like to hide them instead, set the `visible` property to false.

Here's an example of hiding the "Player Level 10" event from showing in the client:

```
{ 
    "name": "Player Level 10", 
    "visible": false
}
```
