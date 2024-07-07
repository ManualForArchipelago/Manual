
# called after the items.json has been imported, but before ids, etc. have been assigned
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def before_item_table_processed(item_table: list) -> list:
    return item_table

# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the 
def hook_get_filler_item() -> str | bool:
    return False
