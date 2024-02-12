#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
import glob
from pathlib import Path

# Define below the relevant folder.
_DATA = "Image_Data"
_RAWIMAGES="rawimages"
_nsre = re.compile('([0-9]+)')

rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

total_wells = [row + str(col)
               for row in rows for col in cols]

class initProject(object):
    """Initialise various variables. Put in utils for later compatibility
    if changes are needed for other microscopes.
    path is a pathlib.Path
    """
    def __init__(self, path):
        self.path=path
        self.Directory(self.path)
    
    def Directory(self, path):
        directory=Path.resolve(path)
        parents=directory.parents
        self.rawimages=_RAWIMAGES
        if directory.parts[-1]==self.rawimages or directory.parts[-1]=="cropped":
            self.rootDir = parents[1]
            self.project=directory.parts[-5] #-5 if projectID is set. or -4
            self.target=directory.parts[-4]
            self.plate=directory.parts[-3]
            self.date=directory.parts[-2].split("_")[0]
            # self.timed=directory.parts[-2].split("_")[1]
            self.prep_date_path = self.rootDir.joinpath("prep_date.txt")
        else:
            self.rootDir =parents[0]
            self.project=directory.parts[-4] #-4 if projectID is set. or -3
            self.target=directory.parts[-3]
            self.plate=directory.parts[-2]
            self.date=directory.parts[-1].split("_")[0]
            # self.timed=directory.parts[-1].split("_")[1]
            self.prep_date_path = self.rootDir.joinpath("prep_date.txt")


def natural_sort_key(s):
    global _nsre
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

def main(args=None):
    
    parser = argparse.ArgumentParser(prog=__name__,
                                     description='Tool to create '
                                     'json files from *_data.txt'
                                     'for a given plate')    
    parser.add_argument('dir', metavar='dirName', nargs='?',
                    help='Directory to iterate over.')
    # parser.add_argument('date', metavar='Imgdate', help='Imaging date', required=True)
    
    options = parser.parse_args(args)
    print("options ", options)

    if options.dir == "." or options.dir is None:
        dirName = os.getcwd()
    else:
        dirName = str(Path(options.dir))

    dirName = Path(dirName)
    PATHS = initProject(dirName)
    dirName=Path(PATHS.rootDir).joinpath(_DATA,PATHS.date)
    print("Working folder is: ", dirName)
    
    
    files=list()
    for (dirpath, dirnames, _filenames) in os.walk(dirName):
        files+= [os.path.join(dirpath, file) for file in _filenames if "_data.txt" in file]
    files.sort(key=natural_sort_key)

    data=list()
    for elem in files:
        with open(elem,'r') as f:
            lines=f.readlines()
            well = Path(elem).stem.replace('_data','')
            lines.append(f'Well:{well}')
            data.append(lines)
    
    # Remove in place
    for ls in data:
        for i, s in enumerate(ls):
            ls[i]=s.strip('\n')
            

    # for ls in data: print(ls)

    #Organize data
    datadict=dict()
    Plate=PATHS.plate
    datadict[Plate]=dict()
    datadict[Plate]['Project']=PATHS.project
    datadict[Plate]['Target']=PATHS.target
    datadict[Plate]['Plate Name']=PATHS.plate
    datadict[Plate]['Screen']=None
    with open(PATHS.prep_date_path) as f:
        _prep_date=f.readlines()
    datadict[Plate]['Prep_Date']=_prep_date[0].strip()
    datadict[Plate]['Imaging_Date']=PATHS.date
    datadict[Plate]['Wells']=dict()

    for ls in data:
        # _id=data.index(ls)
        # print('_id: ', _id)
        well=ls[-1].split(':')[1]
        datadict[Plate]['Wells'][well]=dict()
        datadict[Plate]['Wells'][well]['well']=well
        datadict[Plate]['Wells'][well]['subwell']=''.join(x for x in well[-1] if well[-1].islower())
        datadict[Plate]['Wells'][well]['reservoir']=''.join(x for x in well if not x.islower())
        datadict[Plate]['Wells'][well]['position']=total_wells.index(datadict[Plate]['Wells'][well]['reservoir'])+1
        datadict[Plate]['Wells'][well]['date']=PATHS.date
        datadict[Plate]['Wells'][well]['Classification']=ls[5].split(':')[1]
        datadict[Plate]['Wells'][well]['Human Score']=ls[6].split(':')[1]
        datadict[Plate]['Wells'][well]['Notes']=ls[10:-1] #-1 to remove added well within script

        fname= Path(PATHS.rootDir).joinpath(
            "Image_Data", PATHS.date, f'data_{PATHS.date}.json')
    writetojson(datadict, fname)

def writetojson(data, filename):
    with open(filename, "w") as outfile:
    	json.dump(data, outfile, indent=4)
    print("JSON file saved to: ", filename)

if __name__ == '__main__':
    main()
