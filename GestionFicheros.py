import os, sys
import pickle
from Configuracion import Configuracion
import json
from PyQt4 import QtCore, QtGui
from Estructura import *
class GestionFicheros:
    
    titulo = ""
    
    def __init__(self,parent=None,config=None):
        self.titulo = "Untitled"
        self.parent = parent
        if config == None:
            self.dir = os.getenv('HOME')
            self.config = None
        else:
            self.config = config
            self.dir = self.config.getSaveDir()
        
    def writeJSON(self,estr):
        d = dict()
        print estr.getTipo()
        d['position'] = str(estr.getPosition())
        d['tag'] = str(estr.getTag())
        d['dimension'] = str(estr.getDimension())
        d['type'] = estr.getTipo()
        d['file'] = str(estr.getFileName())
        lista = []
        if (estr.getNumEstructuras() > 0):
            for e in estr.getEstructuras():
                lista.append(self.writeJSON(e))
            d['estructs'] = lista
        print d
        return d
        
    def readJSON(self,des):
        d = des['dimension'].replace("(","").replace(")","").split(",")
        dim = (int(d[0]),int(d[1]),int(d[2]))
        estr = Estructura(dim)
        estr.setTag(des['tag'])
        p = des['position'].replace("(","").replace(")","").split(",")
        pos = (int(p[0]),int(p[1]),int(p[2]))
        estr.setPosition(pos)
        estr.setTipo(des['type'])
        estr.setFileName(des['file'])
        if des.has_key("estructs"):
            lista = list(des['estructs'])
            if len(lista) > 0:
                for elem in lista:
                    e1 = self.readJSON(elem)
                    estr.addEstructura(e1)
        return estr
        
    def GetNameFile(self):
        return self.titulo

    def guardar(self,estr):
        if self.titulo=="Untitled":
            nombre_fich = self.guardarcomo(estr)
            self.titulo = nombre_fich
        else:
               self.salvarenfich(self.titulo,estr)
        return self.titulo
    
    def guardarcomo(self,estr):

        self.titulo = QtGui.QFileDialog.getSaveFileName(self.parent, 'Save File', self.dir)
        self.salvarenfich(self.titulo,estr)
        return self.titulo
        
    def salvarenfich(self,filename,estr):
        if ".stc" in filename:
           fich = open(filename,'w')
        else:
            fich = open(filename+'.stc','w')
        json.dump(self.writeJSON(estr),fich)
        #texto = self.writeJSON(json.estr)
        #fich.write()
        fich.close()

    def abrir(self):

        self.filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file',self.dir,"*.stc")
        #self.setWindowTitle(filename+" - "+self.wdname)
        f = open(self.filename)
        print self.filename
        d = json.load(f)
        estr = self.readJSON(d)
        return (estr,self.filename)
        #self.estructura_cubos = []
        #self.estructura_cubos = pickle.load(f)
        #(self.altura,self.anchura,self.profundidad) = self.estructura_cubos.getDimension()
        #self.pantalla.GetRenderWindow().GetRenderers().RemoveAllItems()


    def getFileName(self):
        return self.filename    