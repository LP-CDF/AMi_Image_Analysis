#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Initial repository https://github.com/tensorflow/models/tree/master/research/marco

# and adapted for AMi_Image_Analysis

import os, sys
from pathlib import Path
import tensorflow as tf
from utils import ensure_directory

""" 
usage: 
Processes all .jpg, .png, .bmp and .gif files found in the specified directory and its subdirectories.
 --PATH ( Path to directory of images or path to directory with subdirectory of images). e.g Path/To/Directory/
 --Model_PATH path to the tensorflow model
"""

def predict(file_list, classifications,logDir):
# def predict(image_directory, project_data):
    app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
    # print("app_path ", app_path)
    model_path = Path(app_path).joinpath("saved_model")
    size = len(file_list)
    def load_images(file_list):
        for i in file_list:
            file = open(i, "rb")
            yield {"image_bytes": [file.read()]}, i

    iterator = load_images(file_list)

    predicter = tf.contrib.predictor.from_saved_model(str(model_path))

    logresult=[]
    for _ in range(size):
        data, name = next(iterator)
        well=os.path.splitext(os.path.basename(name))[0]
        print("Processing File ", name)
        results = predicter(data)

        vals = results['scores'][0]
        classes = results['classes'][0]
        dictionary = dict(zip(classes,vals))
        
        # print("vals ", vals)
        # print("classes ", classes)
        # print("dictionary ", dictionary)
        
        logresult.append((well, dictionary))
        
        #Find the most probable and return a tuple(well,dict)
        MostProbable=max(zip(dictionary.values(),dictionary.keys()))
        # print("MostProbable ", MostProbable)

        classification = ""
        if MostProbable[1] == b"Crystals":
            classification = "Crystal"
        elif MostProbable[1] == b"Other":
            classification = "Other"
        elif MostProbable[1] == b"Precipitate":
            classification = "Precipitate"
        elif MostProbable[1] == b"Clear":
            classification = "Clear"

        classifications[well]=classification
        # print("classifications[well] ", classifications[well])
        
    log=Path(logDir).joinpath("auto_MARCO.log")
  
    with open(log, 'w') as f:
            f.write("%9s%15s%15s%17s%15s \n"%("WELL", "Pb_CRYSTAL", "Pb_OTHER", "Pb_Precipitate", "Pb_Clear"))
            for i in logresult: f.write("%9s%15.2f%15.2f%17.2f%15.2f \n"%(i[0],i[1][b"Crystals"]*100,i[1][b"Other"]*100,
                                                                          i[1][b"Precipitate"]*100,i[1][b"Clear"]*100))
    del dictionary, MostProbable, logresult       