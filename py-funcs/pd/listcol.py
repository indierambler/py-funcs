# Import dependencies
import numpy as np
import pandas as pd

# List column functions
def search(vals, series):
    """Search a column of lists for each value in an input list and return all indices where it was found"""
    indices = []
    for val in vals:
        indices.extend([i for i,x in series.iteritems() if val in x])
    return list(set(indices))


def get_df_without_vals(vals, search_col, df):
    """Return a subset of 'df' where none of the 'vals' are contained in the 'search_col'"""
    indices = search(vals, df[search_col])
    return df[~df.index.isin(indices)]


def get_df_with_vals(vals, search_col, df):
    """Return a subset of 'df' with only rows where at least one of the 'vals' are contained in the 'search_col'"""
    indices = search(vals, df[search_col])
    return df[df.index.isin(indices)]


def value_counts(series):
    """Get the value counts of each value in a column of lists"""
    s = series.explode(ignore_index=True)
    return s.value_counts()


def unique(series):
    """Get all the unique values in a column of lists"""
    s = series.explode(ignore_index=True)
    return list(s.dropna().unique())


def exclusive_members(vals, series):
    """Return the indices of each 'val' in the 'series' that does not also include another 'val'"""
    while np.nan in vals:
        vals.remove(np.nan)
    all_indices = {val: search([val], series) for val in vals}
    excl_mem = {}
    for k1, v1 in all_indices.items():
        excl_mem[k1] = v1[:]  # make a copy of the original indices
        for k2, v2 in all_indices.items():
            if k1 != k2:
                #print(f'Before - k1 "{k1}" len: {len(excl_mem[k1])} | k2 "{k2}" len: {len(all_indices[k2])}')  # debug
                excl_mem[k1] = list(set(excl_mem[k1]).difference(v2))
                #print(f'After - k1 "{k1}" len: {len(excl_mem[k1])} | k2 "{k2}" len: {len(all_indices[k2])}')  # debug
    return excl_mem


def exclusive_counts(vals, series):
    members = exclusive_members(vals, series)
    members = {k: len(v) for k,v in members.items()}
    sorted_keys = sorted(members, key=members.get, reverse=True)
    for k in sorted_keys:
        print(f'{k}: {members[k]}')


def replace(old, new, series, *args, **kwargs):
    """Replace a single value in each row of a column of list values (may not replace NaN)"""
    s = pd.Series(
        [
            [new if x==old else x for x in row] 
            if isinstance(row, list) else row 
            for row in series
        ], 
        index=series.index)
    return s


def remove(val, series, *args, **kwargs):
    """Remove a specific value in each row of a column of list values (may not remove NaN)"""
    s = []
    for idx, lst in series.iteritems():
        while val in lst:
            lst.remove(val)
        s.append(lst)
    s = pd.Series(s, index=series.index)
    return s