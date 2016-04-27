# -*- coding: utf-8 -*-
from copy import deepcopy
from ErrorNav import *
from operator import pos


#!/usr/bin/env python
TIPOS = ("Estructura","Stack","Fichero")

class Estructura():

    def __init__(self,tam = (0,0,0)):
        self.Position = (0,0,0)
        self.tipo = "Estructura"
        self.dimensiones = tam
        self.fichero = ""
        self.estructuras = []
        self.tag = ""
        self.anterior = None


    def addEstructura(self,estructura):
        #print type(estructura.getPosition())
        (x,y,z) = estructura.getPosition()
        (x1,y1,z1) = self.dimensiones
        #print "(",x,",",y,",",z,") (",x1,",",y1,",",z1,")"
        if (x > x1 or y > y1 or z > z1): ## Seria mayor o igual si tomaramos como que el 0,0,0 de una estructura es vacio y no un punto
            raise ErrorNav("OutDim")
        encontrado=False
        i=0
        while not encontrado and i < len(self.estructuras):
            if self.estructuras[i].getPosition() == self.estructuras[i].getPosition:
                self.delEstructura(self.estructuras[i])
                encontrado=True        
            i+=1
        estructura.setAnterior(self)
        self.estructuras.append(estructura)
    def setAnterior(self,ant):
        self.anterior = ant
    def getAnterior (self):
        return self.anterior
    
    def addEstructuraInPos(self,Position,estructura):
        for elem in self.estructuras:
            if elem.getPosition() == Position:
                elem.SetDimension(estructura.getDimension())
                elem.setEstructuras(estructura.getEstructuras())
                elem.setTag(estructura.getTag())
                elem.setFileName(estructura.GetFileName())
                elem.setTipo(estructura.getTipo())
                return
        estructura.setPosition(Position)
        estructura.setAnterior(self)
        self.estructuras.append(estructura)
        
    def setEstructuras(self,estructuras):
        self.estructuras = estructuras
        
    def setPosition(self, pos):
        self.Position = pos
        
    def getPosition(self):
        return self.Position

    def setTag(self,tag_st):
        self.tag = tag_st

    def getTag(self):
        return self.tag

    def setTipo(self,tipo):
        if tipo in TIPOS:
		    self.tipo = tipo
        else:
            raise "Error en el tipo de estructura"

    def getTipo(self):
       return self.tipo

    def setDimension(self,dim):
        self.dimensiones = dim

    def getDimension(self):
        return self.dimensiones

    def setFileName(self,name):
        self.fichero = name

    def getFileName(self):
        return self.fichero


    def getEstructuras(self):
        return self.estructuras[:]

    def getNumEstructuras(self):
        return len(self.estructuras)

    def getNumDepthEstructura(self):
        cnt = 0
        if (len(self.estructuras)>0):
            ls = self.estructuras[:]
            while len(ls) != 0:
                aux = ls.pop()
                cnt+=1
                if (aux.getNumEstructuras() >0 ):
                    ls.append(aux.getEstructuras())
        return cnt

    def getEstructuraInPos(self,pos):
        for elem in self.estructuras:
            if elem.getPosition() == pos:
                return deepcopy(elem)

    def delEstructuraInPos(self,pos):
        encontrado = False
        i=0
        for elem in self.estructuras:
            if elem.getPosition() == pos:
                self.estructuras.remove(elem)
                return
        return
    
    def getEstructuraByTag(self,tag):
        lista = []
        for e in self.estructuras:
            lista.append(e.getTag())
        if tag == self.tag:
            return self
        for elem in self.estructuras:
            if elem.getTag() == tag:
                return elem
        return None

    def delEstructura(self,obj):
        self.estructuras.remove(obj)

    def delIndexEstructura(self,num):
        del self.estructuras[num]


