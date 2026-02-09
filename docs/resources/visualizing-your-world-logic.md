# Visualizing Your World Logic

## Visualizing Regions as a UML Diagram
When troubleshooting region connections while building a world, it can be helpful to see that you've connected those regions (and their locations) properly. By setting the `generate_region_diagram: true` in your yaml, a UML file will be added to your Archipelago install folder when you generate this world. Open that UML file in a UML viewer (such as PlantUML), and it will lay out region connections with boxes and lines interconnecting them.

![](../img/resources/visualize-regions-uml-example.png)

To generate a region diagram:

1. Install your apworld as if you were going to play it
2. Generate a template yaml, and set any options that might change the logic
3. Add `generate_region_diagram: true` to your yaml
4. Generate a seed
5. Find the .puml file that gets generated in your Archipelago folder. It will have the same name as your apworld.
6. Put the contents of that file into a viewer like [PlantUML](https://www.planttext.com/)

## Organizing Connected Ideas on a Graph
Some tools can help with visualizing your game's structure.
https://csacademy.com/app/graph_editor/ allows you to make a node graph that you can use to represent aspects of your logic.
