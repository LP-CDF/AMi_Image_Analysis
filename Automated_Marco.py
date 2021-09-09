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
from PyQt5.QtWidgets import QProgressDialog
import preferences as pref

""" 
usage: 
Processes all .jpg, .png, .bmp and .gif files found in the specified directory and its subdirectories.
 --PATH ( Path to directory of images or path to directory with subdirectory of images). e.g Path/To/Directory/
 --Model_PATH path to the tensorflow model
"""

class Predictor():
    def __init__(self, parent=None):
        self.tensorflowOK=self.loadtensorflow()
    
    def loadtensorflow(self):
        '''check if tensorflow is available, checks version, must be below TF2'''
        try:
            import tensorflow as tf
            self.tfversion=tf.__version__
            if tf.__version__ <= '2.0.0': return True
            else: return False
        except: return False
        
    def createpredicter(self):
        if self.tensorflowOK is True: import tensorflow as tf
        else: return
        app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
        model_path = Path(app_path).joinpath("saved_model")
        predicter = tf.contrib.predictor.from_saved_model(str(model_path))
        return predicter

    def convertclassification(self,entry)->list:
        if entry[1] == b"Crystals":
            classification = "Crystal"
        elif entry[1] == b"Other":
            classification = "Other"
        elif entry[1] == b"Precipitate":
            classification = "Precipitate"
        elif entry[1] == b"Clear":
            classification = "Clear"
        return classification
        
    def predict(self,file_list, classifications,logDir, predicter):
        size = len(file_list)
        
        #unsupported image type in tensorflow <2.0
        unsupported=['.tif', '.tiff','.TIF', '.TIFF']
        
        def load_images(file_list):
            for i in file_list:
                if os.path.splitext(os.path.basename(i))[1] not in unsupported:
                    file = open(i, "rb")
                    yield {"image_bytes": [file.read()]}, i
    
        iterator = load_images(file_list)
    
        logresult=[]
        progress = QProgressDialog("Processing files...", "Abort", 0, size)
        progress.setWindowTitle("autoMARCO")
        progress.setMinimumWidth(300)
        progress.setModal(True)
        
        for _ in range(size):
            progress.setValue(_)
            data, name = next(iterator)
            well=os.path.splitext(os.path.basename(name))[0]
            # progress.setLabelText(f'''processing well: {well}''')
            print("Processing File ", name)
            results = predicter(data)
    
            vals = results['scores'][0]
            classes = results['classes'][0]
            dictionary = dict(zip(classes,vals))
            
            logresult.append((well, dictionary))
            
            #Find the most probable and return a tuple(well,dict)
            MostProbable=max(zip(dictionary.values(),dictionary.keys()))
            # print("MostProbable ", MostProbable)
    
            classification = self.convertclassification(MostProbable)
    
            #Adding a filter
            if MostProbable[0]<pref.autoMARCO_threshold:
                classification = "Unknown"
                
            classifications[well]=classification
            # print("classifications[well] ", classifications[well])
            if progress.wasCanceled():
                #To prevent crash assign classification to Unknown for unprocessed images
                for i in range(file_list.index(name), len(file_list)):
                    classifications[os.path.splitext(os.path.basename(file_list[i]))[0]]="Unknown"
                break
            
        log=Path(logDir).joinpath("auto_MARCO.log")
        
        # progress.setLabelText("Saving results to files")
        
        with open(log, 'w') as f:
                f.write("%9s%15s%15s%17s%15s \n"%("WELL", "Pb_CRYSTAL", "Pb_OTHER", "Pb_Precipitate", "Pb_Clear"))
                for i in logresult: f.write("%9s%15.3f%15.3f%17.3f%15.3f \n"%(i[0],i[1][b"Crystals"],i[1][b"Other"],
                                                                              i[1][b"Precipitate"],i[1][b"Clear"]))
        del dictionary, MostProbable, logresult     
    
    def single_predict(self,filepath, predicter):
        '''predict only one image
        TODO: update auto_MARCO.log'''
    
        # logresult=[]
        
        well=os.path.splitext(os.path.basename(filepath))[0]
        print("Processing File ", filepath)
        file = open(filepath, "rb")
        results = predicter({"image_bytes": [file.read()]})
    
        vals = results['scores'][0]
        classes = results['classes'][0]
    
        # for i in range(len(classes)):
        #     val=str(classes[i]).strip('b')
        #     val=val.replace("'","")
        #     classes[i]=val
        dictionary = dict(zip(classes,vals))
        
        #Find the most probable and return a tuple(well,dict)
        MostProbable=max(zip(dictionary.values(),dictionary.keys()))
        print("autoMARCO prediction:", dictionary)
        classification = self.convertclassification(MostProbable)
   
        return (classification, MostProbable[0])
        del MostProbable,dictionary,classification