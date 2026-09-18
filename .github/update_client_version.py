"""Update the client version in __init__.py with today's date"""
import ast
import datetime
import os

file = os.path.abspath(os.path.join(__file__, "..", "..", "src", "__init__.py"))
with open(file, 'r') as f:
    text = f.read()
tree = ast.parse(text)
lines = text.splitlines()

assigns = [s for s in tree.body if isinstance(s, ast.FunctionDef)]
for func in assigns:
    name = func.name
    if name == "add_client_to_launcher":
        for node in func.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "version":
                line_no = node.lineno
                col_start = node.col_offset
                col_end = node.end_col_offset
                old_text = lines[line_no - 1][col_start:col_end]
                new_date = datetime.datetime.now().strftime("%Y_%m_%d")
                text = text.replace(old_text, f'version = {new_date}')

with open(file, 'w') as f:
    f.write(text)
