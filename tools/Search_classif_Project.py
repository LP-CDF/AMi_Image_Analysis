#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:25:59 2020

@author: ludovic
"""
import os
from pathlib import Path
import argparse
import re
import csv
import glob

__version__ = "0.1"
__date__ = "23-11-2021"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"

# Define below the relevant folder.
_DATA = "Image_Data"
_nsre = re.compile('([0-9]+)')

def natural_sort_key(s):
    global _nsre
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def main(args=None):
    ''' main func '''
    # dirName = os.getcwd()
    parser = argparse.ArgumentParser(prog=__name__,
                                     description='Tool to find all  '
                                     'conditions with '
                                     'specified classification.')
    parser.add_argument('dir', metavar='dirName', nargs='?',
                        help='Directory to iterate over.')
    parser.add_argument('--class', default='Crystal',
                        dest='classif', help='''classes are:
                        'Clear'
                        'Crystal'
                        'Precipitate'
                        'PhaseSep'
                        'Other'
                        'Unknown'
                        'The exact class name must be used (case sensitive)''')
    parser.add_argument('--unique', default=False,action='store_true',
                        dest='UNIQUE', help='report unique condition')

    options = parser.parse_args(args)
    print("options ", options)

    if options.dir == "." or options.dir is None:
        dirName = os.getcwd()
    else:
        dirName = Path(options.dir)
    if options.classif is None:
        classif="Crystal"
    else:
        classif=options.classif
    if options.UNIQUE is None or options.UNIQUE is False:
        UNIQUE=False
    else:
        UNIQUE=True
    
    print("Working folder is: ", dirName)


################################ OLD ################################
    # # Get the list of all directories _rawimges at given path
    # listOfDirs = list()
    # for (dirpath, dirnames, _filenames) in os.walk(dirName):
    #     if _DATA in dirnames:
    #         if os.path.isdir(os.path.join(dirpath,_DATA)):
    #                          listOfDirs.append(os.path.join(dirpath, _DATA))

    # if len(listOfDirs) == 0:
    #     print("No files *_data.txt found, nothing to do!!!")
    #     return
    
    # all_files=list()
    # for path in listOfDirs:
    #     # print("path", path)
    #     files=list()
    #     for (dirpath, dirnames, _filenames) in os.walk(path):
    #         # print(_filenames)
    #         files+= [os.path.join(dirpath, file) for file in _filenames if "_data.txt" in file]
    #     files.sort(key=natural_sort_key)
    #     all_files.append(files)
    
    # results=list()
    # for lst in all_files:
    #     for elem in lst:
    #         directory = Path(elem)
    #         parents=directory.parents
    #         plate=directory.parts[-4]
    #         date=directory.parts[-2]
    #         basename=os.path.basename(elem)
    #         well=basename.split("_")[0]
    #         pathtoImg=str(parents[2])+'/'+date+'*/'+well+'.jpg'
    #         pathtoImg=glob.glob(pathtoImg)
    #         if len(pathtoImg)!=0:
    #             pathtoImg=pathtoImg[0]
    #         else:#Should not append but...
    #             pathtoImg=''
    #         with open(elem,'r') as f:
    #             lines=f.readlines()
    #         if classif in lines[5]:
    #             results.append((plate,date,well,pathtoImg))
################################ END OLD ################################
 
    files=list()
    for (dirpath, dirnames, _filenames) in os.walk(dirName):
        files+= [os.path.join(dirpath, file) for file in _filenames if "_data.txt" in file]
    files.sort(key=natural_sort_key)
    
    results=list()
    lines=list()
    unique_report=list()
    for elem in files:
        lines.clear()
        with open(elem,'r') as f:
            lines=f.readlines()
        if classif in lines[5]:
            _directory = Path(elem)
            _parents=_directory.parents
            plate=_directory.parts[-4]
            date=_directory.parts[-2]
            _basename=os.path.basename(elem)
            well=_basename.split("_")[0]
            pathtoImg=str(_parents[2])+'/'+date+'*/'+well+'.jpg'
            pathtoImg=glob.glob(pathtoImg)
            if UNIQUE is True:
                if str(plate+'_'+well) not in unique_report:
                    unique_report.append(str(plate+'_'+well))
                    if len(pathtoImg)!=0:
                        pathtoImg.sort(key=natural_sort_key)
                        pathtoImg=pathtoImg[-1]#if same date, keep most recent
                    else:#Should not append but...
                        pathtoImg=''
                    results.append((plate,well,date,pathtoImg))
            else:
                if len(pathtoImg)!=0:
                    pathtoImg.sort(key=natural_sort_key)
                    pathtoImg=pathtoImg[-1]#if same date, keep most recent
                else:#Should not append but...
                    pathtoImg=''
                results.append((plate,well,date,pathtoImg))
        else:
            continue
           
    fields = ['Plate', 'Well', 'Date', 'Path to image']
    fname='All_'+classif+'.csv'
    with open(fname, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(results)
    print(f"Results saved to {dirName+'/'+fname}")
    
    del results #, all_files        

if __name__ == '__main__':
    main()