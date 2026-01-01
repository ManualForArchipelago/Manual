# Events - events.json
Your events.json contains the details about any events that you have in your world. 

This file contains multiple objects, so you'll want to have a `[]` surrounding the `{}` objects to be valid JSON. If your events.json has a "$schema" property at the top, use the `[]` in the "data" property instead.

## Wait, what are events and why are they useful?
Events are essentially "fake" items that can be used to simplify complicated logic chains or reduce redundant locations using placed items. As a "fake" item, it doesn't need to be placed on a location to be "received". 

Using an event, you can track when a certain requirement has been met. You can then require that event elsewhere as if it was an item, too. It's pretty handy!

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the events.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.events.schema.json).

## The events.json structure
The properties for this file are broken down into these headings below:
- [Naming and categorizing](#naming-and-categorizing)
  - `name`
  - `category`
-
