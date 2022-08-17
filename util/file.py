# Import dependencies
import os, sys, json

# Functions
def read_json(path):
    """Read a .json file path to a python dictionary"""
    with open(path, 'r') as j:
        contents = json.loads(j.read())
    return contents


def write_json(dictionary, path):
    """Write a python dictionary to a .json file path"""
    with open(path, 'w') as j:
        json.dump(dictionary, j)


def append(path, text):
    # a+ = open file and add to end or create if not exist
    with open(path, 'a+') as f:
        f.write(text)


def write(path, text):
    # w+ = open file and overwrite contents or create if not exist
    with open(path, 'w+') as f:
        f.write(text)


def read(path, verbose=False):
    try:
        # get all text from file
        with open(path, 'rt') as f:
            text = f.read()
        if verbose: print(text)
        return text
    except:
        if verbose: print(f'File at "{path}" not found')
        return