"""
Created on Aug 1, 2011
@author: rtaylor

Updated on June 2016
@ Steven Christe and Milo Buitrago-Casas

Needs Python 3.5
"""
from distutils.core import setup
from os import system

srcDir = 'src'
guiDir = 'src/foxsisim_gui/'
scpDir = 'examples/'
gui = ['foxsisim-gui.py']
scripts = ['example1.py', 'example2.py', 'example3.py', 'example4.py',
           'example5.py', 'example6.py', 'example7.py', 'example8.py',
           'example9.py', 'example10.py']

command = 'pyuic4 -o ' + guiDir + 'ui_mainwindow.py ' + guiDir + 'ui/mainwindow.ui'
print(command)
system(command)

install_requires = [
    # List your project dependencies here.
    'matplotlib',
    'numpy',
    'h5py'
]

setup(
    name='foxsisim',
    version='0.1',
    description='FOXSI Optics Simulation Tool: A python tool to simulate grazing incidence optics response to light sources of different wavelengths.',
    author='Robert Taylor, Steven Christe, Milo Buitrago-Casas',
    author_email='rlvtaylor@embarqmail.com, ' +
                 'steven.d.christe@nasa.gov, ' +
                 'jcbuitragoc@unal.edu.co',
    url='https://github.com/foxsi/foxsi-optics-sim',
    package_dir={'':srcDir},
    packages=['foxsisim', 'foxsisim_gui'],
    scripts=[scpDir+s for s in scripts],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
)
