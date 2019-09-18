Grazing-Incidence Optics Simulation Tool
----------------------------------------

How to Install
--------------
To do complete install:

    sudo python setup.py install

To install in current directory:

    python setup.py install --home=.

or using pip while immediately outside the directory

    pip install -e foxsi-optics-sim

When installing to local directory, you need to update PATH 
and PYTHONPATH variables in order to use the foxsisim tools:

For linux:
1. Open ~/.bashrc in a text editor
2. Add the following line, where FOXSISIM_DIR is the location of your foxsisim root directory:
   
    export PATH=$PATH:"FOXSISIM_DIR/bin"
    export PYTHONPATH=$PYTHONPATH:"FOXSISIM_DIR/lib/python"


Help
----
For help using the foxsisim module use python's help() command. 
For example:

    import foxsisim
    help(foxsisim)
    from foxsisim.module import Module
    help(Module)

Also, see the foxsisim/examples/ folder.

To run the GUI from the command line, type:
    
    foxsisim-gui.py

For help using foxsisim-gui, see the Quickstart guide located in the 
foxsisim/doc/ folder.

Authors
-------
This code has been written by Robert Taylor (@rtaylor), Steven Christe (@ehsteve),
and J.C. Buitrago-Casas (@pymilo).


