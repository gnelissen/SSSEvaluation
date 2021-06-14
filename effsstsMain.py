from __future__ import division
from PyQt5 import QtCore, QtGui, QtWidgets
import effssts
import random
import sys
import getopt
import numpy as np
from schedTest import tgPath, SCEDF, SCRM, EDA, PROPORTIONAL, NC, SEIFDA, Audsley, rad, PATH, mipx, combo, functions
from schedTest import RSS, UDLEDF, WLAEDF, RTEDF, UNIFRAMEWORK, FixedPriority, GMFPA, SRSR, Biondi, Uppaal
from effsstsPlot import effsstsPlot
import os
import datetime
import pickle
from multiprocessing import Pool

gSeed = datetime.datetime.now()
gPrefixdata = ''
gTasksetpath = ''
gRuntest = True
gPlotdata = True
gPlotall = True
gTaskChoice = ''
gNumberOfTaskSets = 100
gNumberOfTasksPerSet = 10
gUStart = 0
gUEnd = 100
gUStep = 5
gNumberOfSegs = 2
gSchemes = []
gSLenMinValue = 0.01
gSLenMaxValue = 0.1
gNumberofruns = 1
garwrap = []
gthread = 1

gmultiplot = ''
gmpCheck = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        choice_list = ['Generate Tasksets', 'Generate and Save Tasksets', 'Load Tasksets']
        choice_plot = ['Tasks per Set', 'Number of Segments', 'Suspension Length']



        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 660)



        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        
        self.groupBox_general = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_general.setGeometry(QtCore.QRect(12, 12, 1000, 100))
        self.groupBox_general.setObjectName("groupBox_general")

        self.runtests = QtWidgets.QCheckBox(self.groupBox_general)
        self.runtests.setGeometry(QtCore.QRect(12, 32, 91, 25))
        self.runtests.setChecked(True)
        self.runtests.setObjectName("runtests")

        self.combobox_input = QtWidgets.QComboBox(self.groupBox_general)
        self.combobox_input.setGeometry(QtCore.QRect(110, 32, 225, 25))
        self.combobox_input.setObjectName("combobox_input")
        self.combobox_input.addItems(choice_list)
        self.combobox_input.currentIndexChanged.connect(lambda: selectionchange(self.combobox_input))

        self.label_threadcount = QtWidgets.QLabel(self.groupBox_general)
        self.label_threadcount.setGeometry(QtCore.QRect(800, 32, 100, 25))
        self.label_threadcount.setObjectName("label_threadcount")

        self.threadcount = QtWidgets.QLineEdit(self.groupBox_general)
        self.threadcount.setGeometry(QtCore.QRect(895, 32, 95, 25))
        self.threadcount.setObjectName("threadcount")
        
        self.label_5 = QtWidgets.QLabel(self.groupBox_general)
        self.label_5.setGeometry(QtCore.QRect(12, 65, 115, 25))
        self.label_5.setObjectName("label_5")

        self.prefixdatapath = QtWidgets.QLineEdit(self.groupBox_general)
        self.prefixdatapath.setGeometry(QtCore.QRect(131, 65, 660, 25))
        self.prefixdatapath.setObjectName("prefixdatapath")

        self.label_seed = QtWidgets.QLabel(self.groupBox_general)
        self.label_seed.setGeometry(QtCore.QRect(800, 65, 40, 25))
        self.label_seed.setObjectName("label_seed")

        self.seed = QtWidgets.QLineEdit(self.groupBox_general)
        self.seed.setGeometry(QtCore.QRect(845, 65, 145, 25))
        self.seed.setObjectName("seed")

        self.loadtasks_title = QtWidgets.QLabel(self.groupBox_general)
        self.loadtasks_title.setGeometry(QtCore.QRect(350, 32, 140, 25))
        self.loadtasks_title.setObjectName("loadtasks_title")
        self.loadtasks_title.hide()

        self.tasksetdatapath = QtWidgets.QLineEdit(self.groupBox_general)
        self.tasksetdatapath.setGeometry(QtCore.QRect(490, 32, 500, 25))
        self.tasksetdatapath.setObjectName("tasksetdatapath")
        self.tasksetdatapath.hide()

        

        self.groupbox_configurations = QtWidgets.QGroupBox(self.centralwidget)
        self.groupbox_configurations.setGeometry(QtCore.QRect(12, 122, 1000, 100))
        self.groupbox_configurations.setObjectName("groupbox_configurations")

        self.label_6 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_6.setGeometry(QtCore.QRect(12, 32, 198, 25))
        self.label_6.setObjectName("label_6") # task sets per configuration

        self.tasksetsperconfig = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.tasksetsperconfig.setGeometry(QtCore.QRect(210, 32, 55, 25))
        self.tasksetsperconfig.setMaximum(1000)
        self.tasksetsperconfig.setProperty("value", 100)
        self.tasksetsperconfig.setObjectName("tasksetsperconfig")

        self.label_7 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_7.setGeometry(QtCore.QRect(12, 65, 198, 25))
        self.label_7.setObjectName("label_7") # tasks per set

        self.tasksperset = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.tasksperset.setGeometry(QtCore.QRect(210, 65, 55, 25))
        self.tasksperset.setMaximum(100)
        self.tasksperset.setProperty("value", 10)
        self.tasksperset.setObjectName("tasksperset")

        self.label_8 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_8.setGeometry(QtCore.QRect(275, 32, 155, 25))
        self.label_8.setObjectName("label_8") # utilization start value

        self.utilstart = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.utilstart.setGeometry(QtCore.QRect(435, 32, 55, 25))
        self.utilstart.setMaximum(100)
        self.utilstart.setProperty("value", 0)
        self.utilstart.setObjectName("utilstart")

        self.label_9 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_9.setGeometry(QtCore.QRect(275, 65, 155, 25))
        self.label_9.setObjectName("label_9") # utilization end value

        self.utilend = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.utilend.setGeometry(QtCore.QRect(435, 65, 55, 25)) #util end value
        self.utilend.setMaximum(100)
        self.utilend.setProperty("value", 100)
        self.utilend.setObjectName("utilend")

        self.label_11 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_11.setGeometry(QtCore.QRect(500, 32, 160, 25))
        self.label_11.setObjectName("label_11") # utilization step
        
        self.utilstep = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.utilstep.setGeometry(QtCore.QRect(660, 32, 55, 25))
        self.utilstep.setMaximum(100)
        self.utilstep.setProperty("value", 5)
        self.utilstep.setObjectName("utilstep")

        self.label_10 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_10.setGeometry(QtCore.QRect(500, 65, 155, 25))
        self.label_10.setObjectName("label_10") # num_of_segment

        self.numberofsegs = QtWidgets.QSpinBox(self.groupbox_configurations)
        self.numberofsegs.setGeometry(QtCore.QRect(660, 65, 55, 25))
        self.numberofsegs.setMaximum(100)
        self.numberofsegs.setProperty("value", 2)
        self.numberofsegs.setObjectName("numberofsegs")

        self.label = QtWidgets.QLabel(self.groupbox_configurations)
        self.label.setGeometry(QtCore.QRect(725, 32, 210, 25))
        self.label.setObjectName("label") # suspension length min value
        
        self.slengthminvalue = QtWidgets.QDoubleSpinBox(self.groupbox_configurations)
        self.slengthminvalue.setGeometry(QtCore.QRect(935, 32, 55, 25))
        self.slengthminvalue.setMaximum(1.0)
        self.slengthminvalue.setSingleStep(0.01)
        self.slengthminvalue.setProperty("value", 0.01)
        self.slengthminvalue.setObjectName("slengthminvalue")

        self.label_3 = QtWidgets.QLabel(self.groupbox_configurations)
        self.label_3.setGeometry(QtCore.QRect(725, 65, 210, 25)) 
        self.label_3.setObjectName("label_3") # suspension length max

        self.slengthmaxvalue = QtWidgets.QDoubleSpinBox(self.groupbox_configurations)
        self.slengthmaxvalue.setGeometry(QtCore.QRect(935, 65, 55, 25))
        self.slengthmaxvalue.setMaximum(1.0)
        self.slengthmaxvalue.setSingleStep(0.01)
        self.slengthmaxvalue.setProperty("value", 0.1)
        self.slengthmaxvalue.setObjectName("slengthmaxvalue")



        self.groupbox_schedulability_tests = QtWidgets.QGroupBox(self.centralwidget) #Schedulability tests
        self.groupbox_schedulability_tests.setGeometry(QtCore.QRect(12, 232, 1000, 228))
        self.groupbox_schedulability_tests.setObjectName("groupbox_schedulability_tests")



        self.groupBox_5 = QtWidgets.QGroupBox(self.groupbox_schedulability_tests) #FRD Segmented
        self.groupBox_5.setGeometry(QtCore.QRect(11, 24, 232, 190))
        self.groupBox_5.setObjectName("groupBox_5")

        self.scrollArea_5 = QtWidgets.QScrollArea(self.groupBox_5)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setGeometry(QtCore.QRect(0, 20, 232, 170))
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollArea_5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 212, 169))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")

        self.formLayoutWidget_5 = QtWidgets.QWidget(self.scrollAreaWidgetContents_5)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 212, 169))
        self.formLayoutWidget_5.setObjectName("formLayoutWidget_5")
        
        self.formLayout_5 = QtWidgets.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.formLayout_5.setObjectName("formLayout_5")

        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.scrollAreaWidgetContents_5.setLayout(self.formLayout_5)

        self.seifdamind = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.seifdamind.setObjectName("seifdamind")
        self.seifdamind.setToolTip('Shortest Execution Interval First Deadline Assignment - Picks the minimum x')
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.seifdamind)

        self.seifdamindg = QtWidgets.QSpinBox(self.formLayoutWidget_5)
        self.seifdamindg.setMaximum(5)
        self.seifdamindg.setProperty("value", 1)
        self.seifdamindg.setObjectName("seifdamindg")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.seifdamindg)

        self.seifdamaxd = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.seifdamaxd.setObjectName("seifdamaxd")
        self.seifdamaxd.setToolTip('Shortest Execution Interval First Deadline Assignment - Picks the maximum x')
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.seifdamaxd)

        self.seifdamaxdg = QtWidgets.QSpinBox(self.formLayoutWidget_5)
        self.seifdamaxdg.setMaximum(5)
        self.seifdamaxdg.setProperty("value", 1)
        self.seifdamaxdg.setObjectName("seifdamaxdg")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.seifdamaxdg)

        self.seifdapbmind = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.seifdapbmind.setObjectName("seifdapbmind")
        self.seifdapbmind.setToolTip('Shortest Execution Interval First Deadline Assignment - Proportionally-Bounded-Min x')
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.seifdapbmind)
        
        self.seifdapbmindg = QtWidgets.QSpinBox(self.formLayoutWidget_5)
        self.seifdapbmindg.setMaximum(5)
        self.seifdapbmindg.setProperty("value", 1)
        self.seifdapbmindg.setObjectName("seifdapbmindg")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.seifdapbmindg)

        self.eda = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.eda.setObjectName("eda")
        self.eda.setToolTip('Equal relative Deadline Assignment (EDA)') 
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.eda)

        self.proportional = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.proportional.setObjectName("proportional")
        self.proportional.setToolTip('Proportional relative deadline assignment')
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.proportional)

        self.seifdamip = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.seifdamip.setObjectName("seifdamip")
        self.seifdamip.setToolTip('Shortest Execution Interval First Deadline Assignment - MILP')
        self.formLayout_5.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.seifdamip)

        self.gmfpa = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.gmfpa.setObjectName("gmfpa")
        self.gmfpa.setToolTip('Generalized Multiframe Task Model with Parameter Adaptation - Set granularity of time steps')
        self.formLayout_5.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.gmfpa)

        self.gmfpag = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_5)
        self.gmfpag.setMaximum(1.0)
        self.gmfpag.setSingleStep(0.01)
        self.gmfpag.setProperty("value", 0.5)
        self.gmfpag.setObjectName("gmfpag")
        self.formLayout_5.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.gmfpag)



        self.groupBox = QtWidgets.QGroupBox(self.groupbox_schedulability_tests)  #FRD Hybrid
        self.groupBox.setGeometry(QtCore.QRect(253, 24, 217, 190))
        self.groupBox.setObjectName("groupBox")

        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(QtCore.QRect(0, 20, 217, 170))
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 217, 169))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.formLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 217, 169))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.formLayout)

        self.pathminddd = QtWidgets.QCheckBox(self.groupBox)
        self.pathminddd.setObjectName("pathminddd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pathminddd)

        self.pathminddd.setToolTip('Pattern Oblivious Individual Upper Bounds')
        self.pathmindddg = QtWidgets.QSpinBox(self.groupBox)
        self.pathmindddg.setMaximum(5)
        self.pathmindddg.setProperty("value", 1)
        self.pathmindddg.setObjectName("pathmindddg")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pathmindddg)

        self.pathminddnd = QtWidgets.QCheckBox(self.groupBox)
        self.pathminddnd.setObjectName("pathminddnd")
        self.pathminddnd.setToolTip('Pattern-Clairvoyant Shorter Segment Shorter Deadline')
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pathminddnd)

        self.pathminddndg = QtWidgets.QSpinBox(self.groupBox)
        self.pathminddndg.setMaximum(5)
        self.pathminddndg.setProperty("value", 1)
        self.pathminddndg.setObjectName("pathminddndg")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pathminddndg)

        self.pathpbminddd = QtWidgets.QCheckBox(self.groupBox)
        self.pathpbminddd.setObjectName("pathpbminddd")
        self.pathpbminddd.setToolTip('Pattern-Oblivious Multiple Paths')
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pathpbminddd)

        self.pathpbmindddg = QtWidgets.QSpinBox(self.groupBox)
        self.pathpbmindddg.setMaximum(5)
        self.pathpbmindddg.setProperty("value", 1)
        self.pathpbmindddg.setObjectName("pathpbmindddg")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pathpbmindddg)

        self.pathpbminddnd = QtWidgets.QCheckBox(self.groupBox)
        self.pathpbminddnd.setObjectName("pathpbminddnd")
        self.pathpbminddnd.setToolTip('Pattern-Clairvoyant Proportional Deadline with A Bias')
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.pathpbminddnd)

        self.pathpbminddndg = QtWidgets.QSpinBox(self.groupBox)
        self.pathpbminddndg.setMaximum(5)
        self.pathpbminddndg.setProperty("value", 1)
        self.pathpbminddndg.setObjectName("pathpbminddndg")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pathpbminddndg)



        self.groupBox_4 = QtWidgets.QGroupBox(self.groupbox_schedulability_tests) #Segmented
        self.groupBox_4.setGeometry(QtCore.QRect(480, 24, 170, 190))
        self.groupBox_4.setObjectName("groupBox_4")
        
        self.scrollArea_4 = QtWidgets.QScrollArea(self.groupBox_4)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setGeometry(QtCore.QRect(0, 20, 170, 170))
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollArea_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 170, 169))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")

        self.formLayoutWidget_4 = QtWidgets.QWidget(self.scrollAreaWidgetContents_4)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 170, 169))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")

        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.scrollAreaWidgetContents_4.setLayout(self.formLayout_4)

        self.scedf = QtWidgets.QCheckBox(self.groupBox_4)
        self.scedf.setObjectName("scedf")
        self.scedf.setToolTip('Suspension as Computation Earliest-Deadline-First (SCEDF)')
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.scedf)

        self.scrm = QtWidgets.QCheckBox(self.groupBox_4)
        self.scrm.setObjectName("scrm")
        self.scrm.setToolTip('Suspension as Computation Rate-Monotonic (SCRM)')
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.scrm)
        
        self.scairrm = QtWidgets.QCheckBox(self.groupBox_4)
        self.scairrm.setObjectName("scairrm")
        self.scairrm.setToolTip('Suspension as Computation (SC) and As Interference Restarts (AIR) Rate-Monotonic (RM)')
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.scairrm)
        
        self.scairopa = QtWidgets.QCheckBox(self.groupBox_4)
        self.scairopa.setObjectName("scairopa")
        self.scairopa.setToolTip('Suspension as Computation (SC) and As Interference Restarts (AIR) Optimal Priority Assignment (OPA) ')
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.scairopa)
        
        self.frdgmfopa = QtWidgets.QCheckBox(self.groupBox_4)
        self.frdgmfopa.setObjectName("frdgmfopa")
        self.frdgmfopa.setToolTip('Fixed Relative Deadline (FRD) and Generalized Multiframe (GMF) Optimal Priority Assignment (OPA) ')
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.frdgmfopa)
        
        self.biondi = QtWidgets.QCheckBox(self.groupBox_4)
        self.biondi.setObjectName("Biondi")
        self.biondi.setToolTip('Alessandros Method. Biondi (RTSS 2016)')
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.biondi)
        
        self.srsr = QtWidgets.QCheckBox(self.groupBox_4)
        self.srsr.setObjectName("srsr")
        self.srsr.setToolTip('Schedulability Analysis with synchronous release sequence refinement')
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.srsr)



        self.groupBox_8 = QtWidgets.QGroupBox(self.groupbox_schedulability_tests) #Dynamic
        self.groupBox_8.setGeometry(QtCore.QRect(660, 24, 170, 190))
        self.groupBox_8.setObjectName("groupBox_8")

        self.scrollArea_8 = QtWidgets.QScrollArea(self.groupBox_8)
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollArea_8.setGeometry(QtCore.QRect(0, 20, 170, 170))
        self.scrollArea_8.setObjectName("scrollArea_8")
        self.scrollArea_8.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_8.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_8 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QtCore.QRect(0, 0, 170, 169))
        self.scrollAreaWidgetContents_8.setObjectName("scrollAreaWidgetContents_8")

        self.formLayoutWidget_8 = QtWidgets.QWidget(self.scrollAreaWidgetContents_8)
        self.formLayoutWidget_8.setGeometry(QtCore.QRect(0, 0, 170, 169))
        self.formLayoutWidget_8.setObjectName("formLayoutWidget_8")
        
        self.formLayout_8 = QtWidgets.QFormLayout(self.formLayoutWidget_8)
        self.formLayout_8.setContentsMargins(0, 0, 0, 0)
        self.formLayout_8.setObjectName("formLayout_8")

        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")

        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)
        self.scrollAreaWidgetContents_8.setLayout(self.formLayout_8)

        self.passopa = QtWidgets.QCheckBox(self.groupBox_8)
        self.passopa.setObjectName("passopa")
        self.passopa.setToolTip('Priority Assignment algorithm for Self-Suspending Systems - Optimal-Priority Assignment')
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passopa)

        self.rss = QtWidgets.QCheckBox(self.groupBox_8)
        self.rss.setObjectName("rss")
        self.rss.setToolTip('Utilization-based Schedulability Test')
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rss)
        
        self.udledf = QtWidgets.QCheckBox(self.groupBox_8)
        self.udledf.setObjectName("udledf")
        self.udledf.setToolTip('')
        self.formLayout_8.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.udledf)
        
        self.wlaedf = QtWidgets.QCheckBox(self.groupBox_8)
        self.wlaedf.setObjectName("wlaedf")
        self.wlaedf.setToolTip('Workload-based Schedulability Test')
        self.formLayout_8.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.wlaedf)
        
        self.rtedf = QtWidgets.QCheckBox(self.groupBox_8)
        self.rtedf.setObjectName("rtedf")
        self.rtedf.setToolTip('Response-Time-Based Schedulability Test')
        self.formLayout_8.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.rtedf)
        
        self.uniframework = QtWidgets.QCheckBox(self.groupBox_8)
        self.uniframework.setObjectName("uniframework")
        self.uniframework.setToolTip('Unified Response Time Analysis Framework')
        self.formLayout_8.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.uniframework)
        
        self.suspobl = QtWidgets.QCheckBox(self.groupBox_8)
        self.suspobl.setObjectName("suspobl")
        self.suspobl.setToolTip('Suspension Oblivious')
        self.formLayout_8.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.suspobl)

        self.suspjit = QtWidgets.QCheckBox(self.groupBox_8)
        self.suspjit.setObjectName("suspjit")
        self.suspjit.setToolTip('Schedulability with Suspension as Jitter')
        self.formLayout_8.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.suspjit)

        self.suspblock = QtWidgets.QCheckBox(self.groupBox_8)
        self.suspblock.setObjectName("suspblock")
        self.suspblock.setToolTip('Schedulability with Suspension as Blocking Time')
        self.formLayout_8.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.suspblock)

        self.uppaal = QtWidgets.QCheckBox(self.groupBox_8)
        self.uppaal.setObjectName("uppaal")
        self.uppaal.setToolTip('Exact Schedulability Test for Non-Preemptive Self-Suspending Real-Time Tasks with UPPAAL model checker')
        self.formLayout_8.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.uppaal)



        self.groupBox_6 = QtWidgets.QGroupBox(self.groupbox_schedulability_tests) #General
        self.groupBox_6.setGeometry(QtCore.QRect(840, 24, 150, 190))
        self.groupBox_6.setObjectName("groupBox_6")

        self.scrollArea_6 = QtWidgets.QScrollArea(self.groupBox_6)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setGeometry(QtCore.QRect(0, 20, 150, 170))
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollArea_6.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_6.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 170, 169))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")

        self.formLayoutWidget_6 = QtWidgets.QWidget(self.scrollAreaWidgetContents_6)
        self.formLayoutWidget_6.setGeometry(QtCore.QRect(0, 0, 170, 169))
        self.formLayoutWidget_6.setObjectName("formLayoutWidget_6")
        
        self.formLayout_6 = QtWidgets.QFormLayout(self.formLayoutWidget_6)
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.formLayout_6.setObjectName("formLayout_6")

        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.scrollAreaWidgetContents_6.setLayout(self.formLayout_6)

        self.nc = QtWidgets.QCheckBox(self.groupBox_6)
        self.nc.setObjectName("nc")
        self.nc.setToolTip('Necessary Condition')
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.nc)



        self.groupbox_plots = QtWidgets.QGroupBox(self.centralwidget)  # multi plot
        self.groupbox_plots.setGeometry(QtCore.QRect(12, 470, 1000, 130))
        self.groupbox_plots.setObjectName("groupbox_plots")
        
        self.plotdata = QtWidgets.QCheckBox(self.groupbox_plots)
        self.plotdata.setGeometry(QtCore.QRect(12, 30, 160, 25))
        self.plotdata.setChecked(True)
        self.plotdata.setObjectName("plotdata")

        self.plotall = QtWidgets.QCheckBox(self.groupbox_plots)
        self.plotall.setGeometry(QtCore.QRect(172, 30, 180, 25))
        self.plotall.setChecked(True)
        self.plotall.setObjectName("plotall")

        self.mp_check = QtWidgets.QCheckBox(self.groupbox_plots)
        self.mp_check.setGeometry(QtCore.QRect(12, 63, 190, 25))
        self.mp_check.setObjectName("mp_check")
        self.mp_check.setToolTip('Plots')
        self.mp_check.stateChanged.connect(lambda: selectionchange_plot(self.combobox_plot))

        self.label_mp_control = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp_control.setGeometry(QtCore.QRect(211, 63, 130, 25))
        self.label_mp_control.setObjectName("label_mp")

        self.combobox_plot = QtWidgets.QComboBox(self.groupbox_plots)
        self.combobox_plot.setGeometry(QtCore.QRect(351, 63, 180, 25))
        self.combobox_plot.setObjectName("combobox_plot")
        self.combobox_plot.addItems(choice_plot)
        self.combobox_plot.currentIndexChanged.connect(lambda: selectionchange_plot(self.combobox_plot))

        self.label_mp = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp.setGeometry(QtCore.QRect(12, 96, 50, 25))
        self.label_mp.setObjectName("label_mp")

        self.tasksperset_p1 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.tasksperset_p1.setGeometry(QtCore.QRect(74, 96, 50, 25))
        self.tasksperset_p1.setMaximum(100)
        self.tasksperset_p1.setProperty("value", 10)
        self.tasksperset_p1.setObjectName("tasksperset")

        self.tasksperset_p2 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.tasksperset_p2.setGeometry(QtCore.QRect(136, 96, 50, 25))
        self.tasksperset_p2.setMaximum(100)
        self.tasksperset_p2.setProperty("value", 10)
        self.tasksperset_p2.setObjectName("tasksperset")

        self.tasksperset_p3 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.tasksperset_p3.setGeometry(QtCore.QRect(198, 96, 50, 25))
        self.tasksperset_p3.setMaximum(100)
        self.tasksperset_p3.setProperty("value", 10)
        self.tasksperset_p3.setObjectName("tasksperset")

        self.numberofsegs_p1 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.numberofsegs_p1.setGeometry(QtCore.QRect(74, 96, 50, 25))
        self.numberofsegs_p1.setMaximum(100)
        self.numberofsegs_p1.setProperty("value", 2)
        self.numberofsegs_p1.setObjectName("numberofsegs")

        self.numberofsegs_p2 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.numberofsegs_p2.setGeometry(QtCore.QRect(136, 96, 50, 25))
        self.numberofsegs_p2.setMaximum(100)
        self.numberofsegs_p2.setProperty("value", 2)
        self.numberofsegs_p2.setObjectName("numberofsegs")

        self.numberofsegs_p3 = QtWidgets.QSpinBox(self.groupbox_plots)
        self.numberofsegs_p3.setGeometry(QtCore.QRect(198, 96, 50, 25))
        self.numberofsegs_p3.setMaximum(100)
        self.numberofsegs_p3.setProperty("value", 2)
        self.numberofsegs_p3.setObjectName("numberofsegs")

        self.label_mp_max = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp_max.setGeometry(QtCore.QRect(12, 96, 80, 25))
        self.label_mp_max.setObjectName("label_mp_max")
        self.label_mp_max.hide()

        self.slengthmaxvalue_p1 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthmaxvalue_p1.setGeometry(QtCore.QRect(104, 96, 55, 25))
        self.slengthmaxvalue_p1.setMaximum(1.0)
        self.slengthmaxvalue_p1.setSingleStep(0.01)
        self.slengthmaxvalue_p1.setProperty("value", 0.1)
        self.slengthmaxvalue_p1.setObjectName("slengthmaxvalue")

        self.slengthmaxvalue_p2 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthmaxvalue_p2.setGeometry(QtCore.QRect(171, 96, 55, 25))
        self.slengthmaxvalue_p2.setMaximum(1.0)
        self.slengthmaxvalue_p2.setSingleStep(0.01)
        self.slengthmaxvalue_p2.setProperty("value", 0.1)
        self.slengthmaxvalue_p2.setObjectName("slengthmaxvalue")
        
        self.slengthmaxvalue_p3 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthmaxvalue_p3.setGeometry(QtCore.QRect(238, 96, 55, 25))
        self.slengthmaxvalue_p3.setMaximum(1.0)
        self.slengthmaxvalue_p3.setSingleStep(0.01)
        self.slengthmaxvalue_p3.setProperty("value", 0.1)
        self.slengthmaxvalue_p3.setObjectName("slengthmaxvalue")

        self.label_mp_min = QtWidgets.QLabel(self.groupbox_plots)
        self.label_mp_min.setGeometry(QtCore.QRect(305, 96, 80, 25))
        self.label_mp_min.setObjectName("label_mp_max")
        self.label_mp_min.hide()

        self.slengthminvalue_p1 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthminvalue_p1.setGeometry(QtCore.QRect(397, 96, 55, 25))
        self.slengthminvalue_p1.setMaximum(1.0)
        self.slengthminvalue_p1.setSingleStep(0.01)
        self.slengthminvalue_p1.setProperty("value", 0.01)
        self.slengthminvalue_p1.setObjectName("slengthminvalue")

        self.slengthminvalue_p2 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthminvalue_p2.setGeometry(QtCore.QRect(464, 96, 55, 25))
        self.slengthminvalue_p2.setMaximum(1.0)
        self.slengthminvalue_p2.setSingleStep(0.01)
        self.slengthminvalue_p2.setProperty("value", 0.01)
        self.slengthminvalue_p2.setObjectName("slengthminvalue")

        self.slengthminvalue_p3 = QtWidgets.QDoubleSpinBox(self.groupbox_plots)
        self.slengthminvalue_p3.setGeometry(QtCore.QRect(531, 96, 55, 25))
        self.slengthminvalue_p3.setMaximum(1.0)
        self.slengthminvalue_p3.setSingleStep(0.01)
        self.slengthminvalue_p3.setProperty("value", 0.01)
        self.slengthminvalue_p3.setObjectName("slengthminvalue")

        for i in range(1, 4):
            slmax = 'slengthmaxvalue_p' + str(i)
            slmin = 'slengthminvalue_p' + str(i)
            numseg = 'numberofsegs_p' + str(i)
            a = getattr(self, slmax)
            b = getattr(self, slmin)
            c = getattr(self, numseg)
            a.hide()
            b.hide()
            c.hide()
            
        self.label_mp_control.hide()
        self.combobox_plot.hide()
        self.label_mp.hide()
    
        self.tasksperset_p1.hide()
        self.tasksperset_p2.hide()
        self.tasksperset_p3.hide()
        self.numberofsegs_p1.hide()
        self.numberofsegs_p2.hide()
        self.numberofsegs_p3.hide()
        self.label_mp_max.hide()
        self.slengthmaxvalue_p1.hide()
        self.slengthmaxvalue_p2.hide()
        self.slengthmaxvalue_p3.hide()
        self.label_mp_min.hide()
        self.slengthminvalue_p1.hide()
        self.slengthminvalue_p2.hide()
        self.slengthminvalue_p3.hide()
        
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setToolTip('Button to run the settings')
        self.run.setGeometry(QtCore.QRect(812, 610, 200, 25))
        self.run.setObjectName("run")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setToolTip('Exit the framework')
        self.exit.setGeometry(QtCore.QRect(12, 610, 200, 25))
        self.exit.setObjectName("exit")



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1030, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionFramework_Help = QtWidgets.QAction(MainWindow)
        self.actionFramework_Help.setObjectName("actionFramework_Help")
        self.actionAbout_Framework = QtWidgets.QAction(MainWindow)
        self.actionAbout_Framework.setObjectName("actionAbout_Framework")




        def clickMethod(self):
            global gPrefixdata
            global gRuntest
            global gPlotdata
            global gNumberOfTaskSets
            global gNumberOfTasksPerSet
            global gUStart
            global gUEnd
            global gUStep
            global gNumberOfSegs
            global gSchemes
            global gSLenMinValue
            global gSLenMaxValue
            global gPlotall
            global gTaskChoice
            global gmpCheck

            del gSchemes[:]
            setSchemes()

            #print gSchemes


        def selectionchange(com_b):
            if com_b.currentText() == 'Load Tasksets':
                self.loadtasks_title.show()
                self.tasksetdatapath.show()
            else:
                self.loadtasks_title.hide()
                self.tasksetdatapath.hide()


        def selectionchange_plot( com_b):

            
            if not(self.mp_check.isChecked()):
                self.label_mp_control.hide()
                self.combobox_plot.hide()
                self.label_mp.hide()
            
                self.tasksperset_p1.hide()
                self.tasksperset_p2.hide()
                self.tasksperset_p3.hide()
                self.numberofsegs_p1.hide()
                self.numberofsegs_p2.hide()
                self.numberofsegs_p3.hide()
                self.label_mp_max.hide()
                self.slengthmaxvalue_p1.hide()
                self.slengthmaxvalue_p2.hide()
                self.slengthmaxvalue_p3.hide()
                self.label_mp_min.hide()
                self.slengthminvalue_p1.hide()
                self.slengthminvalue_p2.hide()
                self.slengthminvalue_p3.hide()
            else:
                self.label_mp_control.show()
                self.combobox_plot.show()
                self.label_mp.show()


                if com_b.currentText() =='Suspension Length':
                    self.label_mp_max.show()
                    self.label_mp_min.show()
                    self.label_mp.hide()
                else:
                    self.label_mp_max.hide()
                    self.label_mp_min.hide()
                    self.label_mp.show()
        
                for i in range(1, 4):
                    slmax = 'slengthmaxvalue_p' + str(i)
                    slmin = 'slengthminvalue_p' + str(i)
                    numseg = 'numberofsegs_p' + str(i)
                    numtasks = 'tasksperset_p' + str(i)

                    aslmax = getattr(self, slmax)
                    aslmin = getattr(self, slmin)
                    anums = getattr(self, numseg)
                    anumt = getattr(self, numtasks)
                    if com_b.currentText() == 'Tasks per Set':
                        aslmax.hide()
                        aslmin.hide()
                        anums.hide()
                        anumt.show()
                    elif com_b.currentText() == 'Number of Segments':
                        aslmax.hide()
                        aslmin.hide()
                        anums.show()
                        anumt.hide()
                    elif com_b.currentText() == 'Suspension Length':
                        aslmax.show()
                        aslmin.show()
                        anums.hide()
                        anumt.hide()   

        def clickexit(self):
            app.quit()

        self.run.clicked.connect(clickMethod)
        self.exit.clicked.connect(clickexit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def setSchemes():
            global gPrefixdata
            global gTasksetpath
            global gRuntest
            global gPlotdata
            global gNumberOfTaskSets
            global gNumberOfTasksPerSet
            global gUStart
            global gUEnd
            global gUStep
            global gNumberOfSegs
            global gSchemes
            global gSLenMinValue
            global gSLenMaxValue
            global gPlotall
            global gSeed
            global gTaskChoice
            global garwrap
            global gthread

            global gmultiplot
            global gmpCheck

            ###GENERAL###
            gRuntest = self.runtests.isChecked()
            gPlotdata = self.plotdata.isChecked()
            gPlotall = self.plotall.isChecked()
            gTaskChoice = self.combobox_input.currentText()

            gPrefixdata = self.prefixdatapath.text()
            gTasksetpath = self.tasksetdatapath.text()

            ###CONFIGURATION###
            gNumberOfTaskSets = self.tasksetsperconfig.value()
            gNumberOfTasksPerSet = self.tasksperset.value()
            gUStart = self.utilstart.value()
            gUEnd = self.utilend.value()
            gUStep = self.utilstep.value()
            gNumberOfSegs = self.numberofsegs.value()
            gSLenMinValue = self.slengthminvalue.value()
            gSLenMaxValue = self.slengthmaxvalue.value()
            if self.seed.text() != '':
                gSeed = self.seed.text()
            else:
                gSeed = datetime.datetime.now()
            if self.threadcount.text() != '':
                gthread = int(self.threadcount.text())
            else:
                gthread = 1
            ###MultiPlot###
            gmultiplot = self.combobox_plot.currentText()
            if gmultiplot == 'Tasks per Set':
                garwrap = [self.tasksperset_p1.value(), self.tasksperset_p2.value(), self.tasksperset_p3.value()]
            elif gmultiplot == 'Number of Segments':
                garwrap = [self.numberofsegs_p1.value(), self.numberofsegs_p2.value(), self.numberofsegs_p3.value()]
            elif gmultiplot == 'Suspension Length':
                garwrap = [self.slengthminvalue_p1.value(), self.slengthminvalue_p2.value(), self.slengthminvalue_p3.value(),
                           self.slengthmaxvalue_p1.value(), self.slengthmaxvalue_p2.value(), self.slengthmaxvalue_p3.value()]
            gmpCheck = self.mp_check.isChecked()

            #khchen init error window and fill in the concept later
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)

            ###SCHEDULABILITY TESTS###
            if self.seifdamind.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdamind.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-minD test fails")
                    error_msg.setInformativeText('SEIFDA-minD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-minD-' + str(self.seifdamindg.value()))
            if self.seifdamaxd.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdamaxd.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-maxD test fails")
                    error_msg.setInformativeText('SEIFDA-maxD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-maxD-' + str(self.seifdamaxdg.value()))
            if self.seifdapbmind.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdapbmind.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-PBminD test fails")
                    error_msg.setInformativeText('SEIFDA-PBminD does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-PBminD-' + str(self.seifdapbmindg.value()))
            if self.seifdamip.isChecked():
                if gNumberOfSegs > 2:
                    self.seifdamip.setChecked(False)
                    error_msg.setWindowTitle("SEIFDA-MILP test fails")
                    error_msg.setInformativeText('SEIFDA-MILP does not work for more than two segements.')
                    error_msg.exec_()
                else:
                    gSchemes.append('SEIFDA-MILP')
            if self.eda.isChecked():
                gSchemes.append('EDA')
            if self.proportional.isChecked():
                gSchemes.append('PROPORTIONAL')
            if self.nc.isChecked():
                if gNumberOfSegs > 2:
                    self.nc.setChecked(False)
                    error_msg = QtWidgets.QMessageBox()
                    error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                    error_msg.setWindowTitle("NC won't work!")
                    error_msg.setInformativeText('Necessary Condition does not work for more than two segements.')
                    #error_msg.setDetailedText("Necessary Condition only works for two segements of computation.")
                    error_msg.exec_()
                else:
                    gSchemes.append('NC')
            if self.biondi.isChecked():
                gSchemes.append('Biondi')
            if self.passopa.isChecked():
                gSchemes.append('PASS-OPA')
            if self.scedf.isChecked():
                gSchemes.append('SCEDF')
            if self.scrm.isChecked():
                gSchemes.append('SCRM')
            if self.scairrm.isChecked():
                gSchemes.append('SCAIR-RM')
            if self.scairopa.isChecked():
                gSchemes.append('SCAIR-OPA')
            if self.frdgmfopa.isChecked():
                gSchemes.append('FRDGMF-OPA')
            if self.pathminddd.isChecked():
                gSchemes.append(
                    'PATH-minD-' + str(self.pathmindddg.value()) + '-D=D')
            if self.pathminddnd.isChecked():
                gSchemes.append(
                    'PATH-minD-' + str(self.pathminddndg.value()) + '-DnD')
            if self.pathpbminddd.isChecked():
                gSchemes.append('PATH-PBminD-' + str(self.pathpbmindddg.value()) + '-D=D')
            if self.pathpbminddnd.isChecked():
                gSchemes.append('PATH-PBminD-' + str(self.pathpbminddndg.value()) + '-DnD')
            #hteper
            if self.rss.isChecked():
                gSchemes.append('RSS')
            if self.udledf.isChecked():
                gSchemes.append('UDLEDF')
            if self.wlaedf.isChecked():
                gSchemes.append('WLAEDF')
            if self.rtedf.isChecked():
                gSchemes.append('RTEDF')
            if self.uniframework.isChecked():
                gSchemes.append('UNIFRAMEWORK')
            if self.suspobl.isChecked():
                gSchemes.append('SUSPOBL')
            if self.suspjit.isChecked():
                gSchemes.append('SUSPJIT')
            if self.suspblock.isChecked():
                gSchemes.append('SUSPBLOCK')
            if self.uppaal.isChecked():
                gSchemes.append('UPPAAL')
            if self.gmfpa.isChecked():
                gSchemes.append('GMFPA-' + str(self.gmfpag.value()))
            if self.srsr.isChecked():
                if gNumberOfSegs > 2:
                    self.srsr.setChecked(False)
                    error_msg = QtWidgets.QMessageBox()
                    error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                    error_msg.setWindowTitle("SRSR won't work!")
                    error_msg.setInformativeText('Necessary Condition does not work for more than two segements.')
                    #error_msg.setDetailedText("Necessary Condition only works for two segements of computation.")
                    error_msg.exec_()
                else:
                    gSchemes.append('SRSR')

            if gRuntest:
                #khchen
                if len(gSchemes) != 0:
                    try:
                        tasksets_util = tasksetConfiguration()
                        MainWindow.statusBar().showMessage('Testing the given configurations...')
                        schedulabilityTest(tasksets_util)
                        MainWindow.statusBar().showMessage('Finish')
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no selection to test.')

            if gPlotdata:
                if len(gSchemes) != 0:
                    try:
                        effsstsPlot.effsstsPlotAll(gPrefixdata, gPlotall, gSchemes, gSLenMinValue, gSLenMaxValue, gNumberOfSegs,
                                                   gUStart, gUEnd, gUStep, gNumberOfTasksPerSet)
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no plot to draw.')
            if gmpCheck:
                if len(gSchemes) != 0:
                    try:
                        effsstsPlot.effsstsPlotAllmulti(gPrefixdata, gPlotall, gmultiplot, garwrap, gSchemes, gSLenMinValue, gSLenMaxValue, gNumberOfSegs,
                                                   gUStart, gUEnd, gUStep, gNumberOfTasksPerSet)
                    except Exception as e:
                        MainWindow.statusBar().showMessage(str(e))
                else:
                    MainWindow.statusBar().showMessage('There is no plot to draw.')

            #MainWindow.statusBar().showMessage('Ready')


        def tasksetConfiguration():
            global gNumberOfTaskSets
            global gNumberOfTasksPerSet
            global gUStep
            global gUStart
            global gUEnd
            global gSLenMaxValue
            global gSLenMinValue
            global gNumberOfSegs
            global gSeed

            tasksets_difutil = []

            
            random.seed(gSeed)

            if gTaskChoice == 'Generate Tasksets' or gTaskChoice == 'Generate and Save Tasksets':
                # khchen original code
                #y = np.zeros(int(100 / gUStep) + 1)
                #for u in range(0, len(y), 1):

                y = np.zeros(int((gUEnd-gUStart) / gUStep) + 1)

                for u in range(gUStart, gUEnd, gUStep):
                    tasksets = []
                    for i in range(0, gNumberOfTaskSets, 1):
                        #percentageU = u * gUStep / 100
                        percentageU = u / 100
                        tasks = tgPath.taskGeneration_p(gNumberOfTasksPerSet, percentageU, gSLenMinValue, gSLenMaxValue, vRatio=1,
                                                        seed=gSeed, numLog=int(2), numsegs=gNumberOfSegs)
                        sortedTasks = sorted(tasks, key=lambda item: item['period'])
                        tasksets.append(sortedTasks)
                    tasksets_difutil.append(tasksets)
                if gTaskChoice == 'Generate and Save Tasksets':
                    file_name = 'TspCon_'+ str(gNumberOfTaskSets) + '_TpTs_' \
                                + str(gNumberOfTasksPerSet) + '_Utilst_' + str(gUStep) +\
                                '_Minss_' + str(gSLenMinValue) + '_Maxss_' + \
                                str(gSLenMaxValue) + '_Seg_'+str(gNumberOfSegs)+'_.pkl'
                    MainWindow.statusBar().showMessage('File saved as: ' + file_name)
                    info = [gNumberOfTaskSets, gNumberOfTasksPerSet, gUStep, gSLenMinValue, gSLenMaxValue, gNumberOfSegs, gSeed ]
                    with open('./genTasksets/'+file_name, 'wb') as f:
                        pickle.dump([tasksets_difutil,info] , f)
            elif gTaskChoice == 'Load Tasksets':
                # if len(gTasksetpath) != 0:
                file_name = gTasksetpath
                with open('./genTasksets/'+file_name, 'rb') as f:
                     data = pickle.load(f)
                tasksets_difutil = data[0]
                info = data[1]
                gNumberOfTaskSets = int(info[0])
                gNumberOfTasksPerSet = int(info[1])
                gUStep = int(info[2])
                gSLenMinValue = float(info[3])
                gSLenMaxValue = float(info[4])
                gNumberOfSegs = int(info[5])
                gSeed = info[6]
            return tasksets_difutil



        def schedulabilityTest(Tasksets_util):
            pool = Pool(gthread)

            sspropotions = ['10']
            periodlogs = ['2']
            for ischeme in gSchemes:
                x = np.arange(gUStart, gUEnd+1, gUStep)
                #y = np.zeros(int(100 / gUStep) + 1)
                print(x)
                y = np.zeros(int((gUEnd-gUStart) / gUStep) + 1)
                print(y)
                ifskip = False
                # print("Hello")
                # print(Tasksets_util)
                # print("Hello")
                for u, tasksets in enumerate(Tasksets_util, start=0):  # iterate through taskset
                    print("Scheme:", ischeme, "Task-sets:", gNumberOfTaskSets, "Tasks per Set:", gNumberOfTasksPerSet, "U:", gUStart + u * gUStep, "SSLength:", str(
                        gSLenMinValue), " - ", str(gSLenMaxValue), "Num. of segments:", gNumberOfSegs)
                    if u == 0:
                        y[u] = 1
                        continue
                    if u * gUStep == 100:
                        y[u] = 0
                        continue
                    if ifskip == True:
                        print("acceptanceRatio:", 0)
                        y[u] = 0
                        continue
                    
                    numfail = 0
                    splitTasks = np.array_split(tasksets,gthread)
                    results = [pool.apply_async(switchTest, args=(splitTasks[i],ischeme,i,)) for i in range(len(splitTasks))]
                    output = [p.get() for p in results]
                    numfail = sum(output)

                    acceptanceRatio = 1 - (numfail / gNumberOfTaskSets)
                    print("acceptanceRatio:", acceptanceRatio)
                    y[u] = acceptanceRatio
                    if acceptanceRatio == 0:
                        ifskip = True

                plotPath = gPrefixdata + '/' + str(gSLenMinValue) + '-' + str(gSLenMaxValue) + '/' + str(gNumberOfSegs) + '/'
                plotfile = gPrefixdata + '/' + str(gSLenMinValue) + '-' + str(gSLenMaxValue) + '/' + str(
                    gNumberOfSegs) + '/' + ischeme + str(gNumberOfTasksPerSet)

                if not os.path.exists(plotPath):
                    os.makedirs(plotPath)
                np.save(plotfile, np.array([x, y]))
       


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Evaluation Framework for Self-Suspending Task Systems"))
        self.groupBox_general.setTitle(_translate("MainWindow", "General"))
        self.prefixdatapath.setText(_translate("MainWindow", "effsstsPlot/Data"))
        self.threadcount.setText(_translate("MainWindow", "1"))
        self.tasksetdatapath.setText(_translate("MainWindow", "TspCon_100_TpTs_10_Utilst_5_Minss_0.01_Maxss_0.1_Seg_2_.pkl"))
        self.runtests.setText(_translate("MainWindow", "Run Tests"))
        self.plotdata.setText(_translate("MainWindow", "Plot selected Tests"))
        self.plotall.setText(_translate("MainWindow", "Combine selected Tests"))
        self.label_5.setText(_translate("MainWindow", "Prefix Data Path:"))
        self.loadtasks_title.setText(_translate("MainWindow", "Tasksets File Name:"))
        self.label_threadcount.setText(_translate("MainWindow", "Threadcount:"))
        self.label_seed.setText(_translate("MainWindow", "Seed:"))
        self.groupbox_configurations.setTitle(_translate("MainWindow", "Configurations"))
        self.label_6.setText(_translate("MainWindow", "Task Sets per Configuration:"))
        self.label_7.setText(_translate("MainWindow", "Tasks per Set:"))
        self.label_8.setText(_translate("MainWindow", "Utilization Start Value:"))
        self.label_9.setText(_translate("MainWindow", "Utilization End Value:"))
        self.label_10.setText(_translate("MainWindow", "Number of Segments:"))
        self.label_11.setText(_translate("MainWindow", "Utilization Step:"))
        self.label.setText(_translate("MainWindow", "Suspension Length Min Value:"))
        self.label_3.setText(_translate("MainWindow", "Suspension Length Max Value:"))
        self.run.setText(_translate("MainWindow", "Run"))
        self.exit.setText(_translate("MainWindow", "Exit"))
        self.groupbox_schedulability_tests.setTitle(_translate("MainWindow", "Schedulability tests"))
        self.groupbox_plots.setTitle(_translate("MainWindow", "Plots"))
        self.groupBox_6.setTitle(_translate("MainWindow", "General"))
        self.nc.setText(_translate("MainWindow", "NC"))
        self.srsr.setText(_translate("MainWindow", "SRSR"))
        self.biondi.setText(_translate("MainWindow", "Biondi RTSS 16"))
        self.groupBox.setTitle(_translate("MainWindow", "FRD Hybrid"))
        self.pathminddd.setText(_translate("MainWindow", "Oblivious-IUB"))
        self.pathminddnd.setText(_translate("MainWindow", "Clairvoyant-SSSD"))
        self.pathpbminddd.setText(_translate("MainWindow", "Oblivious-MP"))
        self.pathpbminddnd.setText(_translate("MainWindow", "Clairvoyant-PDAB"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Segmented"))
        self.scedf.setText(_translate("MainWindow", "SCEDF"))
        self.scrm.setText(_translate("MainWindow", "SCRM"))
        self.scairrm.setText(_translate("MainWindow", "SCAIR-RM"))
        self.rss.setText(_translate("MainWindow", "RSS"))
        self.gmfpa.setText(_translate("MainWindow", "GMF-PA"))
        self.rtedf.setText(_translate("MainWindow", "RTEDF"))
        self.udledf.setText(_translate("MainWindow", "UDLEDF"))
        self.wlaedf.setText(_translate("MainWindow", "WLAEDF"))
        self.uniframework.setText(_translate("MainWindow", "UniFramework"))
        self.suspobl.setText(_translate("MainWindow", "SuspObl"))
        self.suspjit.setText(_translate("MainWindow", "SuspJit"))
        self.suspblock.setText(_translate("MainWindow", "SuspBlock"))
        self.uppaal.setText(_translate("MainWindow", "UPPAAL"))
        self.seifdamip.setText(_translate("MainWindow", "SEIFDA-MILP"))
        self.scairopa.setText(_translate("MainWindow", "SCAIR-OPA"))
        self.frdgmfopa.setText(_translate("MainWindow", "FRDGMF-OPA"))
        self.groupBox_5.setTitle(_translate("MainWindow", "FRD Segmented"))
        self.proportional.setText(_translate("MainWindow", "Proportional"))
        self.seifdamind.setText(_translate("MainWindow", "SEIFDA-minD-"))
        self.seifdamaxd.setText(_translate("MainWindow", "SEIFDA-maxD-"))
        self.seifdapbmind.setText(_translate("MainWindow", "SEIFDA-PBminD-"))
        self.eda.setText(_translate("MainWindow", "EDA"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Dynamic"))
        self.label_mp.setText(_translate("MainWindow", "Values:"))
        self.label_mp_control.setText(_translate("MainWindow", "Control Parameter:"))
        self.label_mp_min.setText(_translate("MainWindow", "Min Values:"))
        self.label_mp_max.setText(_translate("MainWindow", "Max Values:"))
        self.mp_check.setText(_translate("MainWindow", "Combine available Tests"))
        self.passopa.setText(_translate("MainWindow", "PASS-OPA"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+F4"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionFramework_Help.setText(_translate("MainWindow", "Framework Help"))
        self.actionAbout_Framework.setText(_translate("MainWindow", "About Framework"))

 
def switchTest(tasksets,ischeme,i):
    counter = 0
    for tasks in tasksets:
        if ischeme == 'SCEDF':
            if SCEDF.SC_EDF(tasks) == False:
                counter += 1
        elif ischeme == 'SCRM':
            if SCRM.SC_RM(tasks) == False:
                counter += 1
        elif ischeme == 'PASS-OPA':
            if Audsley.Audsley(tasks) == False:
                counter += 1
        elif ischeme == 'SEIFDA-MILP':
            if mipx.mip(tasks) == False:
                counter += 1
        elif ischeme.split('-')[0] == 'SEIFDA':
            if SEIFDA.greedy(tasks, ischeme) == False:
                counter += 1
        elif ischeme.split('-')[0] == 'PATH':
            if PATH.PATH(tasks, ischeme) == False:
                counter += 1
        elif ischeme == 'EDA':
            if EDA.EDA(tasks, gNumberOfSegs) == False:
                counter += 1
        elif ischeme == 'PROPORTIONAL':
            if PROPORTIONAL.PROPORTIONAL(tasks, gNumberOfSegs) == False:
                counter += 1
        elif ischeme == 'NC':
            if NC.NC(tasks) == False:
                counter += 1
        elif ischeme == 'SRSR':
            if SRSR.SRSR(tasks) == False:
                counter += 1
        elif ischeme == 'SCAIR-RM':
            if rad.scair_dm(tasks) == False:
                counter += 1
        elif ischeme == 'SCAIR-OPA':
            if rad.Audsley(tasks, ischeme) == False:
                counter += 1
        elif ischeme == 'FRDGMF-OPA':
            if rad.Audsley(tasks, ischeme) == False:
                counter += 1
        elif ischeme == 'Biondi':
            if Biondi.Biondi(tasks) == False:
                counter += 1
        elif ischeme == 'RSS':
            if RSS.SC2EDF(tasks) == False:
                counter += 1
        elif ischeme == 'UDLEDF':
            if UDLEDF.UDLEDF(tasks) == False:
                counter += 1
        elif ischeme == 'WLAEDF':
            if WLAEDF.WLAEDF(tasks) == False:
                counter += 1
        elif ischeme == 'RTEDF':
            if RTEDF.RTEDF(tasks) == False:
                counter += 1
        elif ischeme == 'UNIFRAMEWORK':
            if UNIFRAMEWORK.UniFramework(tasks) == False:
                counter += 1
        elif ischeme == 'SUSPOBL':
            if FixedPriority.SuspObl(tasks) == False:
                counter += 1
        elif ischeme == 'SUSPJIT':
            if FixedPriority.SuspJit(tasks) == False:
                counter += 1
        elif ischeme == 'SUSPBLOCK':
            if FixedPriority.SuspBlock(tasks) == False:
                counter += 1
        elif ischeme == 'UPPAAL':
            if Uppaal.Uppaal(tasks,i) == False:
                counter += 1
        elif ischeme.split('-')[0] == 'GMFPA':
            if GMFPA.GMFPA(tasks,ischeme) == False:
                counter += 1
        else:
            assert ischeme, 'not vaild ischeme'
    return counter


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #khchen
    MainWindow.statusBar().showMessage('Ready')
    MainWindow.show()
    sys.exit(app.exec_())
