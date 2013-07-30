'''
Created on Aug 14, 2011

@author: rtaylor
'''
from PyQt4.QtCore import QThread, SIGNAL

class SimThread(QThread):
    '''
    A thread class to do simulation
    '''
    
    def __init__(self, parent = None, mainwindow = None):
        '''
        Constructor
        '''
        QThread.__init__(self, parent)
        self.mainwindow = mainwindow
        self.stopped = True  

    def run(self):
        '''
        Does simulation, periodically sending signals to progressbar
        '''
        self.stopped = False
        sources = self.mainwindow.sources
        module = self.mainwindow.module
        detector = self.mainwindow.detector
        raysPerSource = self.mainwindow.raysPerSource
        allRays = self.mainwindow.allRays
        
        if raysPerSource > 0:
            
            self.emit(SIGNAL('simulationStarted'))
    
            rays = []
            for source in sources:
                newrays = source.generateRays(module.targetFront,raysPerSource)
                for ray in newrays: ray.tag = source
                rays.extend(newrays)
            
            start = 0
            step = 100
            total = len(rays)
            while not self.stopped:
                stop = min([start + step, total])
                r = rays[start:stop]
                module.passRays(r)
                detector.catchRays(r)
                start += len(r)
                
                self.emit(SIGNAL('updateSimulationProgress'), 100*float(stop)/total, len(r))
                allRays.extend(r)
                if stop >= total: break
                
            self.emit(SIGNAL('simulationDone'))


        