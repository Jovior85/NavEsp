

class UndoRedo():
    
    def __init__(self,parent=None):
        self.listaundo = []
        self.listaredo = []
        self.parent = parent
        self.multiaccion = False
    def setEstructura(self,estructura):
        self.estructura_cubos = estructura

    def addAction(self,action,opciones):
        self.listaundo.append((action,opciones))
        self.listaredo = []
       ## print self.listaundo
    def addMultiaction(self,accion):
        self.multiaccion = True
        self.listaundo.append(("Multiaccion",accion))
       # print "Multiaccion - enabled"
    def endMultaction(self):
        #print "Multiacction - disabled"
        self.listaundo.append(("Fin Multiaccion"))
        self.multiaccion = False
        
    def isMultiaction(self):
        #print "Es multiaccion: ",self.multiaccion
        return self.multiaccion
    
    def doAction(self,pila):
        if pila == 0:
            action,opciones  = (self.listaundo.pop(len(self.listaundo)-1))
        else:
            action,opciones  = (self.listaredo.pop(len(self.listaredo)-1))
        if (action == "crear"):
            ptr, pos = opciones
            self.estructura_cubos.moveToEstructura(ptr)
            struct = self.estructura_cubos.getEstructuraInPos(pos) 
            self.estructura_cubos.delEstructuraInPos(pos)
            action1 = "eliminar"
            opciones1 = (self.estructura_cubos.getActualEstructura(),pos,struct)
            
        if (action == "eliminar"):
            ptr, pos,estructura = opciones
            self.estructura_cubos.moveToEstructura(ptr)
            self.estructura_cubos.addEstructuraInPos(pos,estructura)
            action1 = "crear"
            opciones1 = (self.estructura_cubos.getActualEstructura(),pos)

        if (action == "renombrar"):
            ptr,pos,tag = opciones
            if ptr == None: #Estructura principal
                
                ant_tag = self.estructura_cubos.getEstructura().getTag()
                self.estructura_cubos.getEstructura().setTag(tag)
            else:

                #self.estructura_cubos.moveToEstructura(ptr)
                ant_tag = self.estructura_cubos.getEstructuraInPos(pos).getTag()
                self.estructura_cubos.getEstructuraInPos(pos).setTag(tag)
                            
            action1 = "renombrar"
            opciones1 = ptr,pos,ant_tag
            
        return action1,opciones1
    
    def getUndo(self):
        if (len(self.listaundo) == 0):
            return None
        else:
          ##  print self.listaundo
            if (self.listaundo[len(self.listaundo)-1] == "Fin Multiaccion"):
                ini = self.listaundo.pop(len(self.listaundo)-1)
                
                lista = []
                while not (self.listaundo[len(self.listaundo)-1][0] == "Multiaccion"):
                   ## print self.listaundo
                    action,opciones = self.doAction(0)
                    lista.append((action,opciones))
                fin = self.listaundo.pop(len(self.listaundo)-1)
                self.listaredo.append(fin)
                for elem in reversed(lista):
                    self.listaredo.append(elem)
                self.listaredo.append(ini)
              #  print self.listaredo
            else:
            
                action,opciones = self.doAction(0)
                self.listaredo.append((action,opciones))
            if opciones[0] == None: #No hay estructura anterior, por lo tanto es la principal
                self.parent.showMainEstructura(self.estructura_cubos.getEstructura())
            else:
                self.parent.showMainEstructura(opciones[0])
            self.parent.refreshNavigation()
    def getRedo(self):
        if (len(self.listaredo) == 0):
            return None
        else:
            
            if (self.listaredo[len(self.listaredo)-1] == "Fin Multiaccion"):
                ini = self.listaredo.pop(len(self.listaredo)-1)
                
                lista = []
                while not (self.listaredo[len(self.listaredo)-1][0] == "Multiaccion"):
                    action,opciones = self.doAction(1)
                    lista.append((action,opciones))
                fin = self.listaredo.pop(len(self.listaredo)-1)
                self.listaundo.append(fin)
                (self.listaundo.append(elem) for elem in reversed(lista))
                self.listaundo.append(ini)
            else:
                action,opciones = self.doAction(1)
                self.listaundo.append((action,opciones))
            self.parent.showMainEstructura(opciones[0])
            self.parent.refreshNavigation()
