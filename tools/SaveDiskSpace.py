#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:25:59 2020

@author: ludovic
"""
import os, sys
from pathlib import Path
import shutil
import argparse

#Define below the name of the folder containing unstacked Z images.
_rawimages="rawimages"

def main(args=None):
    global total_wells
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

    if  options.dir=="." or options.dir==None:
        dirName = os.getcwd()
    else:
        dirName=Path(options.dir)
    # print("dirName: ", dirName)
    
    # Get the list of all files in directory tree at given path
    listOfDirs = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfDirs += [os.path.join(dirpath, file) for file in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath,file))]
        

    rawdata_subfolders=list()
    for elem in listOfDirs:
        if os.path.islink(elem) is False:
            directory=Path(elem)
            parents=directory.parents
            if directory.parts[-1]==_rawimages and not Path(parents[0]).joinpath("DONE").is_file():
                print(f"Data in {directory} likely have not been processed, skipping deletion")
            elif directory.parts[-1]=="rawimages" and Path(parents[0]).joinpath("DONE").is_file():
                rawdata_subfolders += [Path(parents[0]).joinpath(_rawimages)]
    del listOfDirs
    
    # for path in rawdata_subfolders: print(path)
    if len(rawdata_subfolders)==0:
        print(f"No directory {_rawimages} found, nothing to do!!!")
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