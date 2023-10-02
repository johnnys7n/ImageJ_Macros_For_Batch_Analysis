# importing useful libraries
import os
from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog, Roi, ImageRoi, ImageWindow
from ij.process import AutoThresholder, ImageProcessor
from ij.plugin import RGBStackMerge, frame, ImageCalculator
from ij.measure import ResultsTable
from ij.util import FontUtil


def main():

	# getting the directory file list and path
	try:
		dir= IJ.getDir('Select the Folder that contains the Images') #changes dir to the folder selected
		files_list = os.listdir(dir) # outputs the list of files in this folder
	except TypeError, UnboundLocalError:
		print('User cancelled operation')

	# selecting only the useful images within the file list
	new_path_list, new_files_list = select_files(files_list, dir)
	org_working_file_list = select_channels_working(new_path_list, new_files_list)
	
	print(org_working_file_list)
	# merging and processing images
	answer, ans488, ans555, ans647, anssub, ansclear = initial_dialog()

	if answer:
		if anssub == 'No':
			channels_merger(org_working_file_list, ans488, ans555, ans647)
		elif anssub != 'No':
			subtractor_merger(org_working_file_list, ans488, ans555, ans647, anssub)
	else:
		print('program stopped by user')
				
	if ansclear:
		# cleans the ROI Manager
		RM = frame.RoiManager()
		rm = RM.getRoiManager()
		rm.reset()
	
		# cleans the Results Table
		if IJ.isResultsWindow():
			RT = ResultsTable()
			rt = RT.getResultsTable()
			size = rt.size()
			IJ.deleteRows(0,size)
	
	
	print('Finished Processing....Enjoy Analyzing! :)')

def select_files(files_list, path):
	'''
	Function that creates a new list of files inside the selected directory that is only 488 ORG and 555 ORG
	'''
	new_file_path_list = []
	new_file_list = []
	for file in files_list:
		if 'DAPI' not in file and 'ORG' in file:
			new_file_path_list.append(path + file)
			new_file_list.append(file)
	return new_file_path_list, new_file_list

 
def select_channels_working(new_file_list, file_list):
	'''
	This is a function for putting all the images in the same scene together
	'''
	scenes_list = []
	for file in file_list:
		x = file.split('_', 2)
		scenes_list.append(x[1])
#		scenes_list.append(x[1])
	unique_scenes = set(scenes_list)
	list_scenes = list(unique_scenes)
	scenes_all = []
	for i, scene in enumerate(list_scenes):
		add_all = [images for images in new_file_list if scene in images]
		scenes_all.append(add_all)
	return scenes_all
		

def channels_merger(file_list, a1, a2, a3):
	'''
	Function that will merge the images for each scene
	'''
	# creating a list of working files
	for files in file_list:
		working_list = []
		for file in files:
			if 'AF488' in file and a1:
				img_488 = ImagePlus(file)
				working_list.append(img_488)
			if 'AF555' in file and a2:
				img_555 = ImagePlus(file)
				working_list.append(img_555)
			if 'AF647' in file and a3:
				img_647 = ImagePlus(file)
				working_list.append(img_647)
		print('creating merged image....')
		if len(working_list) == 1: # only one of the channels is selected
			if a1: # 488
				img = working_list[0]
				IJ.run(img, 'Green', '')
				IJ.run(img, "Enhance Contrast", "saturated=0.35")
				img.show()
				ImageWindow(img).maximize()
			if a2: # 555
				img = working_list[0]
				IJ.run(img, 'Red', '')
				IJ.run(img, "Enhance Contrast", "saturated=0.35")
				img.show()
				ImageWindow(img).maximize()
			if a3: # 647
				img = working_list[0]
				IJ.run(img, 'Cyan', '')
				IJ.run(img, "Enhance Contrast", "saturated=0.35")
				img.show()
				ImageWindow(img).maximize()
		if len(working_list) == 2: # only if two of the three channels are selected
			print('working on merging 2 images...')
			result = RGBStackMerge.mergeChannels([working_list[1], working_list[0]], False)
			result.setDisplayMode(IJ.COLOR)
			IJ.run(result, "Enhance Contrast", "saturated=0.35")
			result.setC(2)
			IJ.run(result, "Enhance Contrast", "saturated=0.35")  
			result.setDisplayMode(IJ.COMPOSITE)
			result.show()
			ImageWindow(result).maximize()
		if len(working_list) == 3: # if all three channels are selected
			print('working on merging 3 images...')
			result = RGBStackMerge.mergeChannels([working_list[1], working_list[0],None ,working_list[2]], False)
			result.setDisplayMode(IJ.COLOR)
			IJ.run(result, "Enhance Contrast", "saturated=0.35")
			result.setC(2)
			IJ.run(result, "Enhance Contrast", "saturated=0.35")  
			result.setC(3)
			IJ.run(result, "Enhance Contrast", "saturated=0.35")  
			result.setDisplayMode(IJ.COMPOSITE)
			result.show()
			ImageWindow(result).maximize()

