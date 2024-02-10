<!-- omit from toc -->
# Json Schemas
<!-- omit from toc -->
## Table of content

- [Why you should use them](#why-you-should-use-them)
- [How to use them](#how-to-use-them)
  - [Intro](#intro)
  - [Vscode](#vscode)
    - [VScode Text Only](#vscode-text-only)
    - [VScode With Pictures](#vscode-with-pictures)
  - [Visual Studio](#visual-studio)
    - [Visual Studio Text Only](#visual-studio-text-only)
    - [Visual Studio With Pictures](#visual-studio-with-pictures)

## Why you should use them

Json schemas tell your Ide (integrated development environment) aka your text editor of choice  
how a json file should be formated and also include short descriptions of what a property is used for.  
They also tell your IDE if you have error in how you used the properties (eg. used both "player" and "creator" in game.json)

## How to use them

### Intro

Like many things in Coding it depend on your IDE.  
Bellow you will find instructions for the IDE we knew how to import Schemas.  
More might be added as we find how to use Json schemas with them.

Most of the time you either need the url of the [Json Catalog](/schemas/Manual.schema.catalog.json)  
or the url of the other schemas that you can find in the catalog.

- [VsCode](#vscode)
- [Visual Studio](#visual-studio)
- [Pycharm: Check official docs](https://www.jetbrains.com/help/pycharm/json.html#ws_json_schema_add_custom)
  - Uses the content of the catalog
- others to be added in the future

### Vscode

VsCode doesnt support the catalog directly but you can copy and past it's content in your settings like so:

- [Text Only](#vscode-text-only)
- [With Pictures](#vscode-with-pictures)

#### VScode Text Only

1. Open your settings, usually by clicking the cog icon in the bottom left and selecting settings in the menu.
2. In the search bar at the top of the screen write 'Schemas' and in Json Schema click on the 'Edit in settings.json' button.
3. The Settings.json should open with your cursor on the "json.schemas" property.
4. Open the [catalog](/schemas/Manual.schema.catalog.json) and copy everything in the "schema" array
5. Paste it in the "json.schemas" proterty array in settings.json
6. Make sure your setting.json is valid by adding ',' if required.
7. Dont forget to save.

That should do it from now on if you open any json file from manual you should get recommended properties when you edit  
items/locations/regions/etc

[Back to intro](#intro)

#### VScode With Pictures

1. Open your settings, usually by clicking the cog icon in the bottom left and selecting settings in the menu.
2. In the search bar at the top of the screen write 'Schemas' and in Json Schema click on the 'Edit in settings.json' button.
  ![Screenshot of the setting page and what the button look like](/docs/img/schemas/VSCode_settings_search.PNG)
3. The Settings.json should open with your cursor on the "json.schemas" property.
   1. It might look different if you already uses schemas.  
![Screenshot of the setting.json](/docs/img/schemas/VSCode_settings.json_find_jsonschemas.PNG)
4. Open the [catalog](/schemas/Manual.schema.catalog.json) and copy everything in the "schema" array
  ![Screenshot of the catalog which shows evertything in the 'schemas' array selected](/docs/img/schemas/VSCode_catalog_copy_schemas.PNG)
5. Paste it in the "json.schemas" proterty array in settings.json
6. Make sure your setting.json is valid by adding ',' if required so it looks like this
  ![Screenshot of the result of following the instruction in settings.json](/docs/img/schemas/VSCode_settings.json_final.PNG)
7. Dont forget to save.

That should do it from now on if you open any json file from manual you should get recommended properties when you edit  
items/locations/regions/etc

[Back to intro](#intro)

### Visual Studio

Visual Studio support the catalog directly and only wants catalogs which make this a bit easier.

- [Text Only](#visual-studio-text-only)
- [With Pictures](#visual-studio-with-pictures)

#### Visual Studio Text Only

1. Open your options by clicking on Tools -> Options.
2. In the search bar at the top of the screen write 'json schema' and on the left click on Text Editor -> JSON -> Schema
3. Click the button on the top right that looks like a folder with a sun. It will create a new entry in the list.
4. Open the [catalog](/schemas/Manual.schema.catalog.json) on github and click on the Raw button on the top right of the code block.
5. Copy the url of the page your browser was redirected to. (it should start with https:// followed by raw.githubusercontent.com/ManualForArchipelago/...)  
6. Paste the url in the new entry of the schema list
7. Press ok and restart your Visual Studio.

That should do it from now on if you open any json file from manual you should get recommended properties when you edit  
items/locations/regions/etc

[Back to intro](#intro)

#### Visual Studio With Pictures

1. Open your options by clicking on Tools -> Options.
2. In the search bar at the top of the screen write 'json schema' and on the left click on Text Editor -> JSON -> Schema
3. Click the button on the top right that looks like a folder with a sun. It will create a new entry in the list.
  ![Screenshot of the Options page and what the button look like](/docs/img/schemas/VisualStudio_settings_search.PNG)
4. Open the [catalog](/schemas/Manual.schema.catalog.json) on github and click on the Raw button on the top right of the code block.
  ![Screenshot of where the raw button is on github](/docs/img/schemas/VisualStudio_Catalog_RAW.PNG)
5. Copy the url of the page your browser was redirected to. (it should start with https:// followed by raw.githubusercontent.com/ManualForArchipelago/...)  
6. Paste the url in the new entry of the schema list and press Enter to confirm
  ![Screenshot of the result of following the instruction in settings.json](/docs/img/schemas/VisualStudio_settings_final.PNG)
7. Press ok and restart your Visual Studio.

That should do it from now on if you open any json file from manual you should get recommended properties when you edit  
items/locations/regions/etc

[Back to intro](#intro)
