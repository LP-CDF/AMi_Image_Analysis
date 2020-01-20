#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:57:50 2020

@author: ludovic
"""

import os, sys
from pathlib import Path
import stat

activate_venv={'linux': 'activate', 'win32': 'activate.bat'}[sys.platform]
python_path=os.path.join(os.path.dirname(sys.executable))

app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
file_path=Path(app_path).joinpath("bin", "AMI_Image_Analysis.sh")


# print("PYTHON PATH: ", python_path)
# print("APP PATH : ", app_path)
# print("FILE PATH : ", file_path)

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

st = os.stat(file_path)
os.chmod(file_path, st.st_mode |  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)