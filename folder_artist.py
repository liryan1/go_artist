from goposition import GoPosition
from draw import Draw
import os

FOLDER = "Go_files"
size = (13, 11)
overwrite = False

# Define input and output directories
out_dir = r"C:\Go_images"
folder_name = rf'C:\Documents\{FOLDER}'

# Get list of files to draw
folder_path = os.listdir(folder_name)

# Create directory for Book
os.makedirs(out_dir,exist_ok=True)

# Make sure all files are SGF files
folder_path = [f for f in folder_path if ".sgf" in f]
#print(folder_path)


for file in folder_path:
    fname = file.strip(".sgf")
    # Create a subdirectory to hold jpgs
    file_dir = fr"{out_dir}\{fname}"
    if os.path.isdir(file_dir) and (not overwrite):
        print(f"{file_dir} already exists, skipping...")
        continue
    else:
        os.makedirs(file_dir,exist_ok=True)

    # Read SGF and get branches
    with open(f'{folder_name}/{file}','r') as f:
        l = f.read()
    l = l.split('(;')[1:]
    text = l[1:]

    # add page numbers to each file
    for i, v in enumerate(text):
        obj = GoPosition.from_string(v, size=19)
        Draw(obj, fname=fr'{file_dir}\{i+1}.jpg', quality=80, mode=size)
    print(f"Done {file}")