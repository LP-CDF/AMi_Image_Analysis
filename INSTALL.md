# Install

Please read this carefully before proceeding.

    The software was tested on:
    * linux CentOS 7 (PyQt5 (v5.9.2 and v5.12.1) and python3 (v3.6.8 and v3.7.3))
    * Raspbian 10 (on a Pi 3B+, not recommended)
    * macOS HighSierra

    Hopefully, it will run on other linux distributions, MacOS and Windows with minor installation tweaks.
    You will need a screen with minimum resolution of **1920*1080**.

    Download the latest released version and gunzip it or clone this repository with
    git clone https://github.com/LP-CDF/AMi_Image_Analysis AMi_Image_Analysis

    Dependencies:
    * Qt5
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
    * python3 -m pip install -r /whereveryouinstalled/requirements.txt (or requirements_Raspbian.txt)
    * If you use a virtual environment, make sure it is activated before using the script Setup_bin_VENV.py. This script will overwrite the file in 
      /whereveryouinstalled/bin/AMI_Image_Analysis.sh so that virtenv points to your virtual environment.
      If you don't use a virtual environment, **do not use** the script Setup_bin_VENV.py.

    Make the file /whereveryouinstalled/bin/AMI_Image_Analysis.sh executable, it is recommended to create an alias then 
    To start the program type in a bash terminal: 
    ./whereveryouinstalled/bin/AMI_Image_Analysis.sh
    or use your alias.

    If you have an AZERTY keyboard, comment/uncomment lines 18 or 19 in the file preferences.py.
    If you use a QWERTY keyboard, you should not have to do anything.

## Raspbian specific installation notes

   You will need to install the following distribution packages
   * libtiff5 libtiff5-dev python3-libtiff
   * gem-plugin-tiff
   * qt5-default qt5-image-formats-plugins qt5-style-plugins
   * libatlas-base-dev
   * libjasper-dev
   * libqtgui4
   * libqt4-test

To this end you can use the commands:
sudo apt-get install qt5-default qt5-style-plugins qt5-image-formats-plugins libtiff5 libtiff5-dev python3-libtiff gem-plugin-tiff -y
sudo apt-get install libatlas-base-dev libjasper-dev libqtgui4 libqt4-test -y

Then proceed with the installation procedure described previously.
If you want to have a working tensorflow installation on Raspbian after issuing the command
python3 -m pip install -r /whereveryouinstalled/requirements_Raspbian.txt (which does not install tensorflow)
you will have to do the following steps:
   * Download a tensorflow wheel for Raspbian at :
     https://github.com/lhelontra/tensorflow-on-arm/releases/tag/v1.14.0-buster/tensorflow-1.14.0-cpXX-none-linux_armv7l.whl
     (example: tensorflow-1.14.0-cp37-none-linux_armv7l.whl for python 3.7)
   * If you use a virtual environment, **ensure it is activated**. (source /wherever/you/want/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin/activate)
   * python3 -m pip install /whereyoudownloaded/file/tensorflow-1.14.0-cpXX-none-linux_armv7l.whl
   * Disable cloud in contrib (otherwise tensorflow breaks) by editing the file 
     /wherever/you/want/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/lib/python3.7/site-packages/tensorflow/contrib/\__init\__.py
     and change line 30
     **from**
     if os.name != "nt" and platform.machine() != "s390x":
     **to**
     if os.name != "nt" and platform.machine() != "armv7l":

Then autoMARCO should work though slowly at least on a Pi3B+.

# Known issues: 
    * If your graphics card is CUDA capable but with Cuda capability < 6, you must install tensorflow 1.14.0
    * If your CPU does not support AVX instruction sets (CPU before SandyBridge), you will need to find a tensorflow with the correct building options
      (have a look [here](https://github.com/yaroslavvb/tensorflow-community-wheels/issues)).
      Uninstall tensorflow and reinstall with python3 -m pip install pathToWheel.whl
      Or build yourself from source.
