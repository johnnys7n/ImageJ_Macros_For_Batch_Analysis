from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog, Roi, ImageRoi, ImageWindow
from ij.process import AutoThresholder, ImageProcessor
from ij.plugin import RGBStackMerge, frame, ImageCalculator
from ij.measure import ResultsTable
from ij.util import FontUtil

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
	img = ImagePlus(file_input) # opens the image using the ImagePlus API
	IJ.run(img, 'Enhance Contrast', 'saturated=0.35')
	img.show()

def process_all_images_dialog():
	'''
	Function that will generate a dialog box to require the user to proceed
	'''
	gd = GenericDialog('Processing All Images')
	font_1 = FontUtil.getFont('Arial', 14, 20)
	font_2 = FontUtil.getFont('Arial', 14, 15)
	gd.addMessage('Image Processor', font_1)
	gd.addMessage('1. Please choose which channels to analyze', font_2)
	gd.addStringField('What Channel:', 'DAPI', 1)
#	gd.addRadioButtonGroup('Channels List', ['Dapi', '488', '555', '647'], 1, 4, 'Dapi')
	gd.addMessage('2. Do you wish to process all the images?', font_2)
	gd.addMessage('NOTE: this will only process the ORG images')
	gd.addMessage('3. Do you wish to only look at one image?', font_2)
	gd.addCheckbox('Get One Image?: ', False)
	gd.setOKLabel('Process Images')
	gd.showDialog() # displaying the dialog box

	channel_value = gd.getNextString()
	rep_image_ans = gd.getNextBoolean()
	if gd.wasOKed():
		return True, channel_value, rep_image_ans
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


def manual_selection(image_input):
	'''
	function that will allow user to manually create a ROI for measurement
	# Parameter: 
	1. image_input: file path of image to be analyzed
	'''
	