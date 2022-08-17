# Import dependencies
import numpy as np

# Functions for comparing strings directly
def levenshtein_dist(s, t):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indices of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    return distance[row][col]


def levenshtein_window(s, t):
    if len(s) <= len(t):
        short = s
        long = t
    else:
        short = t
        long = s

    min_lev = 1000000
    for i in range(0,len(long)-len(short)):
        lev = levenshtein_dist(short,long[i:i+len(short)])
        if lev < min_lev:
            min_lev = lev

    return min_lev


def compare(s, t, typo_threshold=2):
    if not s or not t:
        return False

    if len(s) <= len(t):
        short = s
        long = t
    else:
        short = t
        long = s

    min_len = len(short)
    #max_len = len(long)
    #diff_len = max_len - min_len

    if min_len <= 3:
        typo_threshold = 0
    elif min_len <= typo_threshold+3:
        typo_threshold = int(min_len/3)

    # if diff length > 3 * min length or threshold?
    # if diff_len <= typo_threshold:

    lev = levenshtein_dist(s,t)
    if lev <= typo_threshold:
        return True
    else:
        return False


def match_pct(s, t):
    if type(s) is not str or type(t) is not str or not s or not t:
        return 0.0

    # get the lev score of the match
    lev = levenshtein_dist(s,t)

    # determine the longer string
    if len(s) >= len(t):
        denom = len(s)
    else:
        denom = len(t)

    # TODO: give a score of how accurate the match is based on length of the strings

    return 1 - (lev / denom)


def best_match(targ, options=[], truncate=False):
    if truncate:
        targ = truncate(str(targ))
        options = [truncate(str(x)) for x in options]

    match_pcts = [match_pct(str(targ), str(x)) for x in options]
    try:
        top_match_idx = match_pcts.index(max(match_pcts))
        top_match = options[top_match_idx]
        return (targ, top_match)
    except:
        return (targ, None)


# Functions for cleaning and searching strings
def split_words(str_input):
    str_input = str_input.replace('_',' ')
    str_input = str_input.replace('/',' ')
    str_input = str_input.replace('-',' ')
    str_split = str_input.split()
    return str_split


def rmv_spaces(str_input):
    str_input = str_input.replace('_','')
    str_input = str_input.replace('-','')
    str_input = str_input.replace('/','')
    str_input = str_input.replace(' ','')
    return str_input


def rmv_special_char(str_input):
    str_input = str_input.replace('!','')
    str_input = str_input.replace('@','')
    str_input = str_input.replace('#','')
    str_input = str_input.replace('$','')
    str_input = str_input.replace('%','')
    str_input = str_input.replace('^','')
    str_input = str_input.replace('&','')
    str_input = str_input.replace('*','')
    str_input = str_input.replace('(','')
    str_input = str_input.replace(')','')
    #str_input = str_input.replace('_','')
    #str_input = str_input.replace('-','')
    str_input = str_input.replace('+','')
    str_input = str_input.replace('=','')
    str_input = str_input.replace('?','')
    #str_input = str_input.replace('/','')
    str_input = str_input.replace('|','')
    str_input = str_input.replace('~','')
    str_input = str_input.replace('.','')
    str_input = str_input.replace(',','')
    str_input = str_input.replace(';','')
    str_input = str_input.replace(':','')
    str_input = str_input.replace('<','')
    str_input = str_input.replace('>','')
    str_input = str_input.replace('{','')
    str_input = str_input.replace('}','')
    str_input = str_input.replace('[','')
    str_input = str_input.replace(']','')
    str_input = str_input.replace("'",'')
    str_input = str_input.replace('"','')
    # missing ` \ for now
    return str_input


def rmv_numbers(str_input):
    str_input = str_input.replace('1','')
    str_input = str_input.replace('2','')
    str_input = str_input.replace('3','')
    str_input = str_input.replace('4','')
    str_input = str_input.replace('5','')
    str_input = str_input.replace('6','')
    str_input = str_input.replace('7','')
    str_input = str_input.replace('8','')
    str_input = str_input.replace('9','')
    str_input = str_input.replace('0','')
    return str_input


def truncate(s):
    result = s.lower()
    result = rmv_special_char(result)
    result = rmv_spaces(result)
    return result


def clean(s):
    result = s.lower()
    result = result.replace('_',' ')
    result = result.replace('-',' ')
    result = result.replace('.','')
    result = result.replace(',','')
    result = result.replace('&','and')
    result = result.replace("'n'",'and')
    result = result.replace('"','')
    result = result.replace("'",'')
    result = result.replace('  ',' ')
    return result


def search(search_for, search_in, threshold=1.0, use_caps=False, use_spaces=False, use_spec_char=False, use_num=False):
    if not search_for or not search_in:
        return 0.0

    if not use_caps:  # convert everything to lowercase
        search_for = search_for.lower()
        search_in = search_in.lower()

    if not use_spec_char:  # remove special characters from string
        search_for = rmv_special_char(search_for)
        search_in = rmv_special_char(search_in)

    # convert separators to spaces and split words into list
    search_for_2 = split_words(search_for)
    search_in_2 = split_words(search_in)

    if not use_spaces:   # remove spaces from string
        search_for = search_for.replace(' ','')
        search_in = search_in.replace(' ','')

    if not use_num:  # remove numbers from string
        search_for = rmv_numbers(search_for)
        search_in = rmv_numbers(search_in)

    if search_for == '' or search_in == '':
        return 0.0
    
    if search_for in search_in:  # check if input is in search string
        return 1.0
    else:  # if not, calculate percentage match
        #char_ratio = len(search_for) / len(search_in)
        #word_ratio = len(search_for_2) / len(search_in_2)

        match_count = 0
        order_count = 0
        last_idx = 0

        for i in range(0,len(search_for_2)):  # for each word in the search text
            # Calc number of occurences of current search word in full search text
            # TODO: search word should be longer than 2-4 letters to use the  lev distance
            # TODO: smaller search strings match easier they need to be weighted
            occ_idxs_for = [x for x, y in enumerate(search_for_2) if compare(y,search_for_2[i])]
            #print(occ_idxs_for)
            #occ_idxs_for = [x for x, y in enumerate(search_for_2) if y == search_for_2[i]]
            total_occ_for = len(occ_idxs_for)
            this_occ_for = occ_idxs_for.index(i) # current iter of this word in search_for

            occ_idxs_in = [x for x, y in enumerate(search_in_2) if compare(search_for_2[i],y)]
            #print(occ_idxs_in)
            #occ_idxs_in = [x for x, y in enumerate(search_in_2) if y == search_for_2[i]]
            total_occ_in = len(occ_idxs_in)
            
            #print(f'a: {this_occ_for} <= {total_occ_in-1}')
            if this_occ_for <= total_occ_in-1 and total_occ_in > 0:  # this occurence exists in search_in
                this_occ_in = occ_idxs_in[this_occ_for]  # index of current iter of this word in search_in
                match_count += 1
                
                #print(f'b: {this_occ_in} > {last_idx}')
                if this_occ_in >= last_idx:
                    if this_occ_in-last_idx == 1 or last_idx == 0:
                        order_count += 1
                    else:
                        order_count += 0.5

                last_idx = this_occ_in

        match_pct = ((match_count + order_count) / (len(search_for_2) * 2))# * word_ratio
        return match_pct