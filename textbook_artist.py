import os
from PIL import Image, ImageDraw, ImageFont
from artist_helper import *

class Branch:
    stuff = ["bstones","wstones","triangles","circles","squares","x",
             "numbers", "letters"]
    def __init__(self, bstones=None, wstones=None,tr=None, cr=None, 
                 sq=None, ma=None, letters=None, nums=None, board_size=19):
        # Read in the LB part of the SGF
        self.bstones = bstones
        self.wstones = wstones
        self.triangles = tr
        self.circles = cr
        self.squares = sq
        self.x = ma
        self.numbers = nums
        self.letters = letters
        self.board_size = board_size

    def __repr__(self) -> str:
        l = [f'Black Stones: {self.bstones}', f'White Stones: {self.wstones}',
             f'Triangles: {self.triangles}', f'Circles: {self.circles}',
             f'Square: {self.squares}', f'X: {self.x}',
             f'Letters: {self.letters}', f'Numbers: {self.numbers}']
        return '\n'.join(l)

    def all_coords(self):
        coords = []
        for attr in Branch.stuff:
            data = getattr(self, attr)
            if isinstance(data, list):
                coords += data
            elif isinstance(data, dict):
                coords += list(data.values())
        return coords


    def to_upper_right(self):
        ''' Rotates the problem to the upper right corner.
        In any other quadrant than 1: vertical_flip, reverse_xy, horizontal_flip
        '''
        quadrant = in_upper_right(self.all_coords())
        if not quadrant:
            for attr in Branch.stuff:
                setattr(self, attr, vertical_flip(getattr(self, attr)))
                setattr(self, attr, reverse_xy(getattr(self, attr)))
                setattr(self, attr, horizontal_flip(getattr(self, attr)))

    def to_lower_left(self):
        ''' Rotates the problem to the lower left corner.
        get it to the upper right, then do one vertical followed by horizontal flip.
        '''
        self.to_upper_right()
        for attr in Branch.stuff:
            setattr(self, attr, vertical_flip(getattr(self, attr)))
            setattr(self, attr, horizontal_flip(getattr(self, attr)))        

    def extent(self):
        if not in_lower_left(self.all_coords()):
            self.to_lower_left()
        xmax, ymax = 0, 0
        for c in self.all_coords():
            x, y = ord(c[0]) - 97 + 1, self.board_size - (ord(c[1]) - 97)
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
        return (xmax, ymax)

    @classmethod
    def from_string(cls, text, BS=19):
        # update it so it can read all the labels
        # assign everything after LB to label
        bstones = get_str(text, 'AB')
        wstones = get_str(text, 'AW')
        tr = get_str(text, 'TR')
        cr = get_str(text, 'CR')
        sq = get_str(text, 'SQ')
        ma = get_str(text, 'MA')
        letters = get_label(text, 'L')
        nums = get_label(text, 'N')
        return cls(bstones,wstones,tr,cr,sq,ma,letters,nums,board_size=BS)

    def draw(self, fname="problem.jpg", draw_labels=True, mode_change=False,
             mode=(13, 11), S=400, quality=60):
        ''' Draws Go problem and saves as jpg. Assumes problem is already
            in the lower left corner.
            mode: tuple of int (x,y). x: # of x lines, y: # of y lines
        '''
        BLACK, WHITE = (0, 0, 0), (255, 255, 255)  # Colors
        def draw_stones(draw_obj, coord: str, color, text=None):
            '''Draws one stone of color. If text, put text on top of stone. '''
            x = BL[0] + S * ((ord(coord[0]) - 96) - 1)  # Transform coordinates
            y = BL[1] - S * (self.board_size-(ord(coord[1]) - 96))
            OS = S//80 # offset to make the stone a bit smaller than the grid spacing
            draw_obj.ellipse((x-S//2+OS, y-S//2+OS,x+S//2-OS, y+S//2-OS),
                             fill=color, outline=BLACK, width=S//30)
            return

        def draw_text(draw_obj, coord: str, text: str, scale=1,
                        FONT="Lato-Regular"):
            ''' Draws text on the board.
            '''
            x = BL[0] + S * ((ord(coord[0]) - 96) - 1)  # Transform coordinates
            y = BL[1] - S * (self.board_size - (ord(coord[1]) - 96))

            # scale down longer text
            tsize = int(S * scale * 2 // 3 * (6 - len(str(text))) // 5)
            font = ImageFont.truetype(FONT, tsize)
            w, h = font.getsize(text)
            if coord not in self.bstones and coord not in self.wstones:
                draw_obj.rectangle((x-w/2, y-h/2, x+w/2, y+h/2),
                                    fill=WHITE, outline=WHITE)
            if coord in self.bstones: # draw in white color if over black stone
                draw_obj.text((x, y), text, fill=WHITE, anchor="mm", font=font)
            else: # draw in black color
                draw_obj.text((x, y), text, fill=BLACK, anchor="mm", font=font)
            return

        def draw_shapes(draw_obj, coord: str, shape: str):
            ''' Draws shapes on the board.
            '''
            x = BL[0] + S * ((ord(coord[0]) - 96) - 1)  # Transform coordinates
            y = BL[1] - S * (self.board_size - (ord(coord[1]) - 96))
            OL = S//20 # outline width for shapes
            if shape == "circle":
                SIZE = S//5 # SIZE of the object
                xy = (x - SIZE, y - SIZE, x + SIZE, y + SIZE)
                # https://newbedev.com/draw-ellipse-in-python-pil-with-line-thickness
                xy2 = (xy[0] - OL, xy[1] - OL, xy[2] + OL, xy[3] + OL)
                if coord in self.bstones:  # draw in white color if over black stone
                    draw_obj.ellipse(xy2, outline=WHITE, fill=WHITE)
                    draw_obj.ellipse(xy, outline=WHITE, fill=BLACK)
                else:  # draw in black color
                    draw_obj.ellipse(xy2, outline=BLACK, fill=BLACK)
                    draw_obj.ellipse(xy, outline=BLACK, fill=WHITE)
            elif shape == "square":
                SIZE = S//6  # SIZE of the object
                xy = (x - SIZE, y - SIZE, x + SIZE, y + SIZE)
                xy2 = (xy[0] - OL, xy[1] - OL, xy[2] + OL, xy[3] + OL)
                if coord in self.bstones:  # draw in white color if over black stone
                    draw_obj.rectangle(xy2, outline=WHITE, fill=WHITE)
                    draw_obj.rectangle(xy, outline=WHITE, fill=BLACK)
                else:  # draw in black color
                    draw_obj.rectangle(xy2, outline=BLACK, fill=BLACK)
                    draw_obj.rectangle(xy, outline=BLACK, fill=WHITE)
            elif shape == "triangle":
                SIZE = S//6  # SIZE of the object
                xy = ((x, y-SIZE), (x-SIZE-SIZE//10, y+SIZE),
                      (x+SIZE+SIZE//10, y+SIZE))
                xy2 = ((x, y-SIZE-OL*2), (x-SIZE-OL*2, y+SIZE+OL), (x+SIZE+OL*2, y+SIZE+OL))
                if coord in self.bstones:  # draw in white color if over black stone
                    draw_obj.polygon(xy2, outline=WHITE, fill=WHITE)
                    draw_obj.polygon(xy, outline=WHITE, fill=BLACK)
                else:  # draw in black color
                    draw_obj.polygon(xy2, outline=BLACK, fill=BLACK)
                    draw_obj.polygon(xy, outline=BLACK, fill=WHITE)
            return

        if mode_change: # if problem is bigger, image size also increases
            problem_xy = self.extent()
            nlines_x = max(mode[0], problem_xy[0]+2)
            nlines_y = max(mode[1], problem_xy[1]+2)
        else:
            nlines_x, nlines_y = mode[0], mode[1]
        # constrain the lines to maximum board size
        nlines_x = min(nlines_x, self.board_size)
        nlines_y = min(nlines_y, self.board_size)
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
        if self.bstones:
            for stone in self.bstones:
                draw_stones(idraw, stone, BLACK)
        if self.wstones:
            for stone in self.wstones:
                draw_stones(idraw, stone, WHITE)

        # Draw labels and shapes
        if draw_labels: 
            for i in self.numbers.keys(): # draw numbers
                draw_text(idraw, self.numbers[i], text=str(i))
            for i in self.letters.keys(): # draw letters
                draw_text(idraw, self.letters[i], text=str(i))
            for i in self.x: # draw x
                draw_text(idraw, i, text=u"\u2715", FONT="DejaVuSans",scale=1.2)
            for i in self.circles:  # draw circles
                draw_shapes(idraw, i, shape="circle")
            for i in self.squares:  # draw circles
                draw_shapes(idraw, i, shape="square")
            for i in self.triangles:  # draw circles
                draw_shapes(idraw, i, shape="triangle")

        # crop white space on borders and save image
        im = im.crop(box=(S//2 - S//50, S//2 - S//50,
                     IM_SIZE[0] - S//2 + S//50, IM_SIZE[1] - S//2 + S//50))
        im = im.resize((IM_SIZE[0] // 8, IM_SIZE[1] // 8), resample=Image.ANTIALIAS)
        im.save(fname, quality=quality)
        return

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{current_dir}/artist_test.sgf', 'r') as f:
        l = f.read()
    B = Branch.from_string(l)
    print(B)
    #print(B.extent())
    #B.to_lower_left()
    B.draw(mode=(13,11), mode_change=True, fname=f"{current_dir}/artist_test.jpg")