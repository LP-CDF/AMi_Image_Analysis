#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:57:50 2020

"""

__date__ = "08-03-2021"

import os, sys
from pathlib import Path
import stat
from utils import _rawimages


def CreateUninstall(app_path, venv_path):
    '''Create a python script to remove program or most of it
    app_path and venv_path are string
    '''
    file_path=Path(app_path).joinpath("Uninstall.py")
    print(f"Creating uninstall script in {file_path}")
    content=f'''#!/usr/bin/env python3

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
    os.chmod(file_path, st.st_mode |  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def ChangeSheBang(app_path, filename, python_path):
    '''app_path and filename are strings'''
    file_path=Path(app_path).joinpath(filename)
    with open(file_path, 'r') as f:
        lines=f.readlines()
    lines[0]="#!"+ python_path+'/python \n'
    with open(file_path, 'w') as f:    
        for l in lines: f.write(l)
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode |  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)    

def ChangeRAW(app_path, filename,_string):
    '''app_path and filename are strings'''
    file_path=Path(app_path).joinpath(filename)
    with open(file_path, 'r') as f:
        lines=f.readlines()
    for i in lines:
        if "_rawimages=" in i:
            INDEX=lines.index(i)
            break
    lines[INDEX]='''_rawimages="%s"\n'''%_string
    with open(file_path, 'w') as f:    
        for l in lines: f.write(l)

activate_venv={'linux': 'activate', 'darwin': 'activate', 'win32': 'activate.bat'}[sys.platform]
python_path=os.path.join(os.path.dirname(sys.executable))

app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
file_path=Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")

with open(file_path, 'w') as f:
    f.write('''#!/usr/bin/env bash

#File generated with Setup_bin_VENV.py
virtenv="%s"
. ${virtenv}/%s

#DO NOT EDIT the next THREE LINES
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
parentdir="$(dirname "$DIR")"
python3 $parentdir/AMi_Image_Analysis.py

deactivate'''%(python_path, activate_venv))

#_list is [(path,filename,True/false for ChangeRaw, True/false for ChangeSheBang)]
_list=[(app_path,"utils.py",True, False),
       (app_path+'/tools/',"Merge_AllNewPlates.py", True, True),
       (app_path+'/tools/',"Merge_Zstack.py", True, True),
       (app_path+'/tools/',"SaveDiskSpace.py", True, True),
       (app_path,"autocrop.py", False, True),
       (app_path,"Check_Circle_detection.py", False, True)]

#Change _rawimages to adapt to maybe different but compatible microscope softwares
for i in _list:
    if i[2] is True: ChangeRAW(i[0], i[1],_rawimages)

st = os.stat(file_path)
os.chmod(file_path, st.st_mode |  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

#Change shebang for some files that can be used in terminal and use openCV
for i in _list:
    if i[3] is True: ChangeSheBang(i[0], i[1], python_path)

if sys.platform=='linux':
    file_path=Path(app_path).joinpath("AMi_IA.desktop")
    lines=f'''[Desktop Entry]
Name=AMi_Image_Analysis
Comment=Run AMI_Image_Analysis
Exec={Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")}
Icon={Path(app_path).joinpath("AMi_IA.png")}
Terminal=true
Type=Application'''
    with open(file_path, 'w') as f:
        for l in lines: f.write(l)
    print(f'''
------------------------------------------------------
If you want you can put an icon on your desktop by issuing the following command
cp {file_path} {os.path.expanduser("~/Desktop")}/.
------------------------------------------------------''')

if sys.platform=='linux' or sys.platform=='darwin':
    file_path=Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")
    print(f'''
------------------------------------------------------
Recommended: create an alias in your .bashrc or .bash_profile with:
alias AMI_IMage_Analysis='{file_path}'
------------------------------------------------------
''')
    CreateUninstall(app_path, python_path)

print("\nInstallation Finished.\n")
print("------------------------------------------------------")