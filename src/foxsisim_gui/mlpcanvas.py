'''
Created on Aug 14, 2011
A modified version of code found at 
http://matplotlib.sourceforge.net/examples/user_interfaces/embedding_in_qt4.html

@author: rtaylor
'''
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    '''
    Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).
    '''
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        '''
        Constructor
        '''
        figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = figure.add_subplot(111)
        
        # We want the axes cleared every time plot() is called
        #self.axes.hold(False)
        
        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
