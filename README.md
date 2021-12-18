# sgf_artist
Draw Go stones and labels using the Python Image Library.

Run **textbook_artist.py** on one SGF branch. Modify **file_artist.py** or **folder_artist.py** to run on whole file. See artist_test for example.

## Scripts
goposition.py: defines the class used to store each branch that is read from an SGF file.    
draw.py: defines the Draw function that draws using PIL.  
draw_one.py: Test code that reads artist_test.sgf and draws the branch as an image.  
folder_artist.py: sample script to draw a folder of SGF files.

## Changelog
- 12/18
	- Modified to minimize dependencies and simplified read and parse code