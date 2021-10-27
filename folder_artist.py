from textbook_artist import Branch
import os

BOOK = "Book 4"
overwrite = True

# Define input and output directories
out_dir = f"/Users/ryan/Desktop/{BOOK} jpg"
folder_name = f'/Users/ryan/Dropbox/2021 Textbook Team/SGF Files/{BOOK}'

# Get list of files to draw
folder_path = os.listdir(folder_name)

# Create directory for Book
os.makedirs(out_dir,exist_ok=True)

# Make sure all files are SGF files
folder_path = [f for f in folder_path if ".sgf" in f]
#print(folder_path)


for file in folder_path:
    if file != 'Book4_Chapter2_10x12.sgf':
        continue
    fname = file.strip(".sgf")
    # Create a subdirectory to hold jpgs
    file_dir = f"{out_dir}/{fname}"
    if os.path.isdir(file_dir) and (not overwrite):
        continue
    else:
        os.makedirs(file_dir,exist_ok=True)

    # Read SGF and get branches
    with open(f'{folder_name}/{file}','r') as f:
        l = f.read()
    l = l.split('(;')[1:]
    head = l[0]
    text = l[1:]

    # Define size of picture to draw and the board size
    size = fname.split('_')[-1].split('x')
    size = (int(size[1]), int(size[0]))
    if size == (13, 13):
        board_size = 13
    elif size == (9, 9):
        board_size = 9
    else:
        board_size = 19

    # If 19x19, don't add one more, if less, add one more line
    if size[0] < board_size:
        size = (size[0] + 1, size[1])

    if size[1] < board_size:
        size = (size[0], size[1] + 1)

    # add page numbers to each file
    for i, v in enumerate(text):
        obj = Branch.from_string(v)
        obj.draw(fname=f'{file_dir}/{i+1}.jpg', quality=60,
                 mode=size, mode_change=False)
