# sgf_artist
Draw Go stones and labels using the Python Image Library.

Sample image  
<img src="test.jpg" alt="drawing" width="200"/>

## Scripts
goposition.py: defines the class used to store each branch that is read from an SGF file.    
draw.py: defines the Draw function that draws using PIL.  
draw_one.py: Test code that reads artist_test.sgf and draws the branch as an image.  
folder_artist.py: sample script to draw a folder of SGF files.

## Changelog
- 12/18
	- Modified to minimize dependencies and simplified read and parse code
