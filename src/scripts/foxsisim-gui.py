#!/usr/bin/env python
'''
Created on Aug 1, 2011

@author: rtaylor
'''
import sys
from PyQt4 import QtGui
from foxsisim_gui.mainwindow import MainWindow

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())    
    