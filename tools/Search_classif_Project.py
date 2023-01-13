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
        dirName = str(Path(options.dir))
    if options.classif is None:
        classif="Crystal"
    else:
        classif=options.classif
    if options.UNIQUE is None or options.UNIQUE is False:
        UNIQUE=False
    else:
        UNIQUE=True
    
    print("Working folder is: ", dirName)
 
    files=list()
    for (dirpath, dirnames, _filenames) in os.walk(dirName):
        files+= [os.path.join(dirpath, file) for file in _filenames if "_data.txt" in file]
    files.sort(key=natural_sort_key)
    
    filtered=list()
    toreport=list()
    results=list()
    lines=list()
    _temp=list()
 
    #Filter all wells with given classification
    for elem in files:
        lines.clear()
        with open(elem,'r') as f:
            lines=f.readlines()
        if classif in lines[5]:
            filtered.append(elem)

    if UNIQUE is True:
        for elem in filtered:
            _path = Path(elem)
            target=_path.parts[-5]
            plate=_path.parts[-4]
            date=_path.parts[-2]
            well=_path.stem.split('_')[0]
            _temp.append((str(plate+'_'+well),
                          date,
                          elem))   
        #Filtering to keep most recent only
        _unique=[]
        for elem in _temp:
            if elem[0] not in _unique:
                _unique.append(elem[0])
                res = list(filter(lambda x: elem[0] in x, _temp))
                res.sort(key=lambda tup: tup[1])  # sorts in place
                toreport.append(res[-1][2])
            else:
                continue #condition already dealt with
    else:
        toreport=filtered
     
    for elem in toreport:
        _path = Path(elem)
        _parents=_path.parents
        target=_path.parts[-5]
        plate=_path.parts[-4]
        date=_path.parts[-2]
        well=_path.stem.split('_')[0]
        pathtoImg=str(_parents[2])+'/'+date+'*/'+well+'.jpg'
        pathtoImg=glob.glob(pathtoImg)        
        if len(pathtoImg)!=0:
            pathtoImg=pathtoImg[-1] #glob returns a list
        else:#Should not append but...
            pathtoImg=''
        results.append((target,plate,date,pathtoImg,well))

    fields = ['Target', 'Plate', 'Date', 'Path to image', 'Well']
    fname='All_'+classif+'.csv'
    fname=dirName+'/'+fname
    with open(fname, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(results)
    print(f"Results saved to {fname}")
    
    del results #, all_files        

if __name__ == '__main__':
    main()
