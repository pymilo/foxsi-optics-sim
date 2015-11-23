'''
Created on Aug 1, 2011

@author: rtaylor
'''
from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from ui_mainwindow import Ui_MainWindow
from mlpcanvas import MplCanvas
from simthread import SimThread
from defaults import *
from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.mymath import * #@UnusedWildImport
from foxsisim.plotting import scatterHist, plot
from math import cos
import numpy as np #@Reimport

dtf = np.dtype('f8')
precision = 13

class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # helper vars
        self.simThread = SimThread(mainwindow=self)
        self.sources = []
        self.module = None
        self.detector = None
        self.allRays = []
        self.simulationSessionStarted = False
        self.tableItemChanging = False
        self.figures = []
        self.colors = ['white','red','green','blue','yellow','light blue','magenta','black']
        self.colorsRGB = [[1,1,1],
                          [1,0,0],
                          [0,1,0],
                          [0,0,1],
                          [1,1,0],
                          [0,1,1],
                          [1,0,1],
                          [0,0,0]]

        # setup connections
        self.connect(self.actionAbout_FOXSISIM_2, SIGNAL('triggered()'),self.about)
        self.sourceSignalMapper = QSignalMapper() # needed to map combobox signals to table widget slots
        self.connect(self.sourceSignalMapper,SIGNAL('mapped(int)'),self.tableWidget_2_sourceTypeChanged)
        self.connect(self.tabWidget, SIGNAL('currentChanged(int)'),self.tabWidget_currentChanged)
        self.connect(self.tableWidget, SIGNAL('itemChanged(QTableWidgetItem *)'), self.tableWidget_itemChanged)
        self.connect(self.tableWidget_2, SIGNAL('itemChanged(QTableWidgetItem *)'), self.tableWidget_2_itemChanged)
        self.connect(self.toolButton, SIGNAL('clicked()'), self.toolButton_clicked)
        self.connect(self.toolButton_2, SIGNAL('clicked()'), self.toolButton_2_clicked)
        self.connect(self.toolButton_3, SIGNAL('clicked()'), self.toolButton_3_clicked)
        self.connect(self.toolButton_4, SIGNAL('clicked()'), self.toolButton_4_clicked)
        self.connect(self.toolButton_5, SIGNAL('clicked()'), self.toolButton_5_clicked)
        self.connect(self.toolButton_6, SIGNAL('clicked()'), self.toolButton_6_clicked)
        self.connect(self.toolButton_7, SIGNAL('clicked()'), self.toolButton_7_clicked)
        self.connect(self.toolButton_8, SIGNAL('clicked()'), self.toolButton_8_clicked)
        self.connect(self.doubleSpinBox, SIGNAL('valueChanged(double)'), self.doubleSpinBox_valueChanged)
        self.connect(self.pushButton, SIGNAL('clicked()'), self.pushButton_clicked)
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.pushButton_2_clicked)
        self.connect(self.pushButton_3, SIGNAL('clicked()'), self.pushButton_3_clicked)
        self.connect(self.pushButton_4, SIGNAL('clicked()'), self.pushButton_4_clicked)
        self.connect(self.pushButton_5, SIGNAL('clicked()'), self.pushButton_5_clicked)
        self.connect(self.pushButton_6, SIGNAL('clicked()'), self.pushButton_6_clicked)
        self.connect(self, SIGNAL('startSimulation'), self.simThread.start)
        self.connect(self.simThread, SIGNAL('updateSimulationProgress'), self.updateSimulationProgress)
        self.connect(self.simThread, SIGNAL('simulationStarted'), self.simulationStarted)
        self.connect(self.simThread, SIGNAL('simulationDone'), self.simulationDone)
        self.connect(self.spinBox, SIGNAL('valueChanged(int)'), self.updateRaysToSimulate)
        self.connect(self, SIGNAL('updateRaysToSimulate'), self.updateRaysToSimulate)

        # set defaults
        self.setModuleDefaults()
        self.setSourceDefaults()

    def closeEvent(self, event):
        '''
        Performs shutdown tasks
        '''
        for fig in self.figures:
            fig.close()
        event.accept()

    def about(self):
        '''
        Calls a message box displaying the 'About'
        '''
        QMessageBox.about(self, 'About FOXSISIM',
u'''FOXSISIM
Copyright \N{COPYRIGHT SIGN} 2011 Robert Taylor, Steven Christe

The FOXSI Optics Simulation Tool (foxsisim) is a python tool to simulate grazing incidence optics response to light sources of different wavelengths. This graphical user interface is a frontend for the foxsisim module.''')

    def setModuleDefaults(self):
        '''
        Sets all default values in Module tab
        '''
        # spin boxes
        self.doubleSpinBox.setValue(defaultFocalLength)
        self.doubleSpinBox_2.setValue(defaultSegmentLength)
        self.doubleSpinBox_3.setValue(defaultDetectorOffset)
        self.doubleSpinBox_4.setValue(defaultDetectorWidth)
        self.doubleSpinBox_5.setValue(defaultDetectorHeight)
        self.spinBox_2.setValue(defaultDetectorReso[0])
        self.spinBox_3.setValue(defaultDetectorReso[1])

        # module radii/angle table
        self.tableWidget.setRowCount(len(defaultRadii))
        for i,radius in enumerate(defaultRadii):
            r = QString.number(radius,precision=precision)
            self.tableWidget.setItem(i,0,QTableWidgetItem(r)) # angle is autofilled by tableWidget_itemChanged()

    def setSourceDefaults(self):
        '''
        Sets all defaults in Sources tab
        '''
        # source table
        self.insertSourceRow(0)
        type = self.tableWidget_2.cellWidget(0,0)
        type.setCurrentIndex(type.findText(defaultSourceType))
        center = QString(str(defaultSourceCenter[0])+','+str(defaultSourceCenter[1])+','+str(defaultSourceCenter[2]))
        self.tableWidget_2.setItem(0,1,QTableWidgetItem(center))
        self.tableWidget_2.setItem(0,3,QTableWidgetItem(QString.number(defaultSourceWidth,precision=precision)))
        self.tableWidget_2.setItem(0,4,QTableWidgetItem(QString.number(defaultSourceHeight,precision=precision)))
        color = self.tableWidget_2.cellWidget(0,5)
        color.setCurrentIndex(color.findText(defaultSourceColor))

    def insertModuleRow(self, i):
        '''
        Insert a row into the module radii/angles table
        '''
        self.tableWidget.blockSignals(True) # no signals emitted during row creation
        self.tableWidget.insertRow(i)
        self.tableWidget.setItem(i,0,QTableWidgetItem(QString('')))
        self.tableWidget.setItem(i,1,QTableWidgetItem(QString('')))
        self.tableWidget.blockSignals(False)

    def insertSourceRow(self, i):
        '''
        Insert a row into the sources table
        '''
        self.tableWidget_2.blockSignals(True) # no signals emitted during row creation
        self.tableWidget_2.insertRow(i)
        type = QComboBox()
        type.addItems(['atinf', 'point', 'nonpoint'])
        color = QComboBox()
        color.addItems(self.colors)
        self.tableWidget_2.setCellWidget(i,0,type)
        self.tableWidget_2.setItem(i,1,QTableWidgetItem(QString('')))
        self.tableWidget_2.setItem(i,2,QTableWidgetItem(QString('')))
        self.tableWidget_2.setItem(i,3,QTableWidgetItem(QString('')))
        self.tableWidget_2.setItem(i,4,QTableWidgetItem(QString('')))
        self.tableWidget_2.setCellWidget(i,5,color)
        self.tableWidget_2.blockSignals(False)

        # connect signal from the type widget to the mapper which then will emit a 'mapped(i)' signal
        self.connect(type,SIGNAL('currentIndexChanged(int)'),self.sourceSignalMapper,SLOT('map()'))
        self.updateSourceSignalMapper()

    def updateSourceSignalMapper(self):
        '''
        Ensures the signal mappings are all correct
        '''
        for i in range(self.tableWidget_2.rowCount()):
            type = self.tableWidget_2.cellWidget(i,0)
            self.sourceSignalMapper.removeMappings(type)
            self.sourceSignalMapper.setMapping(type,i)

    def createModule(self):
        '''
        Returns a Module object based on gui input values
        '''
        # get radii and angles
        radii,angles = [],[]
        for i in range(self.tableWidget.rowCount()):
            r,rvalid = self.tableWidget.item(i,0).text().toDouble()
            a,avalid = self.tableWidget.item(i,1).text().toDouble()
            if rvalid and avalid:
                radii.append(r)
                angles.append(a)
        # radii need to be in decending order
        import operator
        indices = [i for (i,j) in sorted(enumerate(radii), key=operator.itemgetter(1), reverse=True)]        #@UnusedVariable
        radii = [radii[i] for i in indices]
        angles = [angles[i] for i in indices]
        # get other value
        seglen = self.doubleSpinBox_2.value()
        focal = self.doubleSpinBox.value()
        # return module
        try: return Module(seglen=seglen,focal=focal,radii=radii,angles=angles)
        except:
            QMessageBox.warning(self,'Warning','Could not create module. Check input values.')
            return None

    def createDetector(self):
        '''
        Returns a Detector object based on gui input values
        '''
        focal = self.doubleSpinBox.value()
        seglen = self.doubleSpinBox_2.value()
        offset = self.doubleSpinBox_3.value()
        center = [0,0,focal+seglen+offset]
        width = self.doubleSpinBox_4.value()
        height = self.doubleSpinBox_5.value()
        reso = [self.spinBox_2.value(),self.spinBox_3.value()]
        try: return Detector(center=center, width=width, height=height, reso=reso)
        except:
            QMessageBox.warning(self,'Warning','Could not create detector. Check input values.')
            return None

    def createSource(self, row):
        '''
        Returns a Source object from row i in the sources table
        '''

        # get input
        type = str(self.tableWidget_2.cellWidget(row,0).currentText())
        center = self.str2List(self.tableWidget_2.item(row,1).text())
        normal = self.str2List(self.tableWidget_2.item(row,2).text())
        width = self.str2Num(self.tableWidget_2.item(row,3).text())
        height= self.str2Num(self.tableWidget_2.item(row,4).text())
        colorText = str(self.tableWidget_2.cellWidget(row,5).currentText())
        color = self.colorsRGB[self.colors.index(colorText)]

        try:
            if type == 'atinf' or type == 'nonpoint':
                return Source(center=center, width=width, height=height, normal=normal, type=type, color=color)
            elif type == 'point':
                return Source(center=center, type=type, color=color)
        except:
            QMessageBox.warning(self,'Warning','Could not create source at row '+str(row+1)+'. Check input values.')
            return None

    def tabWidget_currentChanged(self, index):
        '''
        Slot for tab change in tabWidget.
        '''
        # if we arent in the middle of simulation session
        if not self.simulationSessionStarted:

            # update module/detector/sources
            if index != 0:
                self.module = self.createModule()
                self.detector = self.createDetector()
            if index != 1:
                self.sources = []
                for row in range(self.tableWidget_2.rowCount()):
                    source = self.createSource(row)
                    if source is not None: self.sources.append(source)

            # update source list for scatterplot
            if index == 2:
                self.listWidget.clear()
                for source in self.sources:
                    self.listWidget.addItem(QString(source.type+' at ['+self.list2Str(source.center)+']'))
                self.listWidget.selectAll()

            # update 'rays to simulate'
            if index == 2: self.emit(SIGNAL('updateRaysToSimulate'))

    def tableWidget_itemChanged(self,item):
        '''
        Slot for item change in module radii/angles table
        '''
        # prevent infinite recursion
        if self.tableItemChanging: return
        self.tableItemChanging = True

        # get location
        row = item.row()
        col = item.column()

        # get double float
        if len(item.text()) > 0:
            number,valid = item.text().toDouble()
            if not valid:
                QMessageBox.warning(self,'Warning','Invalid input')
                item.setText('')
                number = None
        else: number = None

        # if autocalculation is checked
        if self.checkBox.isChecked():

            if number is None: # set the other column to none
                self.tableWidget.setItem(row,(col+1)%2,QTableWidgetItem(''))
            elif col == 0: # radius changed
                focal = self.doubleSpinBox.value()
                angle = calcShellAngle(number,focal)
                item = QTableWidgetItem(QString.number(angle,precision=precision))
                self.tableWidget.setItem(row,1,item)
            elif col == 1: # angle changed
                focal = self.doubleSpinBox.value()
                radius = calcShellRadius(number,focal)
                item = QTableWidgetItem(QString.number(radius,precision=precision))
                self.tableWidget.setItem(row,0,item)
            else: # invalid index
                print 'error: update tableWidget_itemChanged method'

        # reset the recursion preventer
        self.tableItemChanging = False

    def tableWidget_2_sourceTypeChanged(self,row):
        '''
        Slot for value change in type combo box in sources table
        '''
        pass

    def tableWidget_2_itemChanged(self,item):
        '''
        Slot for item change in sources table
        '''
        # prevent infinite recursion
        if self.tableItemChanging: return
        self.tableItemChanging = True

        # get location and row items
        row = item.row()
        col = item.column()
        typeWidget = self.tableWidget_2.cellWidget(row,0)
        centerItem = self.tableWidget_2.item(row,1)
        normalItem = self.tableWidget_2.item(row,2)
        widthItem = self.tableWidget_2.item(row,3)
        heightItem = self.tableWidget_2.item(row,4)
        #colorWidget = self.tableWidget_2.cellWidget(row,5)

        type = typeWidget.currentText()
        center = self.str2List(centerItem.text())
        normal = self.str2List(normalItem.text())
        width = self.str2Num(widthItem.text())
        height = self.str2Num(heightItem.text())
        #color = colorWidget.currentText()

        # check validity of entire row's input
        invalidInput = False
        if len(centerItem.text()) > 0 and (center is None or len(center) != 3):
            center = None
            invalidInput = True
        if len(normalItem.text()) > 0 and (normal is None or len(normal) != 3):
            normal = None
            invalidInput = True
        if len(widthItem.text()) > 0 and (width is None or width < 0):
            width = None
            invalidInput = True
        if len(heightItem.text()) > 0 and (height is None or height < 0):
            height = None
            invalidInput = True
        if invalidInput: QMessageBox.warning(self,'Warning','Invalid input')

        # if autocalculation is checked
        if self.checkBox_2.isChecked():
            if col == 1 and center is not None: # center changed
                normal = [-x for x in center]
            elif col == 2 and normal is not None: # normal changed
                center = [-x for x in normal]

            # source width/height is autocalculated when atinf
            if type == QString('atinf') and normal is not None and normal[2] > 0:
                ny = np.array([normal[0],0,normal[2]])
                ang = angleBetweenVectors(ny,np.array([0,0,1]))
                try: dims = self.module.getDims()
                except: dims = self.createModule().getDims()
                radius = dims[0] # radius at wide end of module
                width = 2*radius*cos(ang)
                height = 2*radius # TODO: find the proper way to calculate this

            # check that center is in negative z region
            if center is not None and center[2] >= 0:
                QMessageBox.warning(self,'Warning','Source center point should have a negative z value')

        # change items
        self.tableWidget_2.setItem(row,1,QTableWidgetItem(self.list2Str(center)))
        self.tableWidget_2.setItem(row,2,QTableWidgetItem(self.list2Str(normal)))
        self.tableWidget_2.setItem(row,3,QTableWidgetItem(self.num2Str(width)))
        self.tableWidget_2.setItem(row,4,QTableWidgetItem(self.num2Str(height)))

        # reset the recursion preventer
        self.tableItemChanging = False

    def str2Num(self,str):
        '''
        Takes a QString and returns a double
        '''
        if str == QString(''): return None
        num,valid = str.toDouble()
        if not valid: return None
        return num

    def num2Str(self,num):
        '''
        Takes a number and returns a string
        '''
        if num is None: return QString('')
        return QString.number(num,precision=precision)

    def str2List(self,str):
        '''
        Takes a string of from 'x,y,z' and returns list [x,y,z]
        '''
        try:
            arr = str.split(',')
            return [float(s) for s in arr]
        except: return None

    def list2Str(self,list):
        '''
        Takes a list of form [x,y,z] and returns string 'x,y,z'
        '''
        if list is None: return QString('') # return empty string if None is passed
        arr = [QString.number(x,precision=precision)+',' for x in list]
        arr[-1].remove(-1,1)
        arr = [str(q) for q in arr]
        return ''.join(arr)

    def toolButton_clicked(self):
        '''
        Slot for toolButton. Adds a row to the sources table.
        '''
        row = self.tableWidget_2.rowCount()
        self.insertSourceRow(row)
        self.updateSourceSignalMapper()

    def toolButton_2_clicked(self):
        '''
        Slot for toolButton_2. Removes a row from the sources table.
        '''
        row = self.tableWidget_2.currentRow()
        if row < 0:
            row = self.tableWidget_2.rowCount()-1
        self.sourceSignalMapper.removeMappings(self.tableWidget_2.cellWidget(row,0))
        self.tableWidget_2.removeRow(row)
        self.updateSourceSignalMapper()

    def toolButton_3_clicked(self):
        '''
        Slot for toolButton_3. Adds a row to the module radii/angles table.
        '''
        row = self.tableWidget.rowCount()
        self.insertModuleRow(row)

    def toolButton_4_clicked(self):
        '''
        Slot for toolButton_4. Removes a row from the module radii/angles table.
        '''
        row = self.tableWidget.currentRow()
        if row < 0:
            row = self.tableWidget.rowCount()-1
        self.tableWidget.removeRow(row)

    def toolButton_5_clicked(self):
        '''
        Slot for toolButton_5. Moves a row up in the module radii/angles table.
        '''
        row = self.tableWidget.currentRow()
        if row > 0 and row < self.tableWidget.rowCount():
            self.insertModuleRow(row+1)
            self.tableWidget.setItem(row+1,0,self.tableWidget.item(row-1,0).clone())
            self.tableWidget.setItem(row+1,1,self.tableWidget.item(row-1,1).clone())
            self.tableWidget.removeRow(row-1)

    def toolButton_6_clicked(self):
        '''
        Slot for toolButton_6. Moves a row down in the module radii/angles table.
        '''
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        if row >= 0 and row+1 < self.tableWidget.rowCount():
            self.insertModuleRow(row+2)
            self.tableWidget.setItem(row+2,0,self.tableWidget.item(row,0).clone())
            self.tableWidget.setItem(row+2,1,self.tableWidget.item(row,1).clone())
            self.tableWidget.removeRow(row)
            self.tableWidget.setCurrentCell(row+1,col)

    def toolButton_7_clicked(self):
        '''
        Slot for toolButton_7. Moves a row up in the sources table.
        '''
        row = self.tableWidget_2.currentRow()
        if row > 0 and row < self.tableWidget_2.rowCount():
            self.insertSourceRow(row+1)
            self.tableWidget_2.cellWidget(row+1,0).setCurrentIndex(self.tableWidget_2.cellWidget(row-1,0).currentIndex())
            self.tableWidget_2.setItem(row+1,1,self.tableWidget_2.item(row-1,1).clone())
            self.tableWidget_2.setItem(row+1,2,self.tableWidget_2.item(row-1,2).clone())
            self.tableWidget_2.setItem(row+1,3,self.tableWidget_2.item(row-1,3).clone())
            self.tableWidget_2.setItem(row+1,4,self.tableWidget_2.item(row-1,4).clone())
            self.tableWidget_2.cellWidget(row+1,5).setCurrentIndex(self.tableWidget_2.cellWidget(row-1,5).currentIndex())

            self.sourceSignalMapper.removeMappings(self.tableWidget_2.cellWidget(row-1,0))
            self.tableWidget_2.removeRow(row-1)
            self.updateSourceSignalMapper()

    def toolButton_8_clicked(self):
        '''
        Slot for toolButton_8. Moves a row down in the sources table.
        '''
        row = self.tableWidget_2.currentRow()
        col = self.tableWidget_2.currentColumn()
        if row >= 0 and row+1 < self.tableWidget_2.rowCount():
            self.insertSourceRow(row+2)
            self.tableWidget_2.cellWidget(row+2,0).setCurrentIndex(self.tableWidget_2.cellWidget(row,0).currentIndex())
            self.tableWidget_2.setItem(row+2,1,self.tableWidget_2.item(row,1).clone())
            self.tableWidget_2.setItem(row+2,2,self.tableWidget_2.item(row,2).clone())
            self.tableWidget_2.setItem(row+2,3,self.tableWidget_2.item(row,3).clone())
            self.tableWidget_2.setItem(row+2,4,self.tableWidget_2.item(row,4).clone())
            self.tableWidget_2.cellWidget(row+2,5).setCurrentIndex(self.tableWidget_2.cellWidget(row,5).currentIndex())

            self.sourceSignalMapper.removeMappings(self.tableWidget_2.cellWidget(row,0))
            self.tableWidget_2.removeRow(row)
            self.tableWidget_2.setCurrentCell(row+1,col)
            self.updateSourceSignalMapper()

    def doubleSpinBox_valueChanged(self,value):
        '''
        Slot for change in value of focal length
        '''
        # if autocalculation is on, recalc angles
        if self.checkBox.isChecked():
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row,0) # radius item
                self.tableWidget_itemChanged(item)

    def pushButton_clicked(self):
        '''
        Slot for pushButton. Simulate.
        '''
        if self.module is None:
            QMessageBox.warning(self,'Invalid module settings')
        elif self.detector is None:
            QMessageBox.warning(self,'Invalid detector settings')
        elif len(self.sources) == 0:
            QMessageBox.warning(self,'Invalid source settings')
        else:
            self.raysPerSource = self.spinBox.value()
            self.emit(SIGNAL('startSimulation'))

    def pushButton_2_clicked(self):
        '''
        Slot for pushButton_2. Reset simulation.
        '''
        # stop thread if needed
        self.simThread.blockSignals(True)
        self.simThread.stopped = True
        self.simThread.wait()
        self.simThread.blockSignals(False)

        # delete rays and update display
        self.allRays = []
        self.simulationDone()

        # ungray other tabs
        self.tab.setEnabled(True)
        self.tab_2.setEnabled(True)

        # indicate that the sim session has ended (module/detector/source settings can be changed)
        self.simulationSessionStarted = False

    def pushButton_3_clicked(self):
        '''
        Slot for pushButton_3. Detector pixel plot.
        '''
        window = QWidget()
        window.setWindowTitle('Detector Pixel Plot')
        l = QVBoxLayout(window)
        canv = MplCanvas(window, width=5, height=5, dpi=100)
        l.addWidget(canv)
        self.detector.plotImage(canv.axes)
        window.show()
        self.figures.append(window)

    def pushButton_4_clicked(self):
        '''
        Slot for pushButton_4. Scatter plot.
        '''
        # just plot the rays from the selected sources
        qindices = self.listWidget.selectedIndexes()
        rays = []
        for qi in qindices:
            source = self.sources[qi.row()]
            for ray in self.detector.rays:
                if ray.tag is source:
                    rays.append(ray)

        # color bounce option
        colorBounces = self.checkBox_3.isChecked()

        # create window
        window = QWidget()
        window.setWindowTitle('Scatter Plot')
        l = QVBoxLayout(window)
        canv = MplCanvas(window, width=5, height=5, dpi=100)
        scatterHist(rays, figure=canv.figure, colorBounces=colorBounces)
        l.addWidget(canv)
        window.show()
        self.figures.append(window)

    def pushButton_5_clicked(self):
        '''
        Slot for pushButton_5. Plot module cross section.
        '''
        window = QWidget()
        window.setWindowTitle('Module Cross Section')
        l = QVBoxLayout(window)
        canv = MplCanvas(window, width=8, height=2, dpi=100)
        l.addWidget(canv)
        module = self.createModule()
        module.plot2D(canv.axes,'b')
        window.show()
        self.figures.append(window)

    def pushButton_6_clicked(self):
        '''
        Slot for pushButton_6. Stop simulation.
        '''
        self.simThread.stopped = True

    def updateRaysToSimulate(self):
        '''
        Slot of spinBox. Number of rays per source changed.
        '''
        raysPerSource = self.spinBox.value()
        self.label_8.setText(QString(str(raysPerSource*len(self.sources))))

    def updateSimulationProgress(self,progressbar,simulated):
        '''
        Slot for updating the progress bar
        '''
        self.progressBar.setValue(progressbar)
        num,valid = self.label_11.text().toInt() #@UnusedVariable
        self.label_11.setText(QString(str(num+simulated)))

    def simulationStarted(self):
        '''
        Slot that disables majority of gui when a simulation is in progress
        '''
        self.simulationSessionStarted = True

        # gray out buttons on sim tab
        self.pushButton.setEnabled(False)
        self.spinBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.groupBox_3.setEnabled(False)

        # gray out other tabs
        self.tab.setEnabled(False)
        self.tab_2.setEnabled(False)

    def simulationDone(self):
        '''
        Slot that reenables the simulation tab, but not the other tabs
        '''
        # ungray the buttons on the sim tab
        self.pushButton.setEnabled(True)
        self.spinBox.setEnabled(True)
        self.groupBox_2.setEnabled(True)
        self.groupBox_3.setEnabled(True)

        # reset progress bar to zero and make sure 'total simulated' is accurate
        self.progressBar.setValue(0)
        self.label_11.setText(QString.number(len(self.allRays)))
