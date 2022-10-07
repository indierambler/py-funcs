# Import dependencies
import datetime

# Functions
def timestamp():
    """Get a timestamp that can be appended to a file name to make it unique
    """
    return datetime.now().strftime("%Y%m%d%H%M%S")


def datestamp():
    """Get a datestamp that can be appended to a file name to make it unique
    """
    return datetime.now().strftime("%Y%m%d")


def convert_time(s):
    if s < 60:  # less than 1 minute
        label = f'{s}sec'
    elif s < 3600:  # less than 1 hours
        label = f'{int(s/60)}min {s%60}sec'
    else:
        label = f'{int(s/3600)}hr {int((s%3600)/60)}min {(s%3600)%60}sec'
    return label