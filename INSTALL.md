## Install

    The software was tested on:
    * linux CentOS 7 (PyQt5 (v5.9.2 and v5.12.1) and python3 (v3.6.8 and v3.7.3))
    * Raspbian 10 (on a Pi 3B+, not recommended)
    * macOS HighSierra

    Hopefully, it should work on other linux distributions, MacOS and Windows.
    You will need a screen with minimum resolution of 1920*1080.

    Download the latest released version and gunzip it or clone this repository with
    git clone https://github.com/LP-CDF/AMi_Image_Analysis AMi_Image_Analysis

    Dependencies:
    * PyQt5 (v5.9.2 or higher)
    * Python Imaging Library (Pillow, v6.2.1 or higher)
    * PyFPDF (v1.7.2 or higher)

    Optional dependencies:
    * TensorFlow (v1.1x, not v2, tested with version 1.14)
    * MARCO tensorflow model (https://storage.googleapis.com/marco-168219-model/savedmodel.zip)
      One version of this model is included in saved_model/
      Methodology details are published in [[2]](#2)
    * openCV for the automatic cropping tool (tested with opencv 4.0.1)
    * NumPy

    You may consider using a virtual environment to avoid python package conflict (recommended).

    To create a virtual environment with venv adapt the following commands:
    * python3 -m venv --without-pip /wherever/you/want/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1
    * source /wherever/you/want/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin/activate
    * curl https://bootstrap.pypa.io/get-pip.py | python
    * deactivate
    * source /wherever/you/want/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin/activate
    * python3 -m pip install -r /whereveryouinstalled/requirements.txt
    * edit the file in /whereveryouinstalled/bin/AMI_Image_Analysis.sh so that virtenv points to your virtual environment and uncomment lines 5, 6 and 13.
      If you don't use a virtual environment, leave lines 5, 6 and 13 commented.

    To use the correct shortcuts for your keyboard, update the file preferences.py
    and comment/uncomment lines 18 or 19 if you use an AZERTY keyboard.
    If using a QWERTY keyboard, you should not have to do anything.

    Make the file /whereveryouinstalled/bin/AMI_Image_Analysis.sh executable, it is recommended to create an alias then 
    To start the program type in a bash terminal: 
    ./whereveryouinstalled/bin/AMI_Image_Analysis.sh
    or use your alias.

    Known issues: 
     * On Raspbian, you must ensure that package qt5-image-formats-plugins is installed
     * On Raspbian, buttons do not change color when clicked.
     * If your graphics card is CUDA capable but with Cuda capability < 6, you must install tensorflow 1.14.0 not 1.15.0
