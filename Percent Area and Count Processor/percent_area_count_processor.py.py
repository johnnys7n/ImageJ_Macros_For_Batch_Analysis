import image_utils as iu

# Next we import Java Classes into Jython.
# This is how we can acces the ImageJ API:
# https://imagej.nih.gov/ij/developer/api/allclasses-noframe.html
from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog, Roi, ImageRoi
from ij.process import AutoThresholder, ImageProcessor
import random

# importing the os module to communicate with the local files
import os

# It's best practice to create a function that contains the code that is executed when running the script.
# This enables us to stop the script by just calling return.
def main():	
	# assigning directory path to 'dir' variable
	dir = IJ.getDir('Choose Directory')
	
	# getting the list of files within the directory
	dir_list = os.listdir(dir)

	preprocess_answer, channel_value, one_image_only = iu.process_all_images_dialog()

	if preprocess_answer == True:
		#	creating a list of the folders inside the working directory
		if '.tif' not in dir_list[0]:
			non_hidden_items = [item for item in os.listdir(dir) if not item.startswith('.')]
			dir_working = []
			for items in non_hidden_items:
				dir_working.append(dir + items)
		#	opening the files in the working directory

			if one_image_only:
				for dir_wd in dir_working:
					print('Directory Processing: ' + dir_wd)
					files = os.listdir(dir_wd)
					a = 0
					file_list = []
					for file in files:
						if 'ORG' in file and channel_value in file:
							file_path = str(dir_wd + "\\" + file)
							file_list.append(file_path)
					print('currently processing: ' + file_list[0])
					# generate random image number for each directory
					random_img = random.randint(0,len(file_list)-1)
					iu.preprocess_image(file_list[random_img], channel_value)
					a += 1
					if a == 0:
						iu.warning_message()
			else:
				for dir_wd in dir_working:
					print('Directory Processing: ' + dir_wd)
					files = os.listdir(dir_wd)
					a = 0
					file_list = []
					for file in files:
						if 'ORG' in file and channel_value in file:
							file_path = str(dir_wd + "\\" + file)
							print('currently processing: ' + file)
							file_list.append(file_path)
							iu.preprocess_image(file_path, channel_value)
					a += 1
					if a == 0:
						iu.warning_message()

						
		else:
			b = 0
			for file in dir_list:
				if channel_value in file:
					print('currently processing' + file)
					file_path = str(dir + file)
					iu.preprocess_image(file_path, channel_value)
#					create_selection_dialog(file_path)
					b += 1
			if b == 0:
				iu.warning_message()


				
# If a Jython script is run, the variable __name__ contains the string '__main__'.
# If a script is loaded as module, __name__ has a different value.
if __name__ in '__main__':
    main()