def subtractor_merger(file_list, a1, a2, a3, ans_sub):
	'''
	This is a function that will remove the 647 channel from the other two and return the two images
	'''
	for files in file_list:
		working_list = []
		for file in files:
			if 'AF488' in file and a1:
				img_488 = ImagePlus(file)
				working_list.append(img_488)
			if 'AF555' in file and a2:
				img_555 = ImagePlus(file)
				working_list.append(img_555)
			if 'AF647' in file and a3:
				img_647 = ImagePlus(file)
				working_list.append(img_647)
		print('subtracting out the {} channel....'.format(ans_sub))
		try:
			if ans_sub == '488':
				result1 = ImageCalculator.run(img_647, img_488, 'subtract')
				result2 = ImageCalculator.run(img_555, img_488, 'subtract')		
			elif ans_sub == '555':
				result1 = ImageCalculator.run(img_488, img_555, 'subtract')
				result2 = ImageCalculator.run(img_647, img_555, 'subtract')
			else:
				result1 = ImageCalculator.run(img_488, img_647, 'subtract')
				result2 = ImageCalculator.run(img_555, img_647, 'subtract')
			print('working on merging the subtracted images')
			final_image = RGBStackMerge.mergeChannels([result2, result1], False)
			final_image = pixel_scaler(final_image)
			ImageWindow(final_image).maximize()
	
			final_image.setDisplayMode(IJ.COLOR)
			IJ.run(final_image, "Enhance Contrast", "saturated=0.35")
			final_image.setC(2)
			IJ.run(final_image, "Enhance Contrast", "saturated=0.35")
			final_image.setDisplayMode(IJ.COMPOSITE)
			final_image.show()
		except UnboundLocalError:
			print('user has selected an empty channel')

def pixel_scaler(image):
	'''
	function for scaling images according to the axioscan px-um conversion
	'''
	print('rescaling the images from pixels to um...')
	IJ.run(image, "Set Scale...","distance=1 known=0.44 unit=um")
	return image
	
		
def initial_dialog():
	'''
	Generic Dialog of processor confirmation
	'''
	font_1 = FontUtil.getFont('Arial', 14, 20)
	font_2 = FontUtil.getFont('Arial', 14, 15)
	gd = GenericDialog('Processing first five images')
	gd.addMessage('CD3 CD45 Lectin Image Processor',font_1)
	gd.addMessage('Which Channels Do you Want to Merge?', font_2)
	gd.addMessage('Please Select 1 or more Channels')
	gd.addCheckbox('488', True)
	gd.addCheckbox('555', True)
	gd.addCheckbox('647', False)
#	gd.addCheckbox('Subtract Lectin?', False)
	gd.addMessage('Which Channel contains lectin (to subtract)', font_2)
	gd.addMessage('*Note all three channels must be selected for subtraction*')
	gd.addRadioButtonGroup('Channels:', ['No', '488', '555', '647'], 1, 4, 'No')
	gd.setOKLabel('Process All Files')
	gd.addMessage('Do you wish to clear the output? (ROI + Results Table)', font_2)
	gd.addCheckbox('Clear Results?', True)
	gd.showDialog()
	ans_488 = gd.getNextBoolean()
	ans_555 = gd.getNextBoolean()
	ans_647 = gd.getNextBoolean()
	ans_sub = gd.getNextRadioButton()
	ans_clear = gd.getNextBoolean()
	if gd.wasOKed():
		return True, ans_488, ans_555, ans_647, ans_sub, ans_clear
	else:
		return False, False, False, False, 0, False
	
	
if __name__ == '__main__': 
	main()