class GestorEstructura:
    def __init__(self):
        self.ptr_estructura_ini = None
        self.ptr_estructura = None
        self.ptr_anterior = []
        self.num = 0
    
    def isEmpty(self):
        return self.ptr_estructura_ini == None
    
    def initializeGestor(self,estruct):
        (x,y,z) = estruct.getDimension()
        if (x ==0 and y==0 and z==0):
            return None
        else:
            self.num = 1
            self.ptr_estructura = estruct
            self.ptr_estructura_ini = estruct
            if (len(estruct.getEstructuras())>0):
                ls = estruct.getEstructuras()
                while len(ls) != 0:
                    aux = ls.pop()
                    self.num+=1
                    if (aux.getNumEstructuras() >0 ):
                        ls += aux.getEstructuras()
                        
    def searchEstructuraByTagPath(self,tags):
        
        if self.getEstructura().getTag() == tags[0] and len(tags) == 1:
            return self.getEstructura()
        if self.getEstructura().getTag() == tags[0] and len(tags) > 1:
            estr = self.getEstructura()
        else:
            estr = None
        encontrado = False
        i = 1
        while i < len(tags) and encontrado == False and estr != None:
            estr = estr.getEstructuraByTag(tags[i])
            if i == (len(tags) -1):
                encontrado = True
            i+=1
        if encontrado == True:
            return estr
        else:
            return None
    
    def getTagPath(self,tag):
        lista = [tag]
        ptr = self.getActualEstructura()
        if ptr == self.ptr_estructura_ini and ptr.getTag() == tag:
            return lista
        if self.getActualEstructura().getTag() == tag:
            ptr = ptr.getAnterior()
        while ptr != self.ptr_estructura_ini:
            lista.append( ptr.getTag() )
            ptr = ptr.getAnterior()
        lista.append(self.ptr_estructura_ini.getTag())
        return list(reversed(lista))
      
    def addEstructura(self,struct):
        if struct.getPosition() == "":
            raise ErrorNav('NoPos')
        if struct.getTag() =="":
            if (struct.getNumEstructuras() > 0):
                compuesta = "compuesta "
            else:
                compuesta =""
            tag = "Estructura "+compuesta+str(self.num+1)
            struct.setTag(tag)
        self.ptr_estructura.addEstructura(struct)                    
        self.num +=1
        if (len(struct.getEstructuras())>0):
            ls = struct.getEstructuras()
            while len(ls) != 0:
                aux = ls.pop()
                print aux
                self.num+=1
                if (aux.getNumEstructuras() >0 ):
                    ls = ls + aux.getEstructuras()

        
    def addEstructuraInPos(self,pos,struct):
        #print "Agregar Estructura en Position"
        self.ptr_estructura.addEstructuraInPos(pos,struct)
        self.num+=1
        
    def getActualEstructura(self):
        return self.ptr_estructura
    def getEstructura(self):
        return self.ptr_estructura_ini
    
    def delEstructuraInPos(self,pos):
        print "Borrar Estructura en Position"
        self.ptr_estructura.delEstructuraInPos(pos)
        self.num -=1
        
    def delEstructura(self,struct):
        for elem in self.ptr_estructura.getEstructuras():
            if elem == struct:
                del elem
                self.num -=1
        print "Elimina la estructura struct en el nivel en el que estamos"
    
    def delEstructuraByTag(self,tag):
        print "Borra una estructura con un tag dado"    
        estructura = self.searchEstructuraByTag(tag)
        self.ptr_estructura.delEstructura(estructura)
        
    def getTagList(self):
        
        lista_tags = []
        lista_tags.append(self.ptr_estructura_ini.getTag())
        #print "Obtener una lista de tags de toda la estructura"
        ls = self.ptr_estructura_ini.getEstructuras()
        while len(ls) != 0:
            aux = ls.pop()
            lista_tags.append(aux.getTag())
           # print "Revisando ",aux.getNumEstructuras()," estructuras mas"
            if (aux.getNumEstructuras() >0 ):
                ls = ls + aux.getEstructuras()
        return lista_tags
    
    def setEstructuraInPos(self,pos,estructura):
        print "Cambia los valores de la estructura en la Position 'pos' "
    
    def backToEstructura(self):
        self.ptr_estructura = self.ptr_anterior.pop(len(self.ptr_anterior)-1)
        #if (self.ptr_estructura.getAnterior())
    def moveToEstructura(self,estructura):
        
        if estructura == self.ptr_estructura_ini:
            self.ptr_estructura = self.ptr_estructura_ini
            return
        
        #print "Desplaza el puntero en la estructura"
        #print type(self.ptr_estructura_ini)
        ls = self.ptr_estructura_ini.getEstructuras()
        while len(ls) != 0:
            aux = ls.pop()
            if aux == estructura:
                #print "Estructura objetivo detectada"
                self.ptr_anterior.append(aux.getAnterior())
                self.ptr_estructura = aux
                return 
            #print "Revisando ",aux.getNumEstructuras()," estructuras mas"
            if (aux.getNumEstructuras() >0 ):
                ls = ls + aux.getEstructuras()

    def getEstructuraInPos(self,pos):
        
        for elem in self.ptr_estructura.getEstructuras():
            #print "(",elem.getPosition(),",",pos,")"
            if elem.getPosition() == pos:
                return elem
        return None
    
    def moveToEstructuraByTag(self,tag):
    
        print "Desplazamos el puntero por el tag"
        estructura = self.searchEstructuraByTag(tag)
        self.ptr_anterior.append(estructura.getAnterior())
        self.ptr_estructura = estructura
    
    def getNumberOfEstructuras(self):
        return self.num
    def printEstructuras(self):
        lista=[]
        for elem in self.ptr_estructura.getEstructuras():
            lista.append("P:"+str(elem.getPosition())+",D:"+str(elem.getDimension())+",T:"+elem.getTag())
        print lista
if __name__=="__main__":

    
    def crearEstructura(dim,estructura = None):
        for i in range(dim):
            for j in range(dim):
                for k in range (dim):
                  #  print "Position",i,",",j,",",k," <<"
                    struct = Estructura()
                    struct.setDimension((1, 1, 1))
                    etiqueta = "Estructura "+str(i)+"-"+str(j)+"-"+str(k)
                    struct.setTag(etiqueta)
                    estructura.addEstructuraInPos((i, j, k),struct)
                    del struct
        print "Se han creado ", estructura.getNumEstructuras(), " estructuras"

    gestor = GestorEstructura()
    struct = Estructura()
    dim = (3,3,3)
    struct.setDimension(dim)
    struct.setTag("Estructura principal")
    gestor.initializeGestor(struct)
    nueva_estructura = Estructura()
    nueva_estructura.setPosition((2,2,2))
    nueva_estructura.setDimension((3,4,5))
    gestor.addEstructura(nueva_estructura)
   # print gestor.getTagList()
  #  print "NUM ",gestor.getNumberOfEstructuras()
    est1 = Estructura()
    crearEstructura(3,est1)
    est1.setPosition((0,1,2))
    for elem in est1.getEstructuras():
            (i,j,k) = elem.getPosition()
            if j == 2:
                struct1 = est1.getEstructuraInPos((i,j,k))
                crearEstructura(2, struct1)
                est1.delEstructuraInPos((i,j,k))
                est1.addEstructuraInPos((i,j,k), struct1)
    gestor.addEstructura(est1)
    #print "NUM ",gestor.getNumberOfEstructuras()
    #print gestor.getTagList()
    