# Next we import Java Classes into Jython.
# This is how we can acces the ImageJ API:
# https://imagej.nih.gov/ij/developer/api/allclasses-noframe.html
from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog, Roi, ImageRoi
from ij.process import AutoThresholder, ImageProcessor

# importing the os module to communicate with the local files
import os

# It's best practice to create a function that contains the code that is executed when running the script.
# This enables us to stop the script by just calling return.
def main():	
	# assigning directory path to 'dir' variable
	dir = IJ.getDir('Choose Directory')
	
	# getting the list of files within the directory
	dir_list = os.listdir(dir)

	preprocess_answer, channel_value = process_all_images_dialog()

	if preprocess_answer == True:
		#	creating a list of the folders inside the working directory
		if '.tif' not in dir_list[0]:
			dir_working = []
			for dirs in dir_list:	
				dir_working.append(dir + dirs)
	
		#	opening the files in the working directory
			

			for dir_wd in dir_working:
				print('currently processing' + dir_wd)
				files = os.listdir(dir_wd)
				a = 0
				file_list = []
				for file in files:
					if channel_value in file:
						file_path = str(dir_wd + "\\" + file)
						file_list.append(file_path)
						preprocess_image(file_path, channel_value)
						a += 1
				if a == 0:
					warning_message()
					
		else:
			b = 0
			for file in dir_list:
				if channel_value in file:
					print('currently processing' + file)
					file_path = str(dir + file)
					preprocess_image(file_path, channel_value)
#					create_selection_dialog(file_path)
					b += 1
			if b == 0:
				warning_message()

def warning_message():
	'''
	GenericDialog output of a warning message in case the channel number is incorrectly input
	'''
	gd = GenericDialog('Warning')
	gd.addMessage('Please write the correct channel number')
	gd.showDialog()

def preprocess_image(file_input, channel_value):
	'''
	Preprocessing the images in order to minimizie variance between the input files
	# Parameters:
	1. file_input: the file path to the image file (tif only)
	'''
	# filter out the DAPI and NOT ORG images
	if 'ORG' in file_input and channel_value in file_input:
		img = ImagePlus(file_input) # opens the image using the ImagePlus API
		img.show()
		img_2 = IJ.run(img, 'Enhance Contrast', 'saturated=0.35')

def process_all_images_dialog():
	'''
	Function that will generate a dialog box to require the user to proceed
	'''
	gd = GenericDialog('Processing All Images')
	
	gd.addMessage('1. Please choose which channels to analyze')
	gd.addStringField('What Channel:', 'DAPI', 1)
#	gd.addRadioButtonGroup('Channels List', ['Dapi', '488', '555', '647'], 1, 4, 'Dapi')
	gd.addMessage('2. Do you wish to process all the images?')
	gd.addMessage('NOTE: this will only process the ORG images')
	gd.setOKLabel('Process Images')
	gd.showDialog() # displaying the dialog box

	channel_value = gd.getNextString()
	if gd.wasOKed():
		return True, channel_value
	else:
		return None

def create_selection_dialog(file_input):
    gd = GenericDialog('Please Create a Selection')
    gd.addMessage('Please Select the Hippocampus for file: \n' + str(file_input))
    # The build in function enumerate() returns two values:
    # The index and the value stored in the tuple/list.
    gd.setOKLabel('Create Selection')
    gd.showDialog()
    if gd.wasOKed():
    	# OK = user will create a manual ROI
		manual_selection(file_input)
	else:
		return

def manual_selection(image_input):
	'''
	function that will allow user to manually create a ROI for measurement
	# Parameter: 
	1. image_input: file path of image to be analyzed
	'''
	get
				
# If a Jython script is run, the variable __name__ contains the string '__main__'.
# If a script is loaded as module, __name__ has a different value.
if __name__ in ['__builtin__','__main__']:
    main()