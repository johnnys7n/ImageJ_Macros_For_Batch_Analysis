# importing the IJ translator module
from ij import IJ
import os

# assigning directory path to 'dir' variable
dir = IJ.getDir('Choose Directory')

# getting the list of files within the directory
dir_list = os.listdir(dir)


for file in files_list:
	current_file = dir + file
	IJ.run("Bio-Formats Importer", "open=["+current_file+"] color_mode=Default view=Hyperstack stack_order=XYCZT")
	IJ.run("Z Project...", "projection=[Max Intensity]")
	IJ.run("Split Channels")
	
	IJ.run("Analyze Particles...", "size=5-Infinity summarize")
