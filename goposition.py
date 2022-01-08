import re
from helpers import get_str, get_LB


class goPosition:
    '''Stores a board position'''
    valid_labels = {'TR': 'Triangle', 'CR': 'Circle',
                    'SQ': 'Square', 'MA': 'X', 'L': 'Letter', 'N': 'Number'}

    def __init__(self, bstones=None, wstones=None,
                 comment=None, board_size=19, labels=None) -> None:
        ''' Problems are always black to play.
        bstones (list of str): initial black stones (SGF coordinates)
        wstones (list of str): initial white stones (SGF coordinates)
        board_size (int): size of the board for the problem
        '''
        self.comment = comment
        self.bstones = bstones
        self.wstones = wstones
        self.board_size = board_size
        self.labels = labels

    def __repr__(self) -> str:
        ''' convert Go Problem into string writable to SGF
        '''
        black = "AB" + "".join([f"[{c}]" for c in self.bstones])
        white = "AW" + "".join([f"[{c}]" for c in self.wstones])
        comment = f"C[{self.comment}]" if self.comment else ""
        # parse labels back to SGF format
        label = ""
        if self.labels:
            label += "\n"
            grouped = {}
            # Change to label: [list of coords]
            for key, value in self.labels.items():
                if value.isnumeric() or len(value) < 2:  # letter and number labels
                    x = grouped.get("LB", [])
                    x.append(f"{key}:{value}")
                    grouped["LB"] = x
                else:  # https://stackoverflow.com/questions/15751979
                    grouped.setdefault(value, set()).add(key)
            for key, value in grouped.items():
                label += (key + "".join(f"[{c}]" for c in value))
        return f'\n(;{black}{white}{label}{comment})\n'

    @classmethod
    def from_string(cls, text, size: int=19, comment: bool=False):
        ''' Constructs the GoPosition class using an SGF string
        '''
        BS = get_str(text, "AB")
        WS = get_str(text, "AW")
        C = re.findall(r'C\[(.+?)\]', text, re.DOTALL)[0] if comment else None
        LB = get_LB(text)
        SIZE = size
        return cls(BS, WS, C, SIZE, LB)