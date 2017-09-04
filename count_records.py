import os, sys

def count_lines(data_path):

	countty = 0
	files_list = os.listdir(data_path)
	for file in files_list:
		with open(os.path.join(data_path, file), 'r') as f:
			countty = countty + len(f.readlines())
	print countty


if __name__ == '__main__':
	path = sys.argv[1]
	count_lines(path)