# Import dependencies
import os, random


def get_dirs(directory, fullpath=False, recursive=False):
    """ Create a list of all the directories inside a
        given directory
    Args:
        directory (str): string representation of the directory to search
        fullpath (bool): select whether or not to return full paths or just directory names
        recursive (bool): select if directories should be searched and returned recursively
    Return:
        list: all directory paths or names in directory
    """
    # add a slash to the directory if needed
    if directory[len(directory)-1] != '/': 
        directory = directory + '/'

    # extract all contents from the dir without an extension
    dirs = [x for x in os.listdir(directory) if os.path.splitext(x)[1] == '']

    # handle paths and recursivity
    if dirs and (fullpath or recursive):
        dirs = list(map(lambda x: directory + x, dirs))  # expand to full paths
        if recursive:
            dirs.extend([get_dirs(x, fullpath=True, recursive=True) for x in dirs])  # get child dirs
        if not fullpath:
            dirs = list(map(lambda x: os.path.split(x)[1], dirs))  # collapse to just dir names

    return dirs


def get_files(directory, ext=''):
    """ Get the paths of all requested file types in a 
        given directory (recursively) to a new list
    Args:
        directory (str): string representation of the directory to search.
        ext (str): file extension to search for.
    Return:
        list: the list of file paths is returned
    """
    # add slash and add period to input as needed
    if directory[len(directory)-1] != '/': 
        directory = directory + '/'
    if ext != '' and ext[0] != '.':
        ext = '.' + ext

    files = []
    # build a list of all contents in the directory
    contents = os.listdir(directory)
    contents = list(map(lambda x: directory+x, contents))
    # index the list checking if the item is a file or directory
    for i in contents:
        # if file: add to the list (if it has the correct extension)
        if os.path.isfile(i) and (ext == os.path.splitext(i)[1] or ext == ''):
            files.append(i)
        elif os.path.isdir(i):
            files += get_files(i, ext=ext)

    return files


def get_structure(directory):
    """Return all contents of a directory as a dictionary hierarchy
    """
    struct = {}
    contents = os.listdir(directory)  # list all contents in the directory
    for i in contents:
        path = os.path.join(directory, i)
        if os.path.isfile(path):
            struct[i] = {}
        elif os.path.isdir(path):
            struct[i] = get_structure(path)
    return struct


def random_file(directory, ext=None):
    """ Choose a random file (with a given extension)
        from a directory and return the path as a string
    Args:
        directory (str): string representation of the directory to search.
            Do not end with a slash.
        ext (str): file extension to search for.
            Always begin with a period. (i.e. '.wav')
    Return:
        list: the list of file paths is returned
    """
    files = get_files(directory, ext=ext)
    if len(files) > 0:
        path = files[random.randint(0, len(files)-1)]
    else:
        raise FileNotFoundError(f'No files of type "{ext}" were found in "{directory}"')
    return path

def get_filename(path, ext=True):
    filename = os.path.split(path)[1]
    if not ext:
        filename = os.path.splitext(filename)[0]
    return filename