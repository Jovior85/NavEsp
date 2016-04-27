
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Estructura import *

class Arbol(QDockWidget):
    def __init__(self,parent = None):
        QDockWidget.__init__(self)
        self.parent = parent
        self.arbol= QTreeWidget(parent)
        self.setWindowTitle("Navegacion")
        self.arbol.setHeaderLabel("Navegacion")
        self.setWidget(self.arbol)
        self.estructura = Estructura()
        self.arbol.setExpandsOnDoubleClick(False)
        self.arbol.setContextMenuPolicy(Qt.CustomContextMenu)
        self.arbol.customContextMenuRequested.connect(self.menu)
        self.dobleclick = False
        self.actualEstructura = None
        self.arbol.itemDoubleClicked.connect(self.navegarAEstructura)
        self.last_selected = None
    def struct(self):

        self.crearEstructura(3)
        for elem in self.estructura.getEstructuras():
            (i,j,k) = elem.getPosicion()
            if j == 2:
                struct = self.estructura.getEstructuraInPos((i,j,k))
                self.crearEstructura(2, struct)
                self.estructura.delEstructuraInPos((i,j,k))
                self.estructura.agregarEstructura((i,j,k), struct)
        self.mostrarEstructura()
        
    def getListTagPath(self,item):
        parent = item.parent()
        lista = [item.text(0)]
        while parent != None:
            lista.append(parent.text(0))
            parent = parent.parent()
        ##print lista
        return list(reversed(lista))
    
    def searchBranchByPath(self,ruta):
        item = self.arbol.topLevelItem(0)
        print "RUTA::: ",ruta

        if item.text(0) != ruta[0]:
            print "Error en el primer elemento de la ruta"
            return
        else:
            print "Se encontro el nodo principal"
            if len(ruta) == 1:
                return item
        ruta.pop(0)
        encontrado = False
        while not encontrado and len(ruta)> 0: # Bucle que se encarga de recorrer toda la ruta
            
            sig_child= False
            i=0
            elem = item.child(0)
            while not sig_child and elem != None: #Bucle que recorre cada secuencia de items
                #print "comparamos:",elem.text(0),",",ruta[0]
                if elem.text(0) == ruta[0]:
                    #print "acierto! Len ruta es :",len(ruta)
                    sig_child=True
                    item = elem
                    if len(ruta) == 1:
                        #print "Encontrado el elemento. Bloqueamos"
                        encontrado = True
                        
                        return item
                    ruta.pop(0)
                else:
                    i +=1
                    elem = item.child(i)
        '''            
        if not encontrado:
            print "No se ha encontrado el elemento"
        else:
            print "El elemento se ha bloqueadooooooo"
         '''
    def highlightMain(self):
        item = self.arbol.topLevelItem(0)
        item.setSelected(True)
    
    def highlightBranch(self,ruta):
        if self.last_selected != None:
            try:
                self.last_selected.setSelected(False)
            except:
                self.last_selected = None
                
        item = self.searchBranchByPath(ruta)
        item.setSelected(True)
        self.last_selected = item
    
    def disableTreeBranch(self,ruta):
        item = self.searchBranchByPath(ruta)
        item.setDisabled(True)
        item.setExpanded(False)
        self.disable_branch = item
    
    def enableTreeBranch(self):
        if self.disable_branch != None:
            self.disable_branch.setDisabled(False)
    
    def navegarAEstructura(self,obj=None,event=None):
        if (obj == None and event==None):
            items = self.arbol.selectedItems()
            lista =  self.getListTagPath(items.pop())
            self.parent.ejecutarAccion("navegar",lista)
        else:
            if obj.isDisabled() != True:
                self.last_selected =obj
                lista = self.getListTagPath(obj)
                self.parent.ejecutarAccion("navegar",lista)
    
    def colorItem(self,nombre):
        index = self.arbol.selectedIndexes()
    
    def menu(self,position):
        indexes = self.arbol.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level +=1
            menu = QMenu()
            if level >= 0:
                actionGoTo = QAction(self)
                actionGoTo.setText("Ir a...")
                self.arbol.connect(actionGoTo, SIGNAL("triggered()"),self.navegarAEstructura)
                menu.addAction(actionGoTo)
                actionRename = QAction(self)
                actionRename.setText("Renombrar")
                actionRename.setShortcut("Ctrl+R")
                self.arbol.connect(actionRename, SIGNAL("triggered()"),self.renameElem)
                menu.addAction(actionRename)
            '''
            if level > 0:
                actionDelete = QAction(self)
                actionDelete.setText("Borrar")
                actionDelete.setShortcut("Del")
                self.arbol.connect(actionDelete, SIGNAL("triggered()"),self.deleteElem)
                menu.addAction(actionDelete)
            '''
            menu.exec_(self.arbol.viewport().mapToGlobal(position))
    def renameElem(self):
        items = self.arbol.selectedItems()
        lista =  self.getListTagPath(items.pop())
        self.parent.ejecutarAccion("renombrar",lista)
    
    def deleteElem(self):
        items = self.arbol.selectedItems()
        lista =  self.getListTagPath(items.pop())
        self.parent.ejecutarAccion("borrar",lista)
            
    
    def crearEstructura(self,dim,estructura = None):
        if estructura == None:
            estructura = self.estructura
            texto = "Estructura"
        else:
            texto = "Subestructura "
        for i in range(dim):
            for j in range(dim):
                for k in range (dim):
                   ## print "posicion",i,",",j,",",k," <<"
                    struct = Estructura()
                    struct.setDimension((1, 1, 1))
                    etiqueta = texto+str(i)+"-"+str(j)+"-"+str(k)
                    struct.setTag(etiqueta)
                    estructura.agregarEstructura((i, j, k),struct)
                    del struct
        ##for elem in estructura.getEstructuras():
        ##    print "STR : ",elem.getTag()," - ",elem.getPosicion()
    

    def mostrarEstructura(self,nodo = None,estructura = None,actualEstructura = None):
        if estructura == None:
            estructura = self.estructura
        if nodo == None:
            self.arbol.clear()
            nodo = QTreeWidgetItem(self.arbol)
            nodo.setText(0,estructura.getTag())

        for elem in estructura.getEstructuras():
            #if nodo == self.arbol:
            #    print "Creamos nodo"
            #else:
            #    print "Creamos subnodo"

            subnodo = QTreeWidgetItem(nodo)
            subnodo.setExpanded(True)
            nodo.setExpanded(True)
            etiqueta = elem.getTag()
            subnodo.setText(0,etiqueta)
            if elem.getTipo() == "Stack":
                subnodo.setTextColor(0,QColor(170,170,170))
            if len(elem.getEstructuras())>0:
               # print "Tiene ", len(elem.getEstructuras()) , " dentro"
                self.mostrarEstructura(subnodo, elem)
                ##        self.arbol.itemDoubleClicked.connect(self.navegarAEstructura)
        
      #  self.arbol.itemClicked.connect(self.eventoRaton)