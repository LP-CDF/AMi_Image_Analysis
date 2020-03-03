#!/usr/bin/env bash

#File generated with Setup_VENV.py
#virtenv="/usr/local/PROGRAMS/XTAL/GIT-AMi_Image_Analysis/python/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin"
#. ${virtenv}/activate

#DO NOT EDIT the next THREE LINES
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
parentdir="$(dirname "$DIR")"
python3 $parentdir/AMi_Image_Analysis.py

deactivate
