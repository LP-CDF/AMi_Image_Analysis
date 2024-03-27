#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:57:50 2020

"""

__date__ = "03-03-2024"

import os
import sys
import argparse
from pathlib import Path
import stat
from utils import _RAWIMAGES


def CreateUninstall(app_path, venv_path):
    '''Create a python script to remove program or most of it
    app_path and venv_path are string
    '''
    file_path = Path(app_path).joinpath("Uninstall.py")
    print(f"Creating uninstall script in {file_path}")
    content = f'''#!/usr/bin/env python3

import os, sys, shutil
from pathlib import Path
from subprocess import call

app_path="{app_path}"
venv_path="{venv_path}"

print("APP_PATH: ", app_path)

venv_path=Path(venv_path).parent
print("VENV_PATH: ", venv_path)

try:
    os.path.isdir(venv_path)
    shutil.rmtree(venv_path)
    print("SUCCESSFULLY removed Python virtual env for AMi_Image_Analysis")
except:
    print("WARNING: %s not Found, exiting."%venv_path)
    sys.exit()

try:
    os.path.isdir(app_path)
    shutil.rmtree(app_path)
    print("SUCCESSFULLY removed AMi_Image_Analysis")
except :
    print("WARNING: %s not found"%app_path)
    sys.exit()


print("------------------------------------------------------")
print("You have to manually remove any Startup Icon or alias")
print("------------------------------------------------------")

'''
    with open(file_path, 'w') as f:
        f.write(content)
    os.chmod(file_path, st.st_mode | stat.S_IXUSR |
             stat.S_IXGRP | stat.S_IXOTH)


def ChangeSheBang(app_path, filename, python_path):
    '''app_path and filename are strings'''
    file_path = Path(app_path).joinpath(filename)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines[0] = "#!" + python_path+'/python \n'
    with open(file_path, 'w') as f:
        for l in lines:
            f.write(l)
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IXUSR |
             stat.S_IXGRP | stat.S_IXOTH)


# def ChangeRAW(app_path, filename, _string):
#     '''app_path and filename are strings, stops at first encounter'''
#     file_path = Path(app_path).joinpath(filename)
#     INDEX = False
#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#     for i in lines:
#         if "_RAWIMAGES=" in i:
#             INDEX = lines.index(i)
#             break
#     if INDEX is not False:
#         lines[INDEX] = '''_RAWIMAGES="%s"\n''' % _string
#     with open(file_path, 'w') as f:
#         for l in lines:
#             f.write(l)

def ChangeField(app_path, filename, field, _string):
    '''app_path and filename are strings, stops at first encounter'''
    file_path = Path(app_path).joinpath(filename)
    INDEX = False
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i in lines:
        if field in i:
            INDEX = lines.index(i)
            break
    if INDEX is not False:
        lines[INDEX] = f'''{field}="%s"\n''' % _string
    with open(file_path, 'w') as f:
        for l in lines:
            f.write(l)

def SetNoPRojectID(_string, _list):
    indexes = [_list.index(i) for i in _list if _string in i]
    _list[indexes[0]] = "            self.project=directory.parts[-4] #-5 if projectID is set. or -4\n"
    _list[indexes[1]] = "            self.project=directory.parts[-3] #-4 if projectID is set. or -3\n"
    return _list


def main(args=None):
    global st
    parser = argparse.ArgumentParser(prog=__name__,
                                     description='Creates virtual Python '
                                                 'environments in one or '
                                                 'more target '
                                                 'directories.')
    parser.add_argument('--no-ProjectID', default=False,
                        action='store_true', dest='noprojectID',
                        help="Don't use ProjectID in tree")
    parser.add_argument('--FR', default=False,
                        action='store_true', dest='layoutFR',
                        help="set keyboard to FR")
    
    options = parser.parse_args(args)

    print("within Setup_local.py OPTIONS noprojectID is", options.noprojectID)

    activate_venv = {'linux': 'activate', 'darwin': 'activate',
                     'win32': 'activate.bat'}[sys.platform]
    python_path = os.path.join(os.path.dirname(sys.executable))

    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    file_path = Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")

    with open(file_path, 'w') as f:
        f.write('''#!/usr/bin/env bash
    
#File generated with Setup_local.py
virtenv="%s"
. ${virtenv}/%s

#DO NOT EDIT the next THREE LINES
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
parentdir="$(dirname "$DIR")"
python3 $parentdir/AMi_Image_Analysis.py

deactivate''' % (python_path, activate_venv))

    # _list is [(path,filename,True/false for ChangeRAW, True/false for ChangeSheBang)]
    _list = [(app_path, "utils.py", True, False),
             (app_path+'/tools/', "Merge_AllNewPlates.py", True, True),
             (app_path+'/tools/', "Merge_Zstack.py", True, True),
             (app_path+'/tools/', "SaveDiskSpace.py", True, True),
             (app_path+'/tools/', "Create_json.py", False, True),
             (app_path+'/tools/', "Create_Project_json.py", False, True),
             (app_path+'/tools/', "Search_classif_Project.py", False, True),
             (app_path, "autocrop.py", False, True),
             (app_path, "Check_Circle_detection.py", False, True)]

    # Change _RAWIMAGES to adapt to maybe different but compatible microscope softwares
    for i in _list:
        if i[2] is True:
            # ChangeRAW(i[0], i[1], _RAWIMAGES)
            ChangeField(i[0], i[1], '_RAWIMAGES', _RAWIMAGES)

    # do not use Set ProjectID if --no-ProjectID
    with open('utils.py', 'r') as f:
        lines = f.readlines()
    if options.noprojectID is True:
        NEW = SetNoPRojectID("self.project", lines)
        with open("utils.py", 'w') as f:
            for l in NEW:
                f.write(l)

    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IXUSR |
             stat.S_IXGRP | stat.S_IXOTH)
    
    # set layout to FR
    if options.layoutFR is True:
        ChangeField(app_path, 'preferences.py', 'keyboard_layout', "azerty")
    else:
        ChangeField(app_path, 'preferences.py', 'keyboard_layout', "qwerty")

    # Change shebang for some files that can be used in terminal and use openCV
    for i in _list:
        if i[3] is True:
            ChangeSheBang(i[0], i[1], python_path)

    if sys.platform == 'linux':
        file_path = Path(app_path).joinpath("AMi_IA.desktop")
        lines = f'''[Desktop Entry]
    Name=AMi_Image_Analysis
    Comment=Run AMI_Image_Analysis
    Exec={Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")}
    Icon={Path(app_path).joinpath("AMi_IA.png")}
    Terminal=true
    Type=Application'''
        with open(file_path, 'w') as f:
            for l in lines:
                f.write(l)
        print(f'''
    ------------------------------------------------------
    If you want you can put an icon on your desktop by issuing the following command
    cp {file_path} {os.path.expanduser("~/Desktop")}/.
    ------------------------------------------------------''')

    if sys.platform == 'linux' or sys.platform == 'darwin':
        file_path = Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")
        print(f'''
    ------------------------------------------------------
    Recommended: create an alias in your .bashrc or .bash_profile with:
    alias AMI_IMage_Analysis='{file_path}'
    ------------------------------------------------------
    ''')
        CreateUninstall(app_path, python_path)

    print("\nInstallation Finished.\n")
    print("------------------------------------------------------")


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
