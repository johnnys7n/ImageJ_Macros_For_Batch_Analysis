from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog, Roi, ImageRoi
from ij.process import AutoThresholder, ImageProcessor

# importing the os module to communicate with the local files
import os

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


def manual_selection(image_input):
	'''
	function that will allow user to manually create a ROI for measurement
	# Parameter: 
	1. image_input: file path of image to be analyzed
	'''
	pass