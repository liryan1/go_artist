import re
from artist_helper import *
from textbook_artist import Branch

class Collection:
	def __init__(self, branches=[]):
		self.branches = branches

	@classmethod
	def from_sgf(cls, path_to_file):
		# Read SGF and get branches
		with open(path_to_file) as f:
			lines = f.read().split('(;')
		branches = [lines[1]] if len(lines) == 2 else lines[2:]

		# get board size from header
		try:
			board_size = int(re.findall(r'SZ(\[(.*?)\])', lines[1])[-1][-1])
		except Exception:
			print("Cannot find board size (SZ) in SGF... Going with 19x19")
			board_size = 19

		return cls([Branch.from_string(branch, BS=board_size) for branch in branches])

	@classmethod
	def from_json(cls, path_to_file):
		return cls()

	def draw(self, fh, rotate, **kwargs):
		''' loop through and draw each branch
		'''
		for i, branch in enumerate(self.branches):
			if rotate:
				branch.to_lower_left()
			if isinstance(fh, str):
				branch.draw(f"{fh}/{i+1}.jpg", **kwargs)
			# elif isinstance(fh, list):
			# 	branch.draw(f"{fh}/{i+1}.jpg", **kwargs)

if __name__ == '__main__':
	path_to_file = 'artist_test.sgf'
	Branches = Collection.from_sgf(path_to_file)
	Branches.draw(mode=(13,11), fh=f".", rotate=False, mode_change=False)
