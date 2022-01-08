''' Draw function that takes in a goposition object and outputs a jpg image.
'''

from PIL import Image, ImageDraw, ImageFont
from goposition import goPosition

BLACK, WHITE = (0, 0, 0), (255, 255, 255)  # Colors
LATO = r"C:\Users\Ryan\AppData\Local\Microsoft\Windows\Fonts\Lato-Regular.ttf"
XFONT = r"C:\Users\Ryan\AppData\Local\Microsoft\Windows\Fonts\DejaVuSans.ttf"


def board(idraw, mode, S, board_size=19):
    ''' Draws the board edges and star points according to the board_size.
    S defines the spacing between the lines of the board.
    '''
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

        star_points = []  # All star point coordinates
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
        idraw.line((TL, BL, BR, TR, TL), fill=BLACK,
                   width=S//15)  # TL-BL, BL-BR
    elif nlines_x == board_size and nlines_y != board_size:
        idraw.line((TL, BL, BR, TR), fill=BLACK, width=S//15)  # TL-BL, BL-BR
    elif nlines_x != board_size and nlines_y == board_size:
        idraw.line((TR, TL, BL, BR), fill=BLACK, width=S//15)  # TL-BL, BL-BR
    else:
        idraw.line((TL, BL, BR), fill=BLACK, width=S//15)  # TL-BL, BL-BR

    return idraw


def Draw(position, fname="problem.jpg", draw_labels=True, mode_change=False,
            mode=(13, 11), S=400, quality=100):
    ''' Draws Go problem and saves as jpg. Assumes problem is already
        in the lower left corner.
        mode: tuple of int (x,y). x: # of x lines, y: # of y lines
    '''
    def draw_shapes(draw_obj, coord: str, shape: str):
        ''' Draws shapes on the board.
        '''
        x = BL[0] + S * ((ord(coord[0]) - 96) - 1)  # Transform coordinates
        y = BL[1] - S * (position.board_size - (ord(coord[1]) - 96))
        OL = S//15  # outline width for shapes
        if shape == "Circle":
            SIZE = S//4  # SIZE of the object
            xy = (x - SIZE, y - SIZE, x + SIZE, y + SIZE)
            # https://newbedev.com/draw-ellipse-in-python-pil-with-line-thickness
            xy2 = (xy[0] - OL, xy[1] - OL, xy[2] + OL, xy[3] + OL)
            if coord in position.bstones:  # draw in white color if over black stone
                draw_obj.ellipse(xy2, outline=WHITE, fill=WHITE)
                draw_obj.ellipse(xy, outline=WHITE, fill=BLACK)
            else:  # draw in black color
                draw_obj.ellipse(xy2, outline=BLACK, fill=BLACK)
                draw_obj.ellipse(xy, outline=BLACK, fill=WHITE)
        elif shape == "Square":
            SIZE = S//5  # SIZE of the object
            xy = (x - SIZE, y - SIZE, x + SIZE, y + SIZE)
            xy2 = (xy[0] - OL, xy[1] - OL, xy[2] + OL, xy[3] + OL)
            if coord in position.bstones:  # draw in white color if over black stone
                draw_obj.rectangle(xy2, outline=WHITE, fill=WHITE)
                draw_obj.rectangle(xy, outline=WHITE, fill=BLACK)
            else:  # draw in black color
                draw_obj.rectangle(xy2, outline=BLACK, fill=BLACK)
                draw_obj.rectangle(xy, outline=BLACK, fill=WHITE)
        elif shape == "Triangle":
            y -= S//30
            SIZE = S//5  # SIZE of the object
            xy = ((x, y-SIZE), (x-SIZE-SIZE//10, y+SIZE),
                (x+SIZE+SIZE//10, y+SIZE))
            xy2 = ((x, y-SIZE-OL*2), (x-SIZE-OL*2, y+SIZE+OL),
                (x+SIZE+OL*2, y+SIZE+OL))
            if coord in position.bstones:  # draw in white color if over black stone
                draw_obj.polygon(xy2, outline=WHITE, fill=WHITE)
                draw_obj.polygon(xy, outline=WHITE, fill=BLACK)
            else:  # draw in black color
                draw_obj.polygon(xy2, outline=BLACK, fill=BLACK)
                draw_obj.polygon(xy, outline=BLACK, fill=WHITE)
        return


    def draw_stones(draw_obj, coord: str, color, text=None):
        '''Draws one stone of color. If text, put text on top of stone. '''
        x = BL[0] + S * ((ord(coord[0]) - 96) - 1)  # Transform coordinates
        y = BL[1] - S * (position.board_size-(ord(coord[1]) - 96))
        OS = S//80  # offset to make the stone a bit smaller than the grid spacing
        draw_obj.ellipse((x-S//2+OS, y-S//2+OS, x+S//2-OS, y+S//2-OS),
                        fill=color, outline=BLACK, width=S//20)
        return


    def draw_text(draw_obj, coord: str, text, scale=1, FONT=LATO):
        ''' Draws text on the board.
        '''
        x = BL[0] + S * ((ord(coord[0]) - 96) - 1)  # Transform coordinates
        y = BL[1] - S * (position.board_size - (ord(coord[1]) - 96))

        # scale down longer text
        tsize = int(S * scale * 4 // 5 * (6 - len(str(text))) // 5)
        font = ImageFont.truetype(FONT, tsize)
        w, h = font.getsize(text)
        if coord not in position.bstones and coord not in position.wstones:
            draw_obj.rectangle((x-w/2, y-h/2, x+w/2, y+h/2),
                            fill=WHITE, outline=WHITE)
        if coord in position.bstones:  # draw in white color if over black stone
            draw_obj.text((x, y), text, fill=WHITE, anchor="mm", font=font)
        else:  # draw in black color
            draw_obj.text((x, y), text, fill=BLACK, anchor="mm", font=font)
        return

    if mode_change:  # if problem is bigger, image size also increases
        problem_xy = position.extent()
        nlines_x = max(mode[0], problem_xy[0]+2)
        nlines_y = max(mode[1], problem_xy[1]+2)
    else:
        nlines_x, nlines_y = mode[0], mode[1]
    # constrain the lines to maximum board size
    nlines_x = min(nlines_x, position.board_size)
    nlines_y = min(nlines_y, position.board_size)
    mode = (nlines_x, nlines_y)

    IM_SIZE = (nlines_x * S + S, nlines_y * S + S)  # Pixels of image

    # Define points Top Left, Bottom Left, Bottom Right, Top Right
    TL, BL = (S, S), (S, IM_SIZE[1] - S)
    BR, TR = (IM_SIZE[0] - S, IM_SIZE[1] - S), (IM_SIZE[0] - S, S)

    # Initialize image
    im = Image.new('RGB', IM_SIZE, WHITE)
    idraw = ImageDraw.Draw(im)

    # Draw board
    idraw = board(idraw, mode, S)

    # Draw stones
    if position.bstones:
        for stone in position.bstones:
            draw_stones(idraw, stone, BLACK)
    if position.wstones:
        for stone in position.wstones:
            draw_stones(idraw, stone, WHITE)

    # Draw labels and shapes
    if draw_labels:
        for coord, label in position.labels.items():
            if label in ["TR", "CR", "SQ"]:
                draw_shapes(idraw, coord, shape=goPosition.valid_labels[label])
            elif label == "MA":
                draw_text(idraw, coord, text=u"\u2715", FONT=XFONT, scale=1.2)
            else: # number or label
                draw_text(idraw, coord, text=label)

    # crop white space on borders and save image
    im = im.crop(box=(S//2 - S//50, S//2 - S//50,
                    IM_SIZE[0] - S//2 + S//50, IM_SIZE[1] - S//2 + S//50))
    im = im.resize((IM_SIZE[0] // 8, IM_SIZE[1] //
                    8), resample=Image.ANTIALIAS)
    im.save(fname, quality=quality)
    return
