# importing useful libraries
import os
from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog, Roi, ImageRoi, ImageWindow
from ij.process import AutoThresholder, ImageProcessor
from ij.plugin import RGBStackMerge, frame, ImageCalculator
from ij.measure import ResultsTable

def main():
	
	dir= IJ.getDir('Select the Folder that contains the Images') #changes dir to the folder selected
	files_list = os.listdir(dir) # outputs the list of files in this folder

	
	new_files_list = select_files(files_list, dir)
	combined_files_list = select_channels(new_files_list)

	print(combined_files_list)
	answer, ans488, ans555, ans647, anssub = initial_dialog()
	
	if answer and not anssub:
		channels_merger(combined_files_list, ans488, ans555, ans647)

	if answer and anssub:
		subtractor_merger(combined_files_list, ans488, ans555, ans647)
		

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
	new_list = []
	for file in files_list:
		if 'DAPI' not in file and 'ORG' in file:
			new_list.append(path + file)
	return new_list

def select_channels(file_list):
	'''
	this function will put the two similar files into a list of lists
	'''
	
	s1 = []
	s2 = []
	s3 = []
	s4 = []
	s5 = []
	s_all = []
	s_list = {'s1':s1, 's2':s2, 's3':s3, 's4':s4, 's5':s5}
	for file in file_list:
		if 's1' in file:
			s1.append(file)
		if 's2' in file:
			s2.append(file)
		if 's3' in file:
			s3.append(file)
		if 's4' in file:
			s4.append(file)
		if 's5' in file:
			s5.append(file)
	for name, value in s_list.items():
		s_all.append(value)

	return s_all

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

def subtractor_merger(file_list, a1, a2, a3):
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
		print('subtracting out the 647 channel....')
		result1 = ImageCalculator.run(img_488, img_647, 'subtract')
		result2 = ImageCalculator.run(img_555, img_647, 'subtract')

		print('working on merging the subtracted images')
		final_image = RGBStackMerge.mergeChannels([result2, result1], False)
		final_image.setDisplayMode(IJ.COLOR)
		IJ.run(final_image, "Enhance Contrast", "saturated=0.35")
		final_image.setC(2)
		IJ.run(final_image, "Enhance Contrast", "saturated=0.35")
		final_image.setDisplayMode(IJ.COMPOSITE)
		final_image.show()
		ImageWindow(final_image).maximize()
		
def initial_dialog():
	'''
	Generic Dialog of processor confirmation
	'''
	gd = GenericDialog('Processing first five images')
	gd.addMessage('Which Channels Do you Want to Merge?')
	gd.addMessage('Please Select 2 or More Channels')
	gd.addCheckbox('488', True)
	gd.addCheckbox('555', True)
	gd.addCheckbox('647', False)
	gd.addCheckbox('Subtract Lectin?', False)
	gd.setOKLabel('Process All Files')
	gd.showDialog()
	ans_488 = gd.getNextBoolean()
	ans_555 = gd.getNextBoolean()
	ans_647 = gd.getNextBoolean()
	ans_sub = gd.getNextBoolean()
	if gd.wasOKed():
		return True, ans_488, ans_555, ans_647, ans_sub
	else:
		return False
	
	
if __name__ == '__main__':
	main()