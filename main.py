from goposition import goPosition
from draw import Draw
import os
current_dir = os.path.dirname(os.path.realpath(__file__))

# ----------- Basic test of SGF framework ----------
if __name__ == "__main__":
	with open(fr'{current_dir}\artist_test.sgf', 'r') as f:
	    text = f.read()
	P = goPosition.from_string(text, comment=True)
	print(P)
	Draw(P, fname=fr"{current_dir}\test.jpg", mode=(19,13))