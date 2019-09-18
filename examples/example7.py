#!/usr/bin/env python
import foxsisim.reflectivity as ref
import matplotlib.pyplot as plt
from foxsisim.plotting import plot

if __name__ == '__main__':

    r = ref.Reflectivity(material='Ni')
    plot(r)
    plt.show()
