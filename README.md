# ImageJ_Macros_For_Batch_Analysis
Using Jython (Python) for creating Macros using the ImageJ module for automating tasks

## Projects

### 1. Automating Cell Counts and Percent Area:

### 2. Batch Image Merger


<h1 align='center'>Instructions</h1>

# Notes:
1. The `utils` directory is only for editing. To locally use the macros on ImageJ please move this directory to the `C:\fiji-win64\Fiji.app\jars\Lib` directory. 

# Project 1: CD3CD45 Quick Merge

The `CD3CD45 Quick Merge` is a Macros to create a merged image of any file.

 Steps:
 1. After installing the macros on the FIJI ImageJ application, open the script on the `Macros --> Run` tab. 
 2. Hit `Run` located below the script box. 
 3. Click on the desired channels (blue, green, red) to merge
 4. There is a option to remove or subtract one of the three channels from the rest. 
 5. The `Process All Images` will merge the channels into one (regardless of whether the subtraction checkbox was checked), then maximize the window for easier visualization. 
 6. 