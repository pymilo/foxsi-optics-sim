'''
Created on Aug 1, 2011

@author: rtaylor
'''
from distutils.core import setup
from os import system
#from PyQt4.uic import compileUi

srcDir = 'src/'
guiDir = 'src/foxsisim_gui/'
scpDir = 'src/scripts/'
scripts = ['foxsisim-gui.py']

command = 'pyuic4 -o ' + guiDir + 'ui_mainwindow.py ' + guiDir + 'ui/mainwindow.ui'
print command
system(command)
#compileUi(guiDir+'ui/mainwindow.ui',file(guiDir+'ui_mainwindow.py','w'))

setup(name='foxsisim',
      version='0.1',
      description='FOXSI Optics Simulation Tool: A python tool to simulate grazing incidence optics response to light sources of different wavelengths.',
      author='Robert Taylor',
      author_email='rlvtaylor@embarqmail.com',
      url='https://launchpad.net/foxsisim',
      package_dir={'':srcDir},
      packages=['foxsisim','foxsisim_gui'],
      scripts=[scpDir+s for s in scripts]
     )
