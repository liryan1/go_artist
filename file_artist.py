from group_artist import Collection
import os

path_to_file = '/Users/ryan/Desktop/Go/NYIG Books/Problems pdf & sgf/must_know_corner_life_and_death.sgf'
out_dir = '/Users/ryan/Desktop/jpg'
os.makedirs(out_dir, exist_ok=True)

Branches = Collection.from_sgf(path_to_file)
Branches.draw(mode=(13,11), fh=f"{out_dir}/", rotate=False, mode_change=False)