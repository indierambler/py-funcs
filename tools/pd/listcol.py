# Import dependencies
import numpy as np
import pandas as pd

# Functions
def pack(df):
    pass


def unpack(df):
    def xform(val):
        if isinstance(val, str) and val[0] == '[' and val[-1] == ']':
            return eval(val)
        elif isinstance(val, np.ndarray):
            return list(val)
        else:
            return val
    return df.applymap(xform)


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


def value_counts(series, val=None):
    """Get the value counts of each value in a column of lists"""
    s = series.explode(ignore_index=True)
    if val:
        if val in s.value_counts():
            return s.value_counts()[val]
        else:
            return 0
    else:
        return s.value_counts()


def value_pcts(series, listcol=False):
    """Get the value counts in a series as a percentage distribution"""
    length = len(series)
    if listcol:
        pcts = {k: round(v/length, 3) for k,v in dict(value_counts(series)).items()}
    else:
        pcts = {k: round(v/length, 3) for k,v in dict(series.value_counts()).items()}
    return pcts


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
    #sorted_keys = sorted(members, key=members.get, reverse=True)
    #for k in sorted_keys:
    #    print(f'{k}: {members[k]}')
    return pd.DataFrame(members, index=['exclusives']).T


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