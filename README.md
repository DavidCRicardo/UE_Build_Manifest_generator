# UE_Build_Manifest-pak_generator
This script generates a fresh build manifest text file automatically.

I created this small Python script in order to automatize the process to create a new BuildManifest file.

## How it works
This script will automatically read the .pak files that Unreal has generated. After that, it will reate a new file/ update the file named "BuildManifest.txt".

## Before Use
1. Update project's name and path 
2. Update BUILD ID according with the one that you're using it

## How to use
- You can run this script at Visual Studio Code (for example). But in other editor it should work as well.
or
- You can also run it inside Unreal Editor in "Tools -> Execute Python Script..."

## Limitations
This script only works with .pak generated files. <br> 
It doesn't support the Io Store configuration (.utoc/.ucas container files).

##
Please, don't forget to give create when using it or modifying it. 
##
Created by David Ricardo
