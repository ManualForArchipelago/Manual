# Updating a Manual
Usually, world creators will keep their Manual apworlds up-to-date. Some worlds might not be updated, though, and are old enough to where they either don't work with our client or don't generate. So whether you're a world creator or someone looking to update a Manual apworld for someone else, this doc is for you!

## Updating automatically

For most apworlds, you can import the apworld into the Manual Builder and, upon export, it will be updated to the most recent Manual release version. You can find the Manual Builder here: https://manualforarchipelago.github.io/ManualBuilder/

## Updating manually

To manually (heh) update a Manual apworld:
1. Rename your .apworld file to .zip and unzip it.
2. Copy the "data" folder from your unzipped apworld to another location. (You'll be restoring this in a few steps).
2b. If you've written any hooks, copy the "hooks" folder to another location as well. _If you don't know what hooks are or know you haven't used them with this world, skip this step._
3. Download the latest Manual release .apworld file from our Releases page here on GitHub.
4. Extract the release .apworld (by renaming as above, or by associating your favorite zip extractor with the .apworld extension) (you may rename the file extension to .zip, but it's easier to just associate .apworld with your extractor of choice)
5. Copy everything from the inside of the unzipped release apworld into the unzipped apworld folder that you're updating.
6. Copy the "data" folder from step 2 and paste it back into your unzipped apworld folder that you're updating. (This will overwrite the release apworld's data folder, which is fine.)
7. Go to the folder above the unzipped apworld folder that you're updating, then right-click the unzipped apworld folder that you're updating and choose the option to compress/zip the folder.
8. Make sure the zip file is named the same as the apworld folder was (plus the .zip extension, of course).
9. Rename the .zip to .apworld again, and you should be good to go!


