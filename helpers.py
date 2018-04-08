def load_files(fname='usps.csv', output = 'dict'):
    """
    load abbreviation from file fname
    return dictionary {pattern : replacement}
    return list [list of items to remove from strings to avoid]
    """
    if output == "dict":
        df = pd.read_csv(fname, index_col='pattern')
        return df.to_dict()
    elif output == "list":
        df = pd.read_csv(fname, header=0)
        col = df.columns[0]
        return df[col].tolist()


def handle_strings(x, exclude=set(string.punctuation)):
    """
    Helper function to make string all caps and remove punctuation.
    
    x: any string
    """
    
    x = x.replace('-', ' ')
    x = ''.join(ch for ch in x if ch not in exclude)
    return x

def handle_words(x, exclude=[], case = 'u'):
    ''' Helper function to remove words from match comparisons that don't have signal but are noisy 
    
        x: any string
        exclude = list of words that are removed from comparison strings for matching.
    '''
    case = case[0].lower()
    exclude = [word.lower() for word in exclude]
    x = x.lower().split(" ")
    x = ' '.join(word for word in x if word not in exclude)
    if case == 'u':
        if type(x) is str:
            x = x.upper()
        else:
            x = [word.upper() for word in x]
    return x


def normalizeText(inputValue, d={}, case='u'):
    '''
    if case=='l', returns lowercase
    if case=='u', returns uppercase
    else returns proper case
    d = dictionary to use for replacements
    '''
    
    case = case[0].lower()
    abbv = d
    words = inputValue.split()
    for i,word in enumerate(words):
        w = handle_strings(word.lower())
        rep = abbv[w] if w in abbv.keys() else handle_strings(words[i])
        words[i] = rep.upper() if case == 'u' else rep.lower() if case == 'l' else (rep[0].upper() + rep[1:])
    
    return ' '.join(words)

def norm_shorthand(inputValue, case = 'u', short_hand = []):
    ''' fixes cases when short-hand is used at the end of a string
    
     eg. "Prevost elementary" vs. "Prevost elementary school'''
    
    case = case[0].lower()
    words = inputValue.split()
    short_hand = ['elementary', 'middle', 'high', 'intermediate']
    if words[-1].lower() in short_hand:
        
        if case == 'l':
            words[-1] = words[-1].replace(words[-1], words[-1] + ' school').lower()
            
        else:
            words[-1] = words[-1].replace(words[-1], words[-1] + ' school').upper()
        
        
    return ' '.join(words)

