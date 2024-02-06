#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 11:50:15 2023

@author: ludovic
"""

import sys
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
import preferences as pref

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

__version__ = "0.1"
__date__ = "13-12-2023"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        spacing=0.2
        fig.subplots_adjust(bottom=spacing)        
        super(MplCanvas, self).__init__(fig)
        
    def showBinGraphA(self,scores):
        '''Extract, bin and plot human scores for all well
        ie no subwell filtering'''
        graph=MplCanvas(self, width=5, height=5, dpi=100)
        graph.axes.set_xlabel("Score")
        graph.axes.set_ylabel("Counts")
        _ = list(filter(lambda val: val is not None,scores.values()))
        _data=np.array(_, dtype=int)
        
        #Using histograms
        # _bins = [n+0.5 for n in range(0, len(pref.scoreclass))]+[len(pref.scoreclass)]
        # graph.counts, graph.bins = np.histogram(_data, bins=_bins, range=(1,len(pref.scoreclass)))       
        # graph.axes.hist(_data, _bins, facecolor="blue", alpha=0.75, edgecolor='black', linewidth=1.2, width = 0.8)
       
        #Using bar
        graph.counts, graph.bins = np.histogram(_data, bins=len(pref.scoreclass), range=(1,len(pref.scoreclass)))
        _x = np.arange(len(graph.counts))
        graph.axes.bar(_x+1, graph.counts, facecolor="blue", alpha=0.75, edgecolor='black', linewidth=1.2, width = 0.8, align='center')
        graph.axes.set_xticks(_x+1)
        graph.axes.set_xticklabels(labels=pref.scoreclass, rotation=45, horizontalalignment='right', rotation_mode='anchor')
        graph.axes.set_title(f'Unclassified={len(scores)-len(_)} ({(len(scores)-len(_))/len(scores)*100:.1f}%)')
        graph.setWindowTitle("Manual Score Histogram")
        graph.show()