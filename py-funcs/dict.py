# Import dependencies
#

# Functions
def get_path(key, dictionary):
    """Return the key path required to access a given key in a dict of nested dicts (usually from a json)"""
    path = []
    if key in dictionary:  # check if key is on top level
        path.append(key)
        return path
    for k, v in dictionary.items():
        if v:  # check if there are keys in the next level
            ext = get_path(key, v)
            if ext:  # check if key was found in a lower level
                path.append(k)
                path.extend(ext)
                return path
    return None


def flatten(dictionary):
    """Flatten a dict of nested dicts into a list of all the keys that it contains"""
    flat = []
    for k, v in dictionary.items():
        flat.append(k)
        if v:  # check if there are keys in the next level
            flat.extend(flatten(dictionary[k]))
    return flat