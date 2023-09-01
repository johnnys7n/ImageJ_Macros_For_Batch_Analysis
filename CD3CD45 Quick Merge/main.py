# importing useful libraries
import os
from ij import IJ

def main():
	dir = IJ.getDir('Select the Folder') #changes dir to the folder selected
	files_list = os.listdir(dir) # outputs the list of files in this folder

	new_files_list = select_channels(files_list)
	
	print(new_files_list)
	

def select_channels(files_list):
	'''
	Function that creates a new list of files inside the selected directory that is only 488 ORG and 555 ORG
	'''
	files_list = []
	for file in files_list:
		if 'DAPI' not in file and 'ORG' in file:
			files_list.append(file)
	return files_list
			

if __name__ == '__main__':
	main()