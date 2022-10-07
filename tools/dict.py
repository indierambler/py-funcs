# Import dependencies
import numpy as np

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


def keys_to_str(d):
    """Convert all the keys in a dict to string type (usually so that it can be serialized)"""
    new = {}
    for key, val in d.items():
        if isinstance(val, dict):
            new[str(key)] = keys_to_str(val)
        else:
            new[str(key)] = val
    return new


def print_val_types(d):
    """Print all of the keys in a dict with their datatypes (mainly for debugging)"""
    for key, val in d.items():
        if isinstance(val, dict):
            print_val_types(val)
        else:
            print(f'{key}: {type(val)}')


def convert_numpy_vals(d):
    """Convert all numpy types in a dict to python types (usually so that it can be serialized)"""
    new = {}
    for key, val in d.items():
        if isinstance(val, dict):
            new[key] = convert_numpy_vals(val)
        elif isinstance(val, (np.integer)):
            new[key] = int(val)
        elif isinstance(val, (np.inexact)):
            new[key] = float(val)
        elif isinstance(val, np.ndarray):
            new[key] = list(val)
        else:
            new[key] = val
    return new