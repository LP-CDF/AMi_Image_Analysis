#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:43:59 2024

@author: ludovic
"""
import argparse
from pathlib import Path
import pandas as pd
import json
import glob
import os

__version__ = "0.1"
__date__ = "01-02-2024"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"

def writetojson(data, fname):
    '''export data to json'''
    with open(fname, "w") as f:
     	json.dump(data, f)

def create_DataFrame(data):
    '''Load Project_database.json and create pandas.DataFrame'''
    # #Normalize
    data_frames=[]
    for i in data:
     	data_frames.append(pd.json_normalize(i))
    
    combined_Norm = pd.concat(data_frames)
    # print("Normalized combined: \n", combined_Norm)
    return combined_Norm

def search_DataFrame(data, field, val): 
    result=data.loc[data[field]==val]
    # print("type(loc): ", type(test))
    print(f"Search for {val}: \n", result)
    return result

def main(args=None):
    ''' main func '''
    # dirName = os.getcwd()
    parser = argparse.ArgumentParser(prog=__name__,
                                     description='Tool to generate  '
                                     'json file '
                                     'for the whole Project')
    parser.add_argument('dir', metavar='dirName', nargs='?',
                        help='Directory to iterate over.')

    options = parser.parse_args(args)
    # print("options ", options)

    if options.dir == "." or options.dir is None:
        dirName = os.getcwd()
    else:
        dirName = str(Path(options.dir))

    print("Working folder is: ", dirName)

    files = glob.glob(f'{dirName}/**/data_????????.json', recursive = True)
    # for i in files: print('File: ', i) #DEBUG
    
    data_json = []
    for i in files:
     	with open(i, "r") as f:
              data_json.append(json.load(f))

    #Add new fields in Wells dict
    for i in data_json:
        _key=list(i.keys())[0]
        for k,v in i[_key]['Wells'].items():
            i[_key]['Wells'][k]["Plate"]=_key
            i[_key]['Wells'][k]["Target"]=i[_key]["Target"]
    
    # #Remove one level of data for pandas
    # data_json_new=[]
    # for i in data_json:
    #     _key=list(i.keys())[0]
    #     # print("Plate Name: ", i[_key]["Plate Name"])
    #     data_json_new.append(dict(i[_key]))

    
    # #Convert Wells dict to list removing keys for pandas
    # for i in data_json_new:
    #     items_list = [v for k,v in i['Wells'].items()]
    #     i['Wells']=items_list

    #Keep only Wells data for pandas
    temp=[]
    for i in data_json:
        _key=list(i.keys())[0]
        # print("Plate Name: ", i[_key]["Plate Name"])
        temp.append(dict(i[_key]['Wells']))
    
    #Convert Wells dict to list removing keys for pandas
    data_json_new=[]
    for i in temp:
        items_list = [v for k,v in i.items()]
        data_json_new.append(items_list)
    del temp
    
    #Save to file
    fname=Path(dirName).joinpath('Project_database.json')
    writetojson(data_json_new, fname)
    print(f"JSON data for Project exported to {fname}")

    # #Test read back
    # with open(fname, "r") as f:
    #        data_json=json.load(f)

     
if __name__ == '__main__':
    main()