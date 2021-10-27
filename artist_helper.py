import re

def board(idraw, mode, S, board_size=19):
    BLACK = (0, 0, 0)
    def get_star_points():
        '''Returns coordinates of where star points should be.
        x, y are the image coordinates (starts lower left corner).
        '''
        x, y = BL[0], BL[1]

        # Define start, step to accommodate smaller board sizes
        start, step = 4, 6
        if board_size == 13:
            step = 3
        elif board_size == 9:
            start = 3
            step = 3

        star_points = [] # All star point coordinates
        for i in range(start, nlines_x, step):
            for j in range(start, nlines_y, step):
                if nlines_x >= i and nlines_y >= j:  # lower side
                    star_points.append((x + S * (i-1), y - S * (j-1)))
        return star_points

    nlines_x, nlines_y = mode
    IM_SIZE = (nlines_x * S + S, nlines_y * S + S)  # Pixels of image
    # Define points Top Left, Bottom Left, Bottom Right, Top Right
    TL, BL = (S, S), (S, IM_SIZE[1] - S)
    BR, TR = (IM_SIZE[0] - S, IM_SIZE[1] - S), (IM_SIZE[0] - S, S)

    # Draw vertical lines
    for i in range(1, nlines_x - 1):
        idraw.line((TL[0] + S * i, TL[1], BL[0] + S * i, BL[1]),
                   fill=BLACK, width=S//30)

    # Draw horizontal lines
    for i in range(1, nlines_y - 1):
        idraw.line((TL[0], TL[1] + S * i, TR[0], TR[1] + S * i),
                   fill=BLACK, width=S//30)

    # Draw star points on the board
    star_points = get_star_points()
    for p in star_points:
        idraw.ellipse((p[0]-S//10, p[1]-S//10, p[0]+S//10, p[1]+S//10),
                      fill=BLACK, outline=BLACK, width=1)

    # Draw board edges
    if nlines_x == board_size and nlines_y == board_size:
        idraw.line((TL, BL, BR, TR, TL), fill=BLACK, width=S//15)  # TL-BL, BL-BR
    elif nlines_x == board_size and nlines_y != board_size:
        idraw.line((TL, BL, BR, TR), fill=BLACK, width=S//15)  # TL-BL, BL-BR
    elif nlines_x != board_size and nlines_y == board_size:
        idraw.line((TR, TL, BL, BR), fill=BLACK, width=S//15)  # TL-BL, BL-BR
    else:
        idraw.line((TL, BL, BR), fill=BLACK, width=S//15)  # TL-BL, BL-BR

    return idraw

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
    ''' Get labels in a SGF format string.
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
        d[a[1]] = a[0]
    return d


def horizontal_flip(C, bs=19):
    '''Flip coordinates horizontally.'''
    if isinstance(C,list):
        if C:
            return [chr(bs - (ord(c[0])-96)+97) + c[1] for c in C]
        return []
    elif isinstance(C, dict):
        if C:
            for k, c in C.items():
                C[k] = chr(bs - (ord(c[0])-96)+97) + c[1]
            return C
        return {}

def vertical_flip(C, bs=19):
    '''Flip coordinates vertically.'''
    if isinstance(C,list):
        if C:
            return [c[0] + chr(bs - (ord(c[1])-96) + 97) for c in C]
        return []
    elif isinstance(C, dict): # deals with dictionary labels number and letter
        if C:
            for k, c in C.items():
                C[k] = c[0] + chr(bs - (ord(c[1])-96) + 97)
            return C
        return {}

def reverse_xy(C):
    '''Swap the x and y coordinates'''
    if isinstance(C,list):
        if C:
            return [s[::-1] for s in C]
        return []
    elif isinstance(C, dict): # deals with dictionary labels number and letter
        if C:
            for k, s in C.items():
                C[k] = s[::-1]
            return C
        return {}

def in_lower_left(C):
    ''' Checks if the coordinates C is in the lower left (True) or in another
    quadrant (False)'''
    hor, ver = 0, 0
    for i, v in enumerate(C):
        if ord(v[0]) - 97 <= 9:
            hor += 1
        if ord(v[1]) - 97 >= 9:
            ver += 1
    move_left = True if (hor > len(C) // 2) else False
    move_down = True if (ver > len(C) // 2) else False
    if move_left == True and move_down == True:
        return True
    return False

def in_upper_right(C):
    ''' Checks if the coordinates C is in the upper right (True) or in another
    quadrant (False)'''
    hor, ver = 0, 0
    for i, v in enumerate(C):
        if ord(v[0]) - 97 >= 9:
            hor += 1
        if ord(v[1]) - 97 <= 9:
            ver += 1
    move_left = True if (hor > len(C) // 2) else False
    move_down = True if (ver > len(C) // 2) else False
    if move_left == True and move_down == True:
        return True
    return False