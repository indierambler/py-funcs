# Import dependencies
import pandas as pd


# List column functions
def search(vals, series):
    """Search a column of lists for each value in an input list and return all indices where it was found"""
    indices = []
    longest = len(max(series, key=len))  # get the length of longest list in col
    for a in range(longest):  # iterate the list members vertically
        s = series.str[a]  # get series of "a" values in list (nonexistent filled with nan)
        indices.extend([n for n,x in zip(s.index,s) if x in vals])  # get indices of the hits
    return list(set(indices))


def get_df_without_vals(vals, search_col, df):
    """Return a subset of 'df' where none of the 'vals' are contained in the 'search_col'"""
    indices = search(vals, df[search_col])
    return df[~df.index.isin(indices)]


def get_df_with_vals(vals, search_col, df):
    """Return a subset of 'df' with only rows where at least one of the 'vals' are contained in the 'search_col'"""
    indices = search(vals, df[search_col])
    return df[df.index.isin(indices)]


def value_counts(search_col, df):
    """Get the value counts of each value in a column of lists"""
    df1 = df.explode(search_col, ignore_index=True)
    return df1[search_col].value_counts()