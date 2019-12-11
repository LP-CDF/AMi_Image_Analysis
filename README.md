# AMi Image Analysis: Automated Microscope Image Analysis

This is a Python 3 / PyQt5 project dedicated to the analysis of the images generated by the AMi microscope.
The AMi microscope is a low-cost automated microscope.

For more details on this device, please look at:
"AMi: a GUI-based, open-source system for imaging samples in multi-well plates"
Andrew Bohm, Acta Crystallogr F Struct Biol Commun. 2019 Aug 1; 75(Pt 8): 531–536.
doi: 10.1107/S2053230X19009853


## Features:

I created this application to help the members of our laboratory in their crystallization work.
The software can read tiff or jpeg files.
Images are accessed via clicking on the corresponding well button or by navigating with keyboard shortcuts.
Images can be zoomed for thorough inspection and a timeline of the corresponding well is displayed if several pictures of the same well taken at different times are available.

Images are scored using the Drop Score section.
Notes can be taken and are saved to file.

A report of the current well can be saved as a pdf.

The results can be displayed on a grid and statistics are also calculated.

## Screenshots

![Screenshot 1](./screenshot1.png)
![Screenshot 2](./screenshot2.png)

## Install

    The software was only tested on linux CentOS 7 (PyQt5 (v5.9.2 and v5.12.1) and python3 (v3.6.8 and v3.7.3)) and on Raspbian 10.
    Hopefully, it should work on OSX and Windows.
    You will need a screen with minimum resolution of 1920*1080.

    Download the latest released version and gunzip it or clone this repository with
    git clone https://github.com/LP-CDF/AMi_Image_Analysis .

    If on linux or OSX, link the correct Shortcuts_XXX.py version to Shortcuts.py
    If on Windows, copy the correct Shortcuts_XXX.py version to Shortcuts.py

    Dependancies:
    * PyQt5 (v5.9.2 or higher, previous version not tested)
    * Python Imaging Library (Pillow, v6.2.1 or higher)
    * PyFPDF (v1.7.2 or higher)

known issues: 
    * On Raspbian, you must ensure that package qt5-image-formats-plugins is installed
    * On Raspbian, buttons do not change color when clicked.

## Citation

If you wish to cite this work, you can use the following reference:
To be added


## Acknowledgements

This project would not have been possible without the previous work of Dakota Handzlik published in:
Acta Crystallogr F Struct Biol Commun. 2019 Nov 1;75(Pt 11):673-686. doi: 10.1107/S2053230X19014730
and initially written for Tk (https://github.com/dakota0064/Fluorescent_Robotic_Imager)


