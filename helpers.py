import re


def get_str(text, key):
    ''' empty list
    '''
    out = ''
    s = key + r'(\[[a-z]{2}\])+([A-Z]|;|\))'
    patern = re.compile(s)
    match = patern.finditer(text)
    for i in match:
        out += i.group()[3:-2]
    if out:
        return out.split('][')
    return []


def get_label(text, key):
    ''' Get number and letter labels in a SGF format string.
    returns a dictionary of coord: number or letter
    '''
    l = []
    if key == 'N':
        s = r'\[[a-z]{2}:\d+\]'
    elif key == 'L':
        s = r'\[[a-z]{2}:[A-Z]{1}\]'
    patern = re.compile(s)
    match = patern.finditer(text)
    for i in match:
        l.append(i.group()[1:-1])
    d = {}
    for i in l:
        a = i.split(':')
        d[a[0]] = a[1]
    return d


def get_LB(input_labels):
    valid_labels = {'TR': 'Triangle', 'CR': 'Circle',
                    'SQ': 'Square', 'MA': 'X', 'L': 'Letter', 'N': 'Number'}
    new_dict = {}  # coord: label type
    for l in valid_labels.keys():
        if l in ["L", "N"]:
            coords = get_label(input_labels, l)
            new_dict.update(coords)
        else:
            coords = get_str(input_labels, l)
            for c in coords:
                new_dict[c] = l
    return new_dict
