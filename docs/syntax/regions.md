# Regions - regions.json
Your regions.json contains the details about all of the regions in your world. Regions are commonly used to group together locations that are related or have similar requirements, or to consolidate your game logic to make it easier to edit.  

## Wait, I've made apworlds in AP before and regions aren't optional there?
By default, Manual creates a region (named "Manual") to house all of your locations that don't have a region assigned. So, if you omit a regions.json, all locations just get added to that default region. :)

## Schema of valid properties and values
If you'd like to see all the available properties and their allowed values, view [the schema file for the regions.json here](https://github.com/ManualForArchipelago/Manual/blob/main/schemas/Manual.regions.schema.json).

## The regions.json structure
The properties for this file are broken down into these headings below:
- [Naming](#naming)
  - (none)
- [Starting with access to a region](#starting-with-access-to-a-region)
  - `starting`
- [Connecting from one region to another](#connecting-from-one-region-to-another)
  - `connects_to`
- [Logical requirements](#logical-requirements)
  - `requires`
  - `entrance_requires`
  - `exit_requires`

---

### Naming
The minimum information you need to provide for a region is its name. Here's an example of that simple region definition:

```json
{
    "Overworld": {

    }
}
```

(It's not recommended to use non-english characters not supported by Archipelago's default font.)

---

### Starting with access to a region
In some cases, you'd want a region to be available from the beginning of your playthrough. To ensure that you don't need any other region connections to reach that region, you can use the `starting` property to mark a region as one of the first regions that you can reach.

Here's an example of marking a region as a starting region:

```json
{
    "Overworld": {
        "starting": true
    }
}
```

NOTE: If you mark a region as a starting region and it has logical requirements that you haven't met, you will not be able to access that region.

---

### Connecting from one region to another
Sometimes, you want to define a specific world layout or order that regions should be accessed in. For this, you'd define region-to-region connections using the `connects_to` property. When you define a connection using that property, you specify the next region that you would be able to access after leaving this region.

Here's an example that connects from the "Overworld" starting region to the "Nether" region:

```json
{
    "Overworld": {
        "starting": true
        "connects_to": ["Nether"]
    },
    "Nether": {

    }
}
```

NOTE: `connects_to` connections are _one-directional_ when defined, because it is implied that you can travel backwards across a connection that you already used. So, in the vast majority of cases, you will only need to define the "forward" connection.

---

### Logical requirements
Logical requirements ensure that your region is not put into logic before it should be reachable. Additionally, when there is a location associated with your region, that location inherits all of the logical requirements of the region while also retaining its own logical requirements.

You can use the default `requires` property to assign logical requirements as you would with locations. If you need to be more particular about the logical requirements on each part of traversing a region, you can use `entrance_requires` / `exit_requires` to assign logical requirements specifically to the inbound connection (entrance) of a region or the outbound connection (exit) of a region, respectively.

See the [Requires for Locations and Regions](requires-for-locations-and-regions.md) page for more information about requires in general.

NOTE: A region marked as `starting` or referenced in another region's `connects_to` can't be reached if there are logical requirements and those logical requirements are not met.

