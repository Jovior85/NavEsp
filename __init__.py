# -*- coding: utf-8 -*-


    
import os, sys
import ConfigParser

if (os.name == 'nt'):
    sys.path.append(os.path.join(os.path.dirname((os.path.realpath(__file__))), '..\\Libs'))
    sys.path.append(os.path.join(os.path.dirname((os.path.realpath(__file__))), '..\\Libs\\VTK\\lib\\site-packages'))
    sys.path.append(os.path.join(os.path.dirname((os.path.realpath(__file__))), '..\\Libs\\WrapITK\\Python'))
    # Suport for svg icons
    #from PyQt4 import QtGui,QtCore
    QtGui.QApplication.addLibraryPath(os.path.join(os.path.dirname((os.path.realpath(__file__))), '..\\Libs\\Qt\\plugins'))
    # hide the vtk output window (some warnigns)

from PyQt4   import QtCore,QtGui
from Ventana import Ventana
from NavEsp import NavEsp
from math import sqrt
from copy import deepcopy
from Configuracion import *
from Arbol import *

if __name__=="__main__":

      app= QtGui.QApplication(sys.argv)
      nav = NavEsp()
     ##     nav.crearEstructura(3, 3, 3)
      sys.exit(app.exec_())