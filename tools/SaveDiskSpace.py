#!/usr/local/PROGRAMS/XTAL/GIT-AMi_Image_Analysis/python/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:25:59 2020

@author: ludovic
"""
import os
from pathlib import Path
import shutil
import argparse

__version__ = "0.1"
__date__ = "20-05-2021"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"

# Define below the name of the folder containing unstacked Z images.
_RAWIMAGES = "rawimages"


def main(args=None):
    ''' main func '''
    # dirName = os.getcwd()
    parser = argparse.ArgumentParser(prog=__name__,
                                     description='Tool to find and  '
                                     'delete all processed '
                                     'folders to save disk '
                                     'space.')
    parser.add_argument('dir', metavar='dirName', nargs='?',
                        help='Directory to iterate over.')
    parser.add_argument('--clean', default=False, action='store_true',
                        dest='clean', help='if not using --clean '
                        'Only checking, no deletion ')

    options = parser.parse_args(args)
    # print("options ", options)

    if options.dir == "." or options.dir is None:
        dirName = os.getcwd()
    else:
        dirName = Path(options.dir)
    # print("dirName: ", dirName)

    # Get the list of all directories _rawimges at given path
    listOfDirs = list()
    for (dirpath, dirnames, _filenames) in os.walk(dirName):
        # listOfDirs += [os.path.join(dirpath, file) for file in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath,file))]
        if _RAWIMAGES in dirnames:
            listOfDirs += [os.path.join(dirpath, file) for file in os.listdir(
                dirpath) if os.path.isdir(os.path.join(dirpath, file))]
    # print(listOfDirs)

    rawdata_subfolders = list()
    for elem in listOfDirs:
        if os.path.islink(elem) is False:
            directory = Path(elem)
            parents = directory.parents
            if directory.parts[-1] == _RAWIMAGES and not Path(parents[0]).joinpath("DONE").is_file():
                print(
                    f"Data in {directory} likely have not been processed, skipping deletion")
            elif directory.parts[-1] == "rawimages" and Path(parents[0]).joinpath("DONE").is_file():
                rawdata_subfolders += [Path(parents[0]).joinpath(_RAWIMAGES)]
    del listOfDirs

    # for path in rawdata_subfolders: print(path)
    if len(rawdata_subfolders) == 0:
        print(f"No directory {_RAWIMAGES} found, nothing to do!!!")
        return
    for path in rawdata_subfolders:
        try:
            os.path.isdir(path)
            if options.clean is False:
                print(f"Will be deleting {path}")
            elif options.clean is True:
                print(f"Deleting {path}")
                shutil.rmtree(path)
        except:
            print(f"WARNING: {path} not found")
            return


if __name__ == '__main__':
    main()
