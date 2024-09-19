#Made this file for functions that do not require imports from Manual (to help with circular imports)
import os
import pkgutil
import json

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

def load_json_file(*args) -> dict:
    fname = os.path.join("", *args)

    try:
        filedata = json.load(open(fname))
    except:
        filedata = {}

    return filedata

def load_remote_json(url: str, has_internet: bool = True) -> dict:
    import requests
    if url.startswith('file:'):
        data = load_json_file(url.lstrip("file:").lstrip("/\\"))
    else:
        if not has_internet:
            return {}
        resp = requests.get(url)
        data = json.loads(resp.text)
    return data

def have_internet() -> bool:
    import http.client as httplib
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

def clamp(value, min, max):
    """Returns value clamped to the inclusive range of min and max"""
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value