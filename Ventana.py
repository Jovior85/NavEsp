#@PydevCodeAnalysisIgnore
# -*- coding: utf-8 -*-

import os, sys
##from PyQt4 import QtCore, QtGui
#from PySide import QtGui,QtCore
from Arbol import *
##from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor              # OpenGL

import math
from math import sqrt
import pickle
import Estructura
from Renderer import *
from Configuracion import Configuracion
from GestionFicheros import GestionFicheros

class MyDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.setWindowFlags(Qt.Dialog)
        ##self.setAttribute()
    def closeEvent(self,e):
        self.parent.setDisabled(False)
        
    def showDialog(self):
        self.parent.setEnabled(False)
        self.setEnabled(True)
        self.show()
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        return
    def mostrarVentana(self,ruta,ext=None):
        if ext==None:
            filename = QtGui.QFileDialog.getExistingDirectory(self,'Seleccionar directorio',os.getcwd())
        else:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Seleccionar fichero stack',ruta,ext)
        return filename
    
class Ventana(QtGui.QMainWindow):
   def __init__(self,parent=None):
       self.parent = parent
       QtGui.QMainWindow.__init__(self)
       self.setMinimumSize(1024,768)
       #self.resize(1024,768)
       self.wdname = 'Navegacion de Stacks - Espina'
       self.filename = "Untitled"
       self.setWindowTitle(self.filename+" - "+self.wdname)
       ##self.pantalla.setGeometry(30,60,600,400)
       print ("Creating menu bar...")
       self.crearMenus()
       print("Creating contextual menu")
       self.setContextMenuPolicy(Qt.CustomContextMenu)
       self.customContextMenuRequested.connect(self.createContextMenu)
       self.opciones = QMenu()
       print ("Creating Widgets...")
       self.createDocks()
       print ("Creating status bar...")
       self.statusbar = QtGui.QStatusBar(self)
       self.setStatusBar(self.statusbar)
       self.statusbar.showMessage("Ready")
       self.pulsado=""
       self.dialogos = QtGui.QFileDialog
       self.configuracion = Configuracion()
       self.gestorFich = GestionFicheros(self,self.configuracion)
       self.maximo_tam = False
   def resizeEvent(self,resizeEvent):
        rect = self.geometry()
        rec1 = self.lateral_navigation.geometry()
        rec2 = self.lateral_preview.geometry()
        
        (x1,y1,w1,h1) = rec1.getRect()
        (x2,y2,w2,h2) = rec2.getRect()
        if (w1 > w2):
            w = w1
        else:
            w= w2
        
        if self.maximo_tam == False:
            self.ppal.setGeometry(5,5,rect.width()-w-15,rect.height()-25)
            self.parent.resizeRender(rect.width()-w-15,rect.height()-25)
        else:
            self.ppal.setGeometry(5,5,rect.width()-15,rect.height()-25)
            self.parent.resizeRender(rect.width()-15,rect.height()-25)

        #self.lateral_preview.setMaximumSize(310,rect.height()/2)
        #self.lateral_navigation.setDimension(5,5,310,rect.height()/2)

   def getPulsado(self):
       return self.pulsado

   def showMessageInStatusBar(self,msg):
       self.statusbar.showMessage(msg)

   def updateStatusPosition(self,x,y,z):
       self.statusbar.showMessage("("+str(round(x,2))+","+str(round(y,2))+","+str(round(z,2))+")",1000)

   def getClickPosition(self):
       return self.click

   def mostrarDialogoNuevaEstructura(self):
       print("Mostrando dialogo nueva estructura")
       self.mdArea.show()

   def widgetCentral(self,widget):
       self.setCentralWidget(widget)

   def crearMenus(self):
       self.crear_menu_file()
       self.crear_menu_edicion()
       self.crear_menu_ver()
       self.menu_herramientas()
       self.crear_menu_about()
    
   def crear_menu_about(self):
       
       actionSobre = QtGui.QAction(QtGui.QIcon(),'Autor',self)
       actionSobre.setObjectName('actionSobre')
       self.connect(actionSobre, SIGNAL('triggered()'),self.visualizarSobre)

       
       menu = self.menuBar()
       menu.setToolTip('Sobre...')
       ver = menu.addMenu('&Sobre...')
       ver.addAction(actionSobre)
   def visualizarSobre(self):
       self.dialogoSobre = MyDialog()
       self.dialogoSobre.setWindowTitle('Sobre el autor.')
       self.dialogoSobre.texto = QLabel(self.dialogoSobre)
       self.dialogoSobre.texto.setText("NAVESP: Herramienta para la navegaci&oacute;n y el manejo de <br />archivos utilizados en la herramienta ESPINA<br /><br />Autor: Jos&eacute; Vila Ortu&ntilde;o.<br /><br />Universidad Polit&eacute;cnica de Madrid")
       self.dialogoSobre.texto.setGeometry(10,10,400,100)
       self.dialogoSobre.boton = QPushButton(self.dialogoSobre)
       self.dialogoSobre.boton.setText("Aceptar")
       self.dialogoSobre.boton.setGeometry(10,120,100,30)
       self.dialogoSobre.boton.clicked.connect(self.hideSobre)
       self.dialogoSobre.show()
       
   def hideSobre(self):
       self.dialogoSobre.hide()
       del self.dialogoSobre
   
   def crear_menu_ver(self):
       actionVerMalla = QtGui.QAction(QtGui.QIcon(),'Mostrar Malla',self)
       actionVerMalla.setObjectName("actionVerMalla")
       actionVerMalla.setShortcut('m')
       self.connect(actionVerMalla, QtCore.SIGNAL('triggered()'),self.parent.visualizarMalla)
       actionRefresh = QtGui.QAction(QtGui.QIcon(),'Refrescar Imagen',self)
       actionRefresh.setObjectName("actionRefresh")
       actionRefresh.setShortcut('F5')
       
       
       
       ##self.actionEstereoscopia = QtGui.QAction(QtGui.QIcon(),'Estereoscopia',self)
       ##self.actionEstereoscopia.setObjectName("actionVerMenuEst")
       ##self.connect(self.actionEstereoscopia, QtCore.SIGNAL('triggered()'),self.crearMenuEstereoscopia)
       #self.connect(actionVerMalla, QtCore.SIGNAL('triggered()'), self.refrescarImagen)
       menu = self.menuBar()
       menu.setToolTip('Ver')
       ver = menu.addMenu('&Ver')
       ver.addAction(actionVerMalla)
       ver.addAction(actionRefresh)
       ##ver.addAction(self.actionEstereoscopia)
       actionNormal = QtGui.QAction(QtGui.QIcon(),'Normal',self)
       actionNormal.setObjectName('Normal')
       actionNormal.setShortcut('alt+1')

       self.connect(actionNormal, SIGNAL('triggered()'),self.visualizarNormal)
       
       actionAnaglifo = QtGui.QAction(QtGui.QIcon(),'Anaglifo Cyan-Rojo',self)
       actionAnaglifo.setObjectName('Anaglifo')
       actionAnaglifo.setShortcut('alt+2')

       self.connect(actionAnaglifo, SIGNAL('triggered()'),self.visualizarAnaglifoVR)
       
       actionAnaglifoBR = QtGui.QAction(QtGui.QIcon(),'Anaglifo Rojo-Azul',self)
       actionAnaglifoBR.setObjectName('AnaglifoBR')
       actionAnaglifoBR.setShortcut('alt+3')

       self.connect(actionAnaglifoBR, SIGNAL('triggered()'),self.visualizarAnaglifoBR)
       

       actionInterlaced = QtGui.QAction(QtGui.QIcon(),'Entrelazado',self)
       actionInterlaced.setObjectName('Interlaced')
       actionInterlaced.setShortcut('alt+4')

       self.connect(actionInterlaced, SIGNAL('triggered()'),self.visualizarInterlaced)

       actionDresden = QtGui.QAction(QtGui.QIcon(),'Dresden',self)
       actionDresden.setObjectName('Dresden')
       actionDresden.setShortcut('alt+5')

       self.connect(actionDresden, SIGNAL('triggered()'),self.visualizarDresden)

       
       ver.setToolTip('Estereoscopia')
       estereoscopia = ver.addMenu('&Estereoscopia')
       estereoscopia.addAction(actionNormal)
       estereoscopia.addAction(actionAnaglifo)
       estereoscopia.addAction(actionAnaglifoBR)
       estereoscopia.addAction(actionInterlaced)
       estereoscopia.addAction(actionDresden)       
   
   
   def visualizarNormal(self):
       self.parent.visualizacion(1)
       
   def visualizarAnaglifoVR(self):
       self.parent.visualizacion(2)
   def visualizarAnaglifoBR(self):
       self.parent.visualizacion(3)
   
   def visualizarInterlaced(self):
       self.parent.visualizacion(4)
   
   
   def visualizarDresden(self):
       self.parent.visualizacion(5)           
   
   
   def crear_menu_edicion(self):


       actionNewStr = QtGui.QAction(QtGui.QIcon(),'Agregar Estructura',self)
       actionNewStr.setObjectName("actionNewStr")

       actionNewStack = QtGui.QAction(QtGui.QIcon(),'Agregar Stack',self)
       actionNewStack.setObjectName("actionNewStack")
		
       actionDelStr = QtGui.QAction(QtGui.QIcon(),'Eliminar Estructura',self)
       actionDelStr.setObjectName("actionDelStr")
       actionDelStr.setShortcut('Del')

       actionDelStack = QtGui.QAction(QtGui.QIcon(),'Eliminar Stack',self)
       actionDelStack.setObjectName("actionDelStack")

       actionCopy = QtGui.QAction(QtGui.QIcon(),'Copiar',self)
       actionCopy.setObjectName("actionCopy")
       actionCopy.setShortcut('Ctrl+C')

       actionCut = QtGui.QAction(QtGui.QIcon(),'Cortar',self)
       actionCut.setObjectName("actionCut")
       actionCut.setShortcut('Ctrl+X')

       actionPaste = QtGui.QAction(QtGui.QIcon(),'Pegar',self)
       actionPaste.setObjectName("actionPaste")
       actionPaste.setShortcut('Ctrl+V')
       
       actionUndo = QtGui.QAction(QtGui.QIcon(),'Deshacer',self)
       actionUndo.setObjectName("actionUndo")
       actionUndo.setShortcut('Ctrl+Z')

       actionRedo = QtGui.QAction(QtGui.QIcon(),'Rehacer',self)
       actionRedo.setObjectName("actionRedo")
       actionRedo.setShortcut('Ctrl+R')

       self.connect(actionNewStr, QtCore.SIGNAL('triggered()'), self.nuevaEstructura)
       self.connect(actionNewStack, QtCore.SIGNAL('triggered()'), self.nuevoStack)
       self.connect(actionDelStr, QtCore.SIGNAL('triggered()'), self.deleteStr)
       #self.connect(actionDelStack, QtCore.SIGNAL('triggered()'), self.borrarStruct)
       self.connect(actionCut, QtCore.SIGNAL('triggered()'), self.cutElem)
       self.connect(actionCopy, QtCore.SIGNAL('triggered()'), self.copyElem)
       self.connect(actionPaste, QtCore.SIGNAL('triggered()'), self.pasteElem)
       
       self.connect(actionUndo, QtCore.SIGNAL('triggered()'), self.undo)
       self.connect(actionRedo, QtCore.SIGNAL('triggered()'), self.redo)
       
       
       menu = self.menuBar()
       menu.setToolTip('Edicion')
       edicion = menu.addMenu('&Edicion')
       edicion.addAction(actionNewStr)
       edicion.addAction(actionNewStack)
       edicion.addAction(actionDelStr)
       edicion.addAction(actionDelStack)
       edicion.addAction(actionCut)
       edicion.addAction(actionCopy)	
       edicion.addAction(actionPaste)
       edicion.addAction(actionUndo)
       edicion.addAction(actionRedo)
       
   def undo(self):
       self.parent.deshacer()

   def redo(self):
       self.parent.rehacer()

   def crear_menu_file(self):
       actionNew = QtGui.QAction(QtGui.QIcon(),'Nuevo',self)
       actionNew.setObjectName("actionNew")
       actionNew.setShortcut('Ctrl+N')

       actionOpen = QtGui.QAction(QtGui.QIcon(),'Abrir',self)
       actionOpen.setObjectName("actionOpen")
       actionOpen.setShortcut('Ctrl+O')


       actionExit = QtGui.QAction(QtGui.QIcon(),'Salir',self)
       actionExit.setObjectName("actionExit")
       actionExit.setShortcut('Ctrl+Q')

       actionSave = QtGui.QAction(QtGui.QIcon(),'Guardar',self)
       actionSave.setObjectName("actionSave")
       actionSave.setShortcut('Ctrl+S')

       actionSaveAs = QtGui.QAction(QtGui.QIcon(),'Guardar como...',self)
       actionSaveAs.setObjectName("actionSaveAs")
       
       actionOpenConfig = QtGui.QAction(QtGui.QIcon(),'Preferencias',self)
       actionOpenConfig.setObjectName("actionOpenConfig")

       self.connect(actionNew, QtCore.SIGNAL('triggered()'), self.nuevofich)
       self.connect(actionOpen, QtCore.SIGNAL('triggered()'), self.abrir)
       self.connect(actionSaveAs, QtCore.SIGNAL('triggered()'),self.guardarcomo)
       self.connect(actionSave, QtCore.SIGNAL('triggered()'),self.guardar)
       self.connect(actionExit, QtCore.SIGNAL('triggered()'),QtGui.qApp, QtCore.SLOT('quit()'))
       self.connect(actionOpenConfig,QtCore.SIGNAL('triggered()'),self.createPreferenceDialog)

       #menu = self.menuBar()
       menu = QtGui.QMenuBar(self)
       
       menu.setToolTip('Archivo')
       archivo = menu.addMenu('&Archivo')
       archivo.addAction(actionNew)
       archivo.addAction(actionOpen)
       archivo.addAction(actionSave)
       archivo.addAction(actionSaveAs)
       archivo.addAction(actionOpenConfig)
       archivo.addAction(actionExit)
       self.setMenuBar(menu)

   def menu_herramientas(self):
       
       mostrarPreview =  QtGui.QAction(QtGui.QIcon(),'Mostrar ventana Preview',self)
       mostrarPreview.setObjectName("mostrarPreview")
       mostrarPreview.setShortcut('Ctrl+Shift+P')
       self.connect(mostrarPreview, QtCore.SIGNAL('triggered()'), self.mostrarPreview)
       
       mostrarNavegacion =  QtGui.QAction(QtGui.QIcon(),'Mostrar ventana Navegacion',self)
       mostrarNavegacion.setObjectName("mostrarNavegacion")
       mostrarNavegacion.setShortcut('Ctrl+Shift+N')
       self.connect(mostrarNavegacion, QtCore.SIGNAL('triggered()'), self.mostrarNavegacion)
       

       
       menu = self.menuBar()
       menu.setToolTip('Herramientas')
       herramientas = menu.addMenu('&Herramientas')
       herramientas.addAction(mostrarNavegacion)
       herramientas.addAction(mostrarPreview)
       
   def mostrarPreview(self):
       self.lateral_preview.show()
   
   def mostrarNavegacion(self):
       self.lateral_navigation.show()
   #def addRightWidget(self):
   def nuevofich(self):
       print ("Mostrando el dialogo de Nuevo Stack")
       self.definir_espacio();
       while (not self.mdArea.isVisible()):
            self.mdArea.setVisible(True)
            self.mdArea.showNormal()
            self.mdArea.show()

   def createDocks(self):

        self.ppal = QtGui.QWidget()
        self.ppal.setMinimumSize(700,750)
        self.lateral_preview = QtGui.QDockWidget("Preview")
        self.lateral_preview.setMinimumSize(310,375)
        self.lateral_navigation = Arbol(self)
        self.setCentralWidget(self.ppal)
        self.addDockWidget(Qt.DockWidgetArea(2),self.lateral_navigation)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.lateral_preview)
        self.lateral_preview.visibilityChanged.connect(self.cerrando_preview)
        self.lateral_navigation.visibilityChanged.connect(self.cerrando_preview)
        self.lateral_preview.dockLocationChanged.connect(self.cerrando_preview)
        self.lateral_navigation.dockLocationChanged.connect(self.cerrando_preview)
   def cerrando_preview(self):
       if (not self.lateral_preview.isVisible() and not self.lateral_navigation.isVisible()) or (self.lateral_navigation.isFloating() and self.lateral_preview.isFloating()):
           
            self.maximo_tam = True
            rect = self.geometry()
            self.ppal.setGeometry(5,5,rect.width()-15,rect.height()-25)
            self.parent.resizeRender(rect.width()-15,rect.height()-25)
       else:
            self.maximo_tam = False
            rect = self.geometry()
            self.ppal.setGeometry(5,5,rect.width()-320,rect.height()-25)
            self.parent.resizeRender(rect.width()-320,rect.height()-25)
               #QMessageBox(self,"Cerrando ventana","El usuario ha cerrado la ventana").show()
   def refreshNavigation(self,strc):
       self.lateral_navigation.mostrarEstructura(None, strc)
       self.lateral_navigation.show()
   def getPreviewWidget(self):
        return self.lateral_preview
    
   def getMainWidget(self):
        return self.ppal
    
   def getNavigationWidget(self):
        return self.lateral_navigation

   def abrir(self):
    (estr,self.filename) = self.gestorFich.abrir()
    self.setWindowTitle(self.filename+" - "+self.wdname)
    self.parent.initializeEstructura(estr)

   def importar(self):
    (estr, filename) = self.gestorFich.abrir()
    self.parent.importarEstructura(estr)
        

   def guardar(self):
       self.filename = self.gestorFich.guardar(self.parent.returnCubesStr())
       self.setWindowTitle(self.filename+" - "+self.wdname)

   def guardarcomo(self):
       self.filename = self.gestorFich.guardarcomo(self.parent.returnCubesStr())
       self.setWindowTitle(self.filename+" - "+self.wdname)

   def createPreferenceDialog(self):
       self.preferencias = MyDialog(self)
       self.preferencias.setGeometry(20,20,700,250)
       self.preferencias.setWindowTitle("Directorios de archivos guardados")
       self.preferencias.etiqueta_stacks = QtGui.QLabel(self.preferencias)
       self.preferencias.etiqueta_stacks.setText("Directorio de las imagenes:")
       
       self.preferencias.campo_stacks = QtGui.QLineEdit(self.preferencias)
       self.preferencias.campo_stacks.setText(self.configuracion.getStackDir())
       
       self.preferencias.boton_stacks = QtGui.QPushButton(self.preferencias)
       self.preferencias.boton_stacks.setText("Cambiar")
       icon_dir = QtGui.QIcon()
       icon_dir.addPixmap(QtGui.QPixmap("icons/folder.png"))
       self.preferencias.boton_stacks.setIcon(icon_dir)
       self.preferencias.boton_stacks
       self.preferencias.etiqueta_saves = QtGui.QLabel(self.preferencias)
       self.preferencias.etiqueta_saves.setText("Directorio de archivos guardados")
       
       self.preferencias.campo_saves = QtGui.QLineEdit(self.preferencias)
       self.preferencias.campo_saves.setText(self.configuracion.getSaveDir())
       
       self.preferencias.boton_saves = QtGui.QPushButton(self.preferencias)
       self.preferencias.boton_saves.setText("Cambiar")
       self.preferencias.boton_saves.setIcon(icon_dir)

       self.preferencias.boton_aceptar = QtGui.QPushButton(self.preferencias)
       self.preferencias.boton_aceptar.setText("Guardar Cambios")

       self.preferencias.etiqueta_stacks.setGeometry(30,50,240,30)
       self.preferencias.etiqueta_saves.setGeometry(30,100,240,30)
       self.preferencias.campo_stacks.setGeometry(260,50,250,30)
       self.preferencias.campo_saves.setGeometry(260,100,250,30)
       self.preferencias.boton_stacks.setGeometry(520,50,100,30)
       self.preferencias.boton_saves.setGeometry(520,100,100,30)
       self.preferencias.boton_aceptar.setGeometry(30,150,150,30)

       self.preferencias.connect(self.preferencias.boton_stacks,QtCore.SIGNAL('clicked()'),self.buscarDirStacks)
       self.preferencias.connect(self.preferencias.boton_saves,QtCore.SIGNAL('clicked()'),self.buscarDirSaveFiles)
       self.preferencias.connect(self.preferencias.boton_aceptar,QtCore.SIGNAL('clicked()'),self.guardarCambios)

       self.preferencias.show()
   
   def buscarDirStacks(self):
       f = self.preferencias.mostrarVentana(os.getcwd())
       ##f = self.dialogos.getExistingDirectory(self,'Seleccionar directorio',os.getcwd())
       self.preferencias.campo_stacks.setText(f)
       
   def buscarDirSaveFiles(self):
       f = self.preferencias.mostrarVentana(os.getcwd())
       ##f = self.dialogos.getExistingDirectory(self,'Seleccionar directorio',os.getcwd())
       self.preferencias.campo_saves.setText(f)
   def guardarCambios(self):
       self.configuracion.setSaveDir(self.preferencias.campo_saves.text())
       self.configuracion.setStackDir(self.preferencias.campo_stacks.text())
       self.preferencias.close()
       
   def createContextMenu(self,position):
        self.opciones = QMenu()
        self.opciones.actionNewStr = QtGui.QAction(QtGui.QIcon(),'Agregar Estructura',self)
        self.opciones.actionNewStr.setObjectName("actionNewStr")
        self.connect(self.opciones.actionNewStr, QtCore.SIGNAL('triggered()'), self.showNewStrDialog)
        self.opciones.addAction(self.opciones.actionNewStr)
        
        
        self.opciones.actionDelStr = QtGui.QAction(QtGui.QIcon(),'Eliminar Estructura',self)
        self.opciones.actionDelStr.setObjectName("actionDelStr")
        self.connect(self.opciones.actionDelStr, QtCore.SIGNAL('triggered()'), self.deleteStr)
        self.opciones.addAction(self.opciones.actionDelStr)
        ##  self.opciones.actionDelStr.setShortcut('Del')

        self.opciones.actionImportar = QtGui.QAction(QtGui.QIcon(),'Importar fichero',self)
        self.opciones.actionImportar.setObjectName("actionImportar")
        self.connect(self.opciones.actionImportar, QtCore.SIGNAL('triggered()'), self.importar)    
        self.opciones.addAction(self.opciones.actionImportar)

        self.opciones.actionNewStack = QtGui.QAction(QtGui.QIcon(),'Agregar Stack',self)
        self.opciones.actionNewStack.setObjectName("actionNewStack")
        self.connect(self.opciones.actionNewStack, QtCore.SIGNAL('triggered()'), self.nuevoStack)
        self.opciones.addAction(self.opciones.actionNewStack)

        
        self.opciones.actionCopy = QtGui.QAction(QtGui.QIcon(),'Copiar',self)
        self.opciones.actionCopy.setObjectName("actionCopy")
        self.connect(self.opciones.actionCopy, QtCore.SIGNAL('triggered()'), self.copyElem)
        self.opciones.addAction(self.opciones.actionCopy)


        self.opciones.actionPaste = QtGui.QAction(QtGui.QIcon(),'Pegar',self)
        self.opciones.actionPaste.setObjectName("actionPaste")
        self.connect(self.opciones.actionPaste, QtCore.SIGNAL('triggered()'), self.pasteElem)
        self.opciones.addAction(self.opciones.actionPaste)



        self.opciones.actionCut = QtGui.QAction(QtGui.QIcon(),'Cortar',self)
        self.opciones.actionCut.setObjectName("actionCut")
        self.connect(self.opciones.actionCut, QtCore.SIGNAL('triggered()'), self.cutElem)
        self.opciones.addAction(self.opciones.actionCut)
       
        self.opciones.actionInto = QtGui.QAction(QtGui.QIcon(),'Atravesar',self)
        self.opciones.actionInto.setObjectName("actionInto")
        self.connect(self.opciones.actionInto, QtCore.SIGNAL('triggered()'), self.atravesarEstructura)
        self.opciones.addAction(self.opciones.actionInto)
        
        self.opciones.actionOutto = QtGui.QAction(QtGui.QIcon(),'Regresar',self)
        self.opciones.actionOutto.setObjectName("actionOutto")
        self.connect(self.opciones.actionOutto, QtCore.SIGNAL('triggered()'), self.regresarEstructura)
        self.opciones.addAction(self.opciones.actionOutto)
        
        self.opciones.actionRename = QtGui.QAction(QtGui.QIcon(),'Renombrar',self)
        self.opciones.actionRename.setObjectName("actionRename")
        self.connect(self.opciones.actionRename, QtCore.SIGNAL('triggered()'), self.renameElem)
        self.opciones.addAction(self.opciones.actionRename)
        self.parent.rightClick()
        self.opciones.exec_(self.ppal.mapToGlobal(position))

   def disableTreeBranch(self,ruta):
       self.lateral_navigation.disableTreeBranch(ruta)

   def enableTreeBranch(self):
       self.lateral_navigation.enableTreeBranch()


   def highlightNavigation(self,ruta):
       self.lateral_navigation.highlightBranch(ruta)
   
   def highlightMain(self):
       self.lateral_navigation.highlightMain()
       

   def ejecutarAccion(self,accion,ruta):
       if (accion == "navegar"):
           self.parent.showEstructuraByTagPath(ruta)
       if (accion == "renombrar"):
           texto = [[ruta[len(ruta)-1],""]]
           self.renameDialog(texto,ruta)
       if (accion == "borrar"):
            self.borrarEstructura
   def atravesarEstructura(self):
       self.parent.atravesarEstructura()
    
   def regresarEstructura(self):
        self.parent.regresarEstructura()

   def renameElem(self):
       self.parent.renameElem()
        
   def setVoidContextMenu(self,x,y):
      # self.opciones.actionNewStr.setVisible(0)
     #  self.opciones.actionNewStack.setVisible(1)
     #  self.opciones.actionDelStack.setVisible(0)
     #  self.opciones.actionInto.setVisible(0)
     #  self.opciones.actionDelStr.setVisible(0)
     #  self.opciones.actionCopy.setVisible(0)
     #  self.opciones.actionCut.setVisible(0)
     #  self.opciones.actionImportar.setVisible(1)
     #  self.opciones.actionPaste.setVisible(1)
     #  self.opciones.actionOpenStack.setVisible(0) 
       
       self.opciones.setGeometry(x,y,150,240)
       self.opciones.show()
   def mostrarNoSeleccion(self):
       self.opciones.actionNewStr.setVisible(0)
       self.opciones.actionDelStr.setVisible(0)
       self.opciones.actionNewStack.setVisible(0)
       self.opciones.actionInto.setVisible(0)
       self.opciones.actionOutto.setVisible(1)
       self.opciones.actionCopy.setVisible(0)
       self.opciones.actionCut.setVisible(0)
       self.opciones.actionRename.setVisible(0)
       self.opciones.actionPaste.setVisible(0)
       self.opciones.actionImportar.setVisible(0)
   def mostrarSeleccionEstructuras(self,copyCut):
       if copyCut == True:
        self.opciones.actionCopy.setVisible(1)
        self.opciones.actionCut.setVisible(1)
       else:
        self.opciones.actionCopy.setVisible(0)
        self.opciones.actionCut.setVisible(0)
       self.opciones.actionNewStack.setVisible(0)        
       self.opciones.actionNewStr.setVisible(1)
       self.opciones.actionDelStr.setVisible(1)
       self.opciones.actionInto.setVisible(1)
       self.opciones.actionOutto.setVisible(1)
       self.opciones.actionRename.setVisible(1)
       self.opciones.actionPaste.setVisible(0)
       self.opciones.actionImportar.setVisible(0)
   def mostrarSeleccionNodos(self):
       self.opciones.actionNewStr.setVisible(1)
       self.opciones.actionNewStack.setVisible(1)       
       self.opciones.actionDelStr.setVisible(0)
       self.opciones.actionInto.setVisible(0)
       self.opciones.actionOutto.setVisible(1)
       self.opciones.actionCopy.setVisible(0)
       self.opciones.actionCut.setVisible(0)
       self.opciones.actionRename.setVisible(0)
       self.opciones.actionPaste.setVisible(1)
       self.opciones.actionImportar.setVisible(1)   
   def showContextMenu(self):
       self.opciones.show()
   def hideContextMenu(self):
       self.opciones.hide()
       
   def definir_espacio(self):

      self.mdArea = MyDialog(self)
      self.mdArea.setMinimumSize(300,500)
      self.mdArea.move(240,135)
      self.mdArea.setWindowTitle('Definir espacio')
      #self.mdArea.setVisible(1)

      self.mdArea.label_anchura = QtGui.QLabel(self.mdArea)
      self.mdArea.label_altura = QtGui.QLabel(self.mdArea)
      self.mdArea.label_profundidad = QtGui.QLabel(self.mdArea)
      self.mdArea.label_tag = QtGui.QLabel(self.mdArea)
      self.mdArea.aclaracion = QtGui.QLabel(self.mdArea)
      
      
      self.mdArea.label_tag.setText("<p style='font-weight:bold'>Nombre de la estructura:</p>")
      self.mdArea.aclaracion.setText("<p style='font-style:italic;font-size:8.5pt'>(Este nombre le puede ayudar si posteriomente desea<br />importar la estructura y para guardar el archivo)</p>")
      self.mdArea.label_anchura.setText('Ancho:')
      self.mdArea.label_altura.setText('Altura:')
      self.mdArea.label_profundidad.setText('Profundidad:')
      self.mdArea.label_tag.move(30,30)
      self.mdArea.aclaracion.move(30,60)
      
      self.mdArea.label_anchura.move(30,150)
      self.mdArea.label_altura.move(30,210)
      self.mdArea.label_profundidad.move(30,270)

      self.mdArea.boton_aceptar = QtGui.QPushButton(self.mdArea)
      self.mdArea.boton_aceptar.setText("Crear")

      self.mdArea.tam_anchura = QtGui.QSpinBox(self.mdArea)
      self.mdArea.tam_altura = QtGui.QSpinBox(self.mdArea)
      self.mdArea.tam_profundidad = QtGui.QSpinBox(self.mdArea)
      self.mdArea.nombre = QtGui.QLineEdit(self.mdArea)
      self.mdArea.tam_anchura.setMinimum(1)
      self.mdArea.tam_altura.setMinimum(1)
      self.mdArea.tam_profundidad.setMinimum(1)
      
      self.mdArea.nombre.move(30,100)
      self.mdArea.nombre.setMinimumSize(300,30)
      self.mdArea.tam_anchura.move(150,150)
      self.mdArea.tam_altura.move(150,210)
      self.mdArea.tam_profundidad.move(150,270)
      self.mdArea.boton_aceptar.move(90,320)
      #self.mdArea.connect(self.mdArea.boton_aceptar, QtCore.SIGNAL("clicked()"), self.establecer_tam)
      self.mdArea.connect(self.mdArea.boton_aceptar, QtCore.SIGNAL("clicked()"), self.createNewStr)
      self.mdArea.show()
      ##self.mdArea.showNormal()
     
   def cutElem(self):
       self.parent.cortarElem()
          
   def copyElem(self):
       self.parent.copiarElem()

   def pasteElem(self):
       self.parent.pegarElem()
       
   def createNewStr(self):
       
          i = int(self.mdArea.tam_anchura.text())
          j = int(self.mdArea.tam_altura.text())
          k = int(self.mdArea.tam_profundidad.text())
          tag = str(self.mdArea.nombre.text())
          self.mdArea.close()
          self.parent.crearEstructura(i,j,k,tag)

   def  renameDialog(self,textos,ruta = None):
    
      self.dialogRename = MyDialog(self)
      if ruta!=None:
          self.dialogRename.ruta = ruta
      height = len(textos)*40+120
      self.dialogRename.setMinimumSize(400,height)
      self.dialogRename.move(240,135)
      self.dialogRename.setWindowTitle('Renombrar etiquetas')
      self.dialogRename.label = QtGui.QLabel(self.dialogRename)
      self.dialogRename.label.setText("Por favor modifique los nombres de los objetos seleccionados")
      self.dialogRename.label.setMinimumWidth(350)
      self.dialogRename.label.move(30,40)
      self.dialogRename.ruta = ruta
      posicion=70
      self.dialogRename.inputText=[]
      for i in range(len(textos)):
          localizacion = QtGui.QLabel(self.dialogRename)
          insercion = QtGui.QLineEdit(self.dialogRename)
          insercion.setText(textos[i][0])
          insercion.move(30,posicion)
          localizacion.setText(str(textos[i][1]))
          localizacion.move(350,posicion)
          insercion.setMinimumWidth(300)
          self.dialogRename.inputText.append(insercion)
          posicion+=40
      self.dialogRename.boton = QtGui.QPushButton(self.dialogRename)
      self.dialogRename.boton.setText("Renombrar elementos")
      self.dialogRename.boton.move(60,posicion)
      self.dialogRename.boton.setMinimumWidth(180)
      if ruta == None:
          self.dialogRename.connect(self.dialogRename.boton,QtCore.SIGNAL('clicked()'),self.renombrarTags)
      else:
          self.dialogRename.connect(self.dialogRename.boton,QtCore.SIGNAL('clicked()'),self.renombrarTagsByPath)
          
      self.dialogRename.connect(self.dialogRename,QtCore.SIGNAL('close()'),self.cerrarDialog)
      
      self.dialogRename.showDialog()
      
   def cerrarDialog(self):
       ##print "Cerrando dialogo"
       self.setDisabled(False)
       self.dialogRename.hide()
       
   def resetFocus(self):
       self.resetTarget.raise_()
       self.resetTarget.activateWindow()
   def renombrarTags(self):
       nombres = self.parent.returnTagList()
       for elem in self.dialogRename.inputText:
           if elem.text() in nombres:
               m = QtGui.QMessageBox(self)
               m.setWindowTitle("Nombres repetidos")
               m.setText("En un mismo nivel no puede haber dos elementos con el mismo nombre")
               self.resetTarget = self.dialogRename               
               m.buttonClicked.connect(self.resetFocus)
               
               m.show()
      
               return
               
       nuevos_textos = []
       for elem in self.dialogRename.inputText:
           nuevos_textos.append(elem.text())
       self.parent.renameElem(nuevos_textos)
       self.dialogRename.hide()
       self.setDisabled(False)
   def renombrarTagsByPath(self):
       nuevos_textos = []
       nombres = self.parent.returnTagList(self.dialogRename.ruta)
       ##print nombres
       for elem in self.dialogRename.inputText:
           if elem.text() in nombres:
               m = QtGui.QMessageBox(self)
               m.setWindowTitle("Nombres repetidos")
               m.setText("En un mismo nivel no puede haber dos elementos con el mismo nombre")
               self.resetTarget = self.dialogRename
               m.buttonClicked.connect(self.resetFocus)
               
               m.show()
      
               return

       for elem in self.dialogRename.inputText:
           nuevos_textos.append(elem.text())
       self.parent.renameElemByPath(nuevos_textos,self.dialogRename.ruta)
       self.dialogRename.hide()
       self.setDisabled(False)
   def nuevaEstructura(self,i="1",j="1",k="1"):
      
      self.dialEstr = MyDialog(self)
      self.dialEstr.setMinimumSize(280,350)
      self.dialEstr.move(240,135)
      self.dialEstr.setWindowTitle('Definir espacio')

      self.dialEstr.label_anchura = QtGui.QLabel(self.dialEstr)
      self.dialEstr.label_altura = QtGui.QLabel(self.dialEstr)
      self.dialEstr.label_profundidad = QtGui.QLabel(self.dialEstr)
      self.dialEstr.label_tag = QtGui.QLabel(self.dialEstr)

      self.dialEstr.label_anchura.setText('Ancho:')
      self.dialEstr.label_altura.setText('Altura:')
      self.dialEstr.label_profundidad.setText('Profundidad:')
      self.dialEstr.label_tag.setText("Etiqueta")
      
      self.dialEstr.label_anchura.move(30,70)
      self.dialEstr.label_altura.move(30,130)
      self.dialEstr.label_profundidad.move(30,190)
      self.dialEstr.label_tag.move(30,250)
      

      self.dialEstr.boton_aceptar = QtGui.QPushButton(self.dialEstr)
      self.dialEstr.boton_aceptar.setText("Crear")

      self.dialEstr.tam_anchura = QtGui.QSpinBox(self.dialEstr)
      self.dialEstr.tam_altura = QtGui.QSpinBox(self.dialEstr)
      self.dialEstr.tam_profundidad = QtGui.QSpinBox(self.dialEstr)
      self.dialEstr.tag = QtGui.QLineEdit(self.dialEstr)
      
      self.dialEstr.tam_anchura.setMinimum(int(j))
      self.dialEstr.tam_altura.setMinimum(int(i))
      self.dialEstr.tam_profundidad.setMinimum(int(k))
      num_estr = self.parent.getNumEstructuras()
      self.dialEstr.tag.setText("Estructura #"+str(num_estr))
      
      self.dialEstr.tam_anchura.move(150,70)
      self.dialEstr.tam_altura.move(150,130)
      self.dialEstr.tam_profundidad.move(150,190)
      self.dialEstr.tag.move(150,250)
      
      self.dialEstr.boton_aceptar.move(90,290)

      self.dialEstr.connect(self.dialEstr.boton_aceptar, QtCore.SIGNAL("clicked()"), self.agregarEstr)
      self.cont = 0
      self.dialEstr.showDialog()

   def showNewStrDialog(self):
       self.nuevaEstructura()
       self.dialEstr.setVisible(True)
       self.dialEstr.show()
       
   def hideNewStrDialog(self):
       self.dialEstr.hide()

   def agregarEstr(self):
        j = int(self.dialEstr.tam_anchura.text())
        i = int(self.dialEstr.tam_altura.text())
        k = int(self.dialEstr.tam_profundidad.text())
        tag = self.dialEstr.tag.text()
        nombres = self.parent.returnTagList()
        if tag in nombres:
            m = QtGui.QMessageBox(self)
            m.setWindowTitle("Nombres repetidos")
            m.setText("En un mismo nivel no puede haber dos elementos con el mismo nombre")
            self.resetTarget = self.dialEstr
            m.buttonClicked.connect(self.resetFocus)
            m.show()
            return
        if i=="" or j=="" or k=="" or tag=="":
            QMessageBox.about(self,"Error en los datos" ,"Ninguno de los campos puede estar vacio")  
        else:
            self.dialEstr.close()
            self.parent.addNewStruct(i,j,k,tag)
    
   def deleteStr(self):
       ##print "Borrando estructura!"
       self.parent.delStruct()

   def nuevoStack(self):
	self.newStack = MyDialog(self)
	self.newStack.setMinimumSize(460,210)
	self.newStack.move(240,135)
	self.newStack.nom_dir = ""
	self.newStack.setWindowTitle('Crear nuevo Stack')

	## Nombre del stack
	self.newStack.label_nombre = QtGui.QLabel(self.newStack)
	self.newStack.label_nombre.setText('Nombre del Stack:')
	self.newStack.label_nombre.resize(200,25)
	self.newStack.label_nombre.move(20,40)
	self.newStack.label_etiqueta = QtGui.QLineEdit(self.newStack)
	self.newStack.label_etiqueta.move(20,70)
	self.newStack.label_etiqueta.resize(320,25)
	self.newStack.label_etiqueta.setText("")

	## Seleccion del fichero

	self.newStack.boton_abrir = QtGui.QPushButton(self.newStack)
	self.newStack.boton_abrir.setText("Search")
	self.newStack.boton_abrir.move(350,120)

	self.newStack.label_direccion = QtGui.QLineEdit(self.newStack)
	self.newStack.label_direccion.move(20,120)
	self.newStack.label_direccion.resize(320,25)
	self.newStack.label_direccion.setText(self.newStack.nom_dir)
	self.newStack.ok = self.newStack.connect(self.newStack.boton_abrir, QtCore.SIGNAL("clicked()"),self.abrirStack)

	## boton ok
	self.newStack.boton_aceptar = QtGui.QPushButton(self.newStack)
	self.newStack.boton_aceptar.move(150,160)
	self.newStack.boton_aceptar.setText("Asociar")
	self.newStack.connect(self.newStack.boton_aceptar, QtCore.SIGNAL("clicked()"), self.asociarStack)
	self.newStack.showDialog()
   
   def abrirStack(self):
       filename = self.newStack.mostrarVentana(self.configuracion.getStackDir(), "Stack files MHA (*.mha);;Stack files SEG (*.seg)")
       ##filename = self.dialogos.getOpenFileName(self, 'Open file',self.configuracion.getStackDir(),"*.mha")
       #while filename=="" or filename == None:
       #    self.setFocus(Qt.FocusReason)
       #    self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
       f = open(filename)
       aux_name = filename.split("/")
       name = aux_name[len(aux_name)-1]
       self.newStack.label_direccion.setText(filename)
       self.newStack.raise_()
       self.newStack.showDialog()
       #self.newStack.clearFocus()
       #self.newStack.hasFocus()
       #self.newStack.setFocus()
       #self.newStack.focusWidget()
       #self.newStack.topLevelWidget()
       

   def asociarStack(self):
       texto = self.newStack.label_etiqueta.text()
       todoesps= True
       i=0
       while todoesps == True and i < len(texto):
           if texto[i] != " ":
               todoesps = False
           i+=1
       if todoesps == True:
           QMessageBox.about(self,"Nombre erroneo" ,"El nombre no puede estar vacio ni compuesto de espacios")
           self.resetTarget = self.newStack
           self.resetFocus()
       else:
           self.parent.addStack(self.newStack.label_etiqueta.text(),self.newStack.label_direccion.text())
           self.newStack.close()
