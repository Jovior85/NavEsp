# -*- coding: utf-8 -*-

from Renderer import *
from Ventana import *
from Estructura import *
from copy import deepcopy
from UndoRedo import UndoRedo
class NavEsp:

    def __init__(self):

        self.show_malla=1
        self.listFreeNodes = []
        self.listOccupiedNodes = []
        self.selectedObjects = []
        self.objectBelow= None
        self.estructura_cubos = GestorEstructura()
        self.ventana = Ventana(self)
        self.render = Render(self)
        self.render_preview = Render(self)
        self.undoredo = UndoRedo(self)
        self.undoredo.setEstructura(self.estructura_cubos)
        self.copiedElems = []
        self.cutElems = []
        self.render.setVTKMainWidget(self.ventana.getMainWidget())
        self.render_preview.setVTKPreviewWidget(self.ventana.getPreviewWidget())
        self.ventana.show()
        self.render.setMouseEvents()
        self.render_preview.showRender()
        self.render.showRender()
        self.num_estructuras = 0

    def visualizacion(self,num):
        self.render.setStereo(num) 
       
            
    def defineColor(self,element,action):
        '''
            Over: Mouse is over the object
            Selected: Object is selected
            OverSelected: Mouse is over a selected item
            Normal: Normal state of item - Depends on the item
        '''
        
        if (action == "Over"):
            #self.render.setColor((0,1,0), element)
            self.render.setBrightness(element)
        elif (action == "Selected"):
            self.render.setColor((0.4,0.6,0.3),element)
            self.render.unsetBrightness(element)
        elif (action == "OverSelected"):
            #self.render.setColor((0.9,0.8,0.5),element)
            self.render.setBrightness(element)
        elif (action == "Normal"):
            #lista = [e[1] for e in self.listFreeNodes]
            for e in self.listFreeNodes:
                if element == e[1]:
                    self.render.setColor((0.7,0.7,0.7),element)
            for e in self.listOccupiedNodes:
                if element == e[1]:
              #  for elem in self.listOccupiedNodes:
                    if self.estructura_cubos.getEstructuraInPos(e[0]).getTipo() == "Stack":
                        stru = self.estructura_cubos.getEstructuraInPos(e[0])
                        f = stru.getFileName()
                        if os.path.exists(f):
                            self.render.setColor((0.7,0.7,0.7), element)
                        else:
                            self.render.setColor((0.7,0,0), element)
                    else:
                        self.render.setColor((.0,.3,.6),element)
                    ## Stack self.render.setColor((0.5,0,0.7),element)
            self.render.unsetBrightness(element)

    def isSelected(self,actor):
        for elem in self.selectedObjects:
            if elem == actor:
                return True
        return False;
    
    def moveThrough(self,o,e):
        pos = self.render.getPosition()
        (x,y,z) = pos
        actor = self.render.isSomethingPick(o,e)
        
        if (actor != None): # Hay un elemento debajo del raton
            if self.isSelected(actor): # Si estamos sobre un objeto seleccionado lo pintamos de una manera y sino de otra.
                self.defineColor(actor, "OverSelected")
            else:
                self.defineColor(actor, "Over")
                
            if (self.objectBelow != None and actor!= self.objectBelow): # El elemento es distinto al que estabamos debajo antes
                if self.isSelected(self.objectBelow): # Si el objeto esta seleccionado lo pintamos de rojo nuevamente
                    self.defineColor(self.objectBelow, "Selected")
                else: # Sino lo devolvemos a su color original.
                    self.defineColor(self.objectBelow, "Normal")
            self.objectBelow = actor # Cambiamos el actor que tenemos debajo
                
        else:
            
            if (self.objectBelow != None): ## No estamos encima de nada pero hay un elemento en el que estabamos antes
                if self.isSelected(self.objectBelow):
                    self.defineColor(self.objectBelow, "Selected")
                else:
                    self.defineColor(self.objectBelow, "Normal")
                self.objectBelow = None
        
   
        self.render.updateRender()
    
    
    
    def clickOnWorld(self,o,e):
        #self.render_preview.clearRender()
        self.render_preview.updateRender()
        ##print "Click en el nuevo Worlddddd"
        actor = self.render.isSomethingPick(o,e)
        if (actor != None):
            ## Seleccionamos el objeto y lo metemos en la lista de objetos seleccionados
            
            if len(self.selectedObjects) > 0 and not self.isSelected(actor) and self.render.getMultiseleccion() ==False:
               # print "Seleccion multiple sin control"
                #Si ya habia algun elemento en la lista
                #Si no esta pulsado el control borramos la lista y coloreamos elementos al color standard
                for elem in self.selectedObjects:
                    (x,y,z) = elem.GetCenter()
                    self.render.deleteText((round(x,1),round(y,1),round(z,1)))
                    self.ventana.showMessageInStatusBar("")

                    self.defineColor(elem, "Normal")
                        #self.render.setColor((0.5,0.5,0.5), elem)
                del self.selectedObjects
                
                self.selectedObjects = []

            if not self.isSelected(actor):
               # print "Objeto que queremos seleccionar. Agregando elemento"
                #Si no estaba seleccionado lo pintamos de nuevo y lo agregamos a la lista
                self.defineColor(actor, "Selected")
                #self.render.setColor((1,0,0),actor)
                (x,y,z) = actor.GetCenter()
               # print "El objeto seleccionado es ", str((round(x,1),round(y,1),round(z,1)))
                #print self.estructura_cubos.printEstructuras()
                estr = self.estructura_cubos.getEstructuraInPos((round(x,1),round(y,1),round(z,1)))
                color=False
                if estr!= None:
                    if estr.getTipo() == "Stack":
                        fichero = "\nFichero:\n"+estr.getFileName()
                        self.ventana.showMessageInStatusBar(fichero)
                        nombre = fichero.split("/")
                        nom = "\nFichero: "+nombre[len(nombre)-1]
                        if not os.path.exists(estr.getFileName()):
                            color = True
                        else:
                            color=False
                    else:
                        nom = ""
                    texto = estr.getTag()+"\n"+"POS: "+str(estr.getPosition())+"\nTipo: "+str(estr.getTipo())+nom+"\n"
                    self.render.createText((round(x,1),round(y,1),round(z,1)), str(texto),color)
                    
                self.selectedObjects.append(actor)
            else:
                #print "Objeto deseleccionado: Lo sacamos de la lista"
                #Si ya estaba seleccionado lo sacamos de la lista
                self.defineColor(actor, "Over")
                #self.render.setColor((1,1,1),actor)
                (x,y,z) = actor.GetCenter()
                self.render.deleteText((round(x,1),round(y,1),round(z,1)))
                self.selectedObjects.remove(actor)
            
            if len(self.selectedObjects) == 1:
                
                for actores in self.listOccupiedNodes:
                    if actor == actores[1]:
                    #    print "Preview del nodooooo!!!",actores[0]
                        if (self.estructura_cubos.getEstructuraInPos(actores[0]).getTipo() != "Stack"):
                            self.showEstructura(self.estructura_cubos.getEstructuraInPos(actores[0]), self.render_preview);
                        #self.render_preview.clearRender()
                        #self.render_preview.insertActor(actor)
                        #self.render_preview.updateRender()
 
            
        else:
            for elem in self.selectedObjects:
                self.defineColor(elem, "Normal")
                    #self.render.setColor((0.5,0.5,0.5), elem)
                (x,y,z) = elem.GetCenter()
                self.render.deleteText((round(x,1),round(y,1),round(z,1)),True)
                self.ventana.showMessageInStatusBar("")
            self.render.updateRender()

            del self.selectedObjects
            self.selectedObjects = []
    
    
    #def rightClick(self,o,e):
    def rightClick(self):
        if len(self.selectedObjects) == 0:
            self.ventana.mostrarNoSeleccion()
        if len(self.selectedObjects) > 0:
            todasStr = True
            i=0
            while todasStr and i< len(self.selectedObjects):
                ocupado=False
                j=0
                while j < len(self.listOccupiedNodes) and not ocupado:
                    if self.listOccupiedNodes[j][1] == self.selectedObjects[i]:
                        ocupado=True
                    j+=1
                if not ocupado:
                    todasStr = False
                i+=1

            todosNodos = True
            i=0
            while todosNodos and i< len(self.selectedObjects):
                ocupado=False
                j=0
                while j < len(self.listFreeNodes) and not ocupado:
                    if self.listFreeNodes[j][1] == self.selectedObjects[i]:
                        ocupado=True
                    j+=1
                if not ocupado:
                    todosNodos = False
                i+=1
                    
            if todasStr:
                if len(self.selectedObjects) ==1:
                    self.ventana.mostrarSeleccionEstructuras(True)
                else:
                    self.ventana.mostrarSeleccionEstructuras(False)
            elif todosNodos:
                self.ventana.mostrarSeleccionNodos()            
        #self.ventana.showContextMenu()
        #print o
        # print "##",e
        (x,y) = self.render.getClickCoords()
        #print "(",x,",",768-y,")"
        if self.objectBelow != None and len(self.selectedObjects) !=  0:
            #print "Left Click"
            self.ventana.setVoidContextMenu(x,y)
  
    def cortarElem(self):
        ## Se crea un objeto con el actor cortado
        self.copiedElems = []
        if (len(self.cutElems) >0):
           # print "Estamos en el unset"
            #print str(self.selectedObjects[0].getPosition())##+"///"+str(self.cutElems[0].getPosition())
            #if self.selectedObjects[0].getPosition() == self.cutElems[0].getPosition():
            for elem in self.listOccupiedNodes:
                self.render.unsetTransparency(elem[1])
            self.cutElems = []
            self.render.updateRender()
        if len(self.selectedObjects) == 1:
            encontrado = False
            i=0
            while not encontrado and i<len(self.listOccupiedNodes):
                nodo = self.listOccupiedNodes[i]
                if self.selectedObjects[0] == nodo[1]:
                    self.render.setTransparency(self.selectedObjects[0])
                    encontrado=True
                    #cubo = self.estructura_cubos.getEstructuraInPos(nodo[0])
                    #self.cutElems.append(cubo)
                    
                    tag = self.estructura_cubos.getEstructuraInPos(nodo[0]).getTag() #Buscamos el tag
                   ## print "El tag del elemento a cortar es", tag
                    estr = self.estructura_cubos.getActualEstructura().getEstructuraByTag(tag)
                    actual = self.estructura_cubos.getActualEstructura()
                    posicion = estr.getPosition()
                    opciones = actual,posicion,estr
                    ruta = self.estructura_cubos.getTagPath(tag) # Cogemos la ruta al objeto
                    self.cutElems.append((self.selectedObjects[0],opciones))
                    ##print "RUTA NAVESP ::: ",ruta
                    #print "Nodos ocupados" , self.listOccupiedNodes
                    #print "Elemento cortado : ", self.cutElems
                    #print "Elementos seleccionados: ", self.selectedObjects
                    
                    self.render.updateRender()
                    
                    self.ventana.disableTreeBranch(ruta)
                i+=1
            if (not encontrado):
                self.ventana.showMessageInStatusBar("No se puede cortar dicho elemento")
        elif len(self.selectedObjects) > 1:
            self.ventana.showMessageInStatusBar("No se puede cortar mas de un elemento a la vez")   
        else:
            self.ventana.showMessageInStatusBar("No se puede cortar sin haber previamente seleccionado un objeto")   
            return
    def copiarElem(self):
       # print "Copiando"
        del self.copiedElems
        self.copiedElems = []

        if (len(self.cutElems) >0):
            #print "Estamos en el unset"
            #print str(self.selectedObjects[0].getPosition())##+"///"+str(self.cutElems[0].getPosition())
            #if self.selectedObjects[0].getPosition() == self.cutElems[0].getPosition():
            for elem in self.listOccupiedNodes:
                self.render.unsetTransparency(elem[1])
            self.cutElems = []
            self.ventana.enableTreeBranch()
            self.render.updateRender()
        if len(self.selectedObjects) == 1:
            encontrado = False
            i=0
            while not encontrado and i<len(self.listOccupiedNodes):
                nodo = self.listOccupiedNodes[i]
                if self.selectedObjects[0] == nodo[1]:
                    encontrado=True
                    cubo = self.estructura_cubos.getEstructuraInPos(nodo[0])
                    self.copiedElems.append(cubo)
                i+=1
       # print "Elemento a copiar el de pos ",self.copiedElems[0].getPosition()
    
    def pegarElem(self):
        encontrado = False
        i =0
        ##print "INI",self.estructura_cubos
        # La copia de un elemento que se quiere pegar en otra posicion libre (o varias)
        
        if len(self.copiedElems) ==1:
            if (len(self.selectedObjects) > 1 and not self.undoredo.isMultiaction()):
                self.undoredo.addMultiaction("copiar")
            j=0
            for elem in self.selectedObjects: ##Iteramos sobre todos los objetos para pegar el cubo en las posiciones selecccionadas.
                cubo = Estructura()
                cubo.setDimension(self.copiedElems[0].getDimension())
                cubo.setTipo(self.copiedElems[0].getTipo())
                cubo.setFileName(self.copiedElems[0].getFileName())
                existe = True
                while existe:
                    if j==0:
                        eti = self.copiedElems[0].getTag()
                    else:
                        eti = self.copiedElems[0].getTag()+" #"+str(j) 
                    est = self.estructura_cubos.getActualEstructura().getEstructuraByTag(eti)
                    if est != None:
                        j+=1
                    else:
                        existe= False
                cubo.setTag(eti)
                cubo.setEstructuras(self.copiedElems[0].getEstructuras())
                self.ocuparNodo(elem, cubo)
                
            i+=1
            if (self.undoredo.isMultiaction()):
                self.undoredo.endMultaction()
            self.render.updateRender()
            self.estructura_cubos.printEstructuras()
            self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())
        elif len(self.cutElems) == 1:
            if len(self.selectedObjects) == 0:
                return
            self.undoredo.addMultiaction("Cortar")
            self.copiedElems = []
            
            #self.copiedElems.append(self.cutElems[0])
            actor,opciones = self.cutElems[0]
            struct = self.liberarNodo(actor,opciones)
            self.copiedElems.append(struct)

            self.cutElems = []
            self.pegarElem() 
 
            self.render.updateRender()
            self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())
   ## def ocuparNodo(self,pos,estruct):
               
    def getNumEstructuras(self):
        return self.num_estructuras;
    def doubleClickOnItem(self,o,e):
        pos = self.render.getPosition()
        (x,y,z) = pos
        actor = self.render.isSomethingPick(o,e)
        if actor != None:
            #lista = [e[1] for e in self.listOccupiedNodes]
            for e in self.listOccupiedNodes:
                if actor == e[1]:
                    self.selectedObjects = []
                    self.selectedObjects.append(actor)
                    if (self.estructura_cubos.getEstructuraInPos(e[0]).getTipo()!= "Stack"):
                        if len(self.cutElems) >0 and actor == self.cutElems[0]:
                            self.ventana.showMessageInStatusBar("No se puede acceder a una estructura cortada")
                            return
                        self.atravesarEstructura()
                    else:
                        
                        ##Codigo para abrir los stacks de espina.
                        
                        #esp = os.getenv("ESPINA", "NO PATH")
                        #print "Abriedo ",esp,". Fichero: ",str(self.estructura_cubos.getEstructuraInPos(e[0]).getFileName())
                        if os.path.exists(self.estructura_cubos.getEstructuraInPos(e[0]).getFileName()):
                            res = os.system("espina "+str(self.estructura_cubos.getEstructuraInPos(e[0]).getFileName())+" &")
                        else:
                            self.ventana.showMessageInStatusBar("El fichero: "+str(self.estructura_cubos.getEstructuraInPos(e[0]).getFileName())+" no existe en el sistema")
                        #print "------",res,"-----------"
                        #if (res == -1):
                        #    os.system("python espina.py "+str(self.estructura_cubos.getEstructuraInPos(e[0]).getFileName()))
    def atravesarEstructura(self):
        
        if (len(self.selectedObjects) == 1):
            encontrado = False
            i=0
            while not encontrado and i < len(self.listOccupiedNodes):
                if self.listOccupiedNodes[i][1] == self.selectedObjects[0]:
                    actual = self.estructura_cubos.getEstructuraInPos(self.listOccupiedNodes[i][0])
                    self.estructura_cubos.moveToEstructura(actual)
                    self.showEstructura(self.estructura_cubos.getActualEstructura(), self.render, True)
                    encontrado = True
                    self.selectedObjects = []
                    tag = actual.getTag()
                    ruta = self.estructura_cubos.getTagPath(tag) # Cogemos la ruta al objeto
                    self.ventana.highlightNavigation(ruta)
                i+=1
            
    def regresarEstructura(self):
        self.estructura_cubos.backToEstructura()
        estructura = self.estructura_cubos.getActualEstructura()
        self.showEstructura(estructura, self.render, True)
        tag = estructura.getTag()
        ruta = self.estructura_cubos.getTagPath(tag) # Cogemos la ruta al objeto
        self.ventana.highlightNavigation(ruta)
    def returnTagList(self,ruta=None):
        if ruta ==None:
            estructura = self.estructura_cubos.getActualEstructura()
        else:
            estructura = self.estructura_cubos.searchEstructuraByTagPath(ruta).getAnterior()
        if estructura == None:
            estructura = self.estructura_cubos.getEstructura()
       # print estructura.getTag()
        lista_tags = []
        for elem in estructura.getEstructuras():
            lista_tags.append(elem.getTag())
        return lista_tags

    def renameElemByPath(self,textos,ruta):
        if len(ruta) == 1:
            opciones = None,self.estructura_cubos.getEstructura(),self.estructura_cubos.getEstructura().getTag()
            self.undoredo.addAction("renombrar",opciones )
            self.estructura_cubos.getEstructura().setTag(textos[0])
        else:
            estruct = self.estructura_cubos.searchEstructuraByTagPath(ruta)
            anterior = estruct.getAnterior()
            opciones = anterior,estruct.getPosition(),estruct.getTag()
            self.undoredo.addAction("renombrar", opciones)
            estruct.setTag(textos[0])
        self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())
    def renameElem(self,textos = None):
        lista_estructuras = []
        lista_textos = []
            
        if (len(self.selectedObjects) > 1):
            self.undoredo.addMultiaction("renombrar")
        for elem in self.selectedObjects:
            for ocupados in self.listOccupiedNodes:
                if ocupados[1] == elem:
                    lista_estructuras.append(self.estructura_cubos.getEstructuraInPos(ocupados[0]))
                    lista_textos.append((self.estructura_cubos.getEstructuraInPos(ocupados[0]).getTag(),self.estructura_cubos.getEstructuraInPos(ocupados[0]).getPosition()))
        if textos != None and len(textos) == len(lista_estructuras):
            for i in range(len(lista_estructuras)):
                self.undoredo.addAction("renombrar", (self.estructura_cubos.getActualEstructura(),lista_estructuras[i].getPosition(),lista_estructuras[i].getTag()))
                lista_estructuras[i].setTag(textos[i])
        else:
            self.ventana.renameDialog(lista_textos)
        if (self.undoredo.isMultiaction()):
            self.undoredo.endMultaction()
        self.render.updateRender()
        self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())

    def returnCubesStr(self):
        return self.estructura_cubos.getEstructura()

    def createVertexList(self):
        cnt=1
        self.listFreeNodes = []
        self.listOccupiedNodes = []
        for n in range(0,self.altura+1):
            for s in range(0,self.anchura+1):
                for t in range(0,self.profundidad+1):
                    ##print "Dibujamos esfera ",cnt
                    actorEsfera = self.render.addSphere(n,s,t)
                    self.listFreeNodes.append(((n,s,t),actorEsfera))
                    cnt+=1
        self.render.updateRender()
      #  print (self.listFreeNodes)

    def resizeRender(self,x,y):
        self.render.resize(x,y)
    
    def showEstructuraByTagPath(self,tags):
        estruct = self.estructura_cubos.searchEstructuraByTagPath(tags)
        if estruct != None:
            if estruct.getTipo() == "Stack":
                ##print "La estructura seleccionada es un stack"
                if os.path.exists(estruct.getFileName()):
                            res = os.system("espina "+str(estruct.getFileName())+" &")
                else:
                    self.ventana.showMessageInStatusBar("El fichero: "+str(estruct.getFileName())+" no existe en el sistema")
                return
            self.estructura_cubos.moveToEstructura(estruct)
            self.showEstructura(estruct, self.render, True)
            
    def showMainEstructura(self,estructura):
        self.showEstructura(estructura, self.render, True )
          
    def showEstructura(self,estructura,render, rewriteEstado = False):
     #   print estructura
        i,j,k = estructura.getDimension()
        
        render.clearRender()
        render.removeActors()
        render.crear_malla((i,j,k))
        nodos = estructura.getEstructuras()
        if (rewriteEstado == True):
            del self.listFreeNodes
            del self.listOccupiedNodes
            self.listFreeNodes = []
            self.listOccupiedNodes = []
            
        for posi in range(0,i+1):
            for posj in range(0,j+1):
                for posk in range(0,k+1):
                    encontrado = False
                    cnt = 0
                    while encontrado == False and cnt < len(nodos):
                        nx,ny,nz = nodos[cnt].getPosition()
                        if (nx == posi and ny == posj and nz== posk):
                          #  print "--------------------------",(nx,ny,nz)
                          #  print self.estructura_cubos.getEstructuraInPos((nx,ny,nz))
                            if estructura.getEstructuraInPos((nx,ny,nz)).getTipo() == "Stack":
                                actor_cubo = render.addCube((nx,ny,nz),nodos[cnt].getDimension(),True)

                                stru = estructura.getEstructuraInPos((nx,ny,nz))
                                f = stru.getFileName()
                                if not os.path.exists(f):
                                     #self.render.setColor((0,0.7,0.7), actor_cubo)
                                #else:
                                    self.render.setColor((0.7,0,0), actor_cubo)
                            else:
                                actor_cubo = render.addCube((nx,ny,nz),nodos[cnt].getDimension(),False)
                                self.render.setColor((0,0,0.7),actor_cubo)
                                if len(self.cutElems) !=0:
                                    actor, opciones = self.cutElems[0]
                                    ptr, pos, str = opciones
                                    if estructura == ptr and pos == (nx,ny,nz):
                                        render.setTransparency(actor_cubo)
                            
                            
                            if (rewriteEstado == True):
                                self.listOccupiedNodes.append(((nx,ny,nz),actor_cubo))
                            encontrado = True                         
                        cnt +=1 
                    if encontrado == False:
                        
                        actor_esfera = render.addSphere(posi,posj,posk)
                        if (rewriteEstado == True):
                            self.listFreeNodes.append(((posi,posj,posk),actor_esfera))

                        
                    
        render.setCamera()
        if (self.show_malla == 0):
            self.render.hideMalla()
        else:
            self.render.showMalla()
                    
        render.showRender()

        render.updateRender()
    def refreshNavigation(self):
        self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())    
    
    def addStack(self,tag,fich):
         
        ##CREAR STACK        
        cont = 0
        if len(self.selectedObjects) > 1:
            self.undoredo.addMultiaction("Crear")
        
        for elem in self.selectedObjects:
            nuevocubo = Estructura((1,1,1))
            nuevocubo.setTipo("Stack")
            nuevocubo.setFileName(fich)
            if cont > 0:
                nuevocubo.setTag(tag+" #"+str(cont))

            else:
                nuevocubo.setTag(tag)
            cont+=1
            self.ocuparNodo(elem, nuevocubo)
        ##print "La estructura queda: ",self.estructura_cubos.printEstructuras()
        if self.undoredo.isMultiaction():
            self.undoredo.endMultaction()
        ##if len(self.selectedObjects) == 1:
        ##    self.showEstructura(nuevocubo, self.render_preview)        
        ##self.render_preview.clearRender()
        
    def addNewStruct(self,i,j,k,tag):
         

        ##CREAR CUBO        
        cont = 0
        
        if len(self.selectedObjects) > 1:
            self.undoredo.addMultiaction("Crear")
        
        for elem in self.selectedObjects:
            nuevocubo = Estructura((i,j,k))
            if cont > 0:
                nuevocubo.setTag(tag+" #"+str(cont))

            else:
                nuevocubo.setTag(tag)
            cont+=1
            self.ocuparNodo(elem, nuevocubo)
        ##print "La estructura queda: ",self.estructura_cubos.printEstructuras()
        if self.undoredo.isMultiaction():
            self.undoredo.endMultaction()
        if len(self.selectedObjects) == 1:
            self.showEstructura(nuevocubo, self.render_preview)
    
    def deshacer(self):
        self.undoredo.getUndo()
    def rehacer(self):
        self.undoredo.getRedo()
    def delStruct(self):
        if len(self.selectedObjects) > 1:
            self.undoredo.addMultiaction("Crear")
        
        for elem in self.selectedObjects:
            self.liberarNodo(elem)
        if self.undoredo.isMultiaction():
            self.undoredo.endMultaction()
        ##print "La estructura queda: ",self.estructura_cubos.printEstructuras()
        #self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())
        #self.render.updateRender()
        
    def crearEstructura(self,i,j,k,tag=""):
        ##print "Nueva estructura : (",i,",",j,",",k,")"
        self.altura = i
        self.anchura = j
        self.profundidad = k
        self.estructura_cubos = GestorEstructura()
        del self.undoredo
        self.undoredo = UndoRedo(self)
        self.undoredo.setEstructura(self.estructura_cubos)
        struct = Estructura()
        struct.setDimension((i,j,k))
        self.num_estructuras = 1
        if tag == "":
            struct.setTag("Estructura principal")
        else:
            struct.setTag(tag)
        self.estructura_cubos.initializeGestor(struct)
        self.render.clearRender()
        self.ventana.refreshNavigation(self.estructura_cubos.getActualEstructura())
        self.ventana.highlightMain()
        self.showEstructura(self.estructura_cubos.getActualEstructura(), self.render,rewriteEstado=True)
        self.render_preview.clearRender()
        
    def visualizarMalla(self):
        if (self.show_malla == 0):
            self.render.showMalla()
            self.show_malla=1
        else:
            self.render.hideMalla()
            self.show_malla=0
  
    def getStatusEstructura(self):
        return self.estructura_cubos.getEstructura()

    def ocuparNodo(self,actor,estructura):
        encontrado = False
        x=0
        while not encontrado and x < len(self.listFreeNodes):
            elem = self.listFreeNodes[x]
            if elem[1] == actor:
                posicion = elem[0]
                estructura.setPosition(posicion)
                encontrado = True
                #self.estructura_cubos.addEstructuraInPos(pos, estructura)    
                if estructura.getTipo() == "Stack":
                    im = True
                else:
                    im = False
                cubo = self.render.addCube(posicion, estructura.getDimension(),im)
                
                ##if estructura.getTipo() == "Stack":
                   ## self.render.setColor((0,0.7,0.7), cubo)
                
                
                self.listOccupiedNodes.append((posicion,cubo))
                self.listFreeNodes.remove(elem)
                self.render.deleteActor(elem[1])
            x+=1
        if encontrado:
            self.estructura_cubos.addEstructuraInPos(posicion, estructura)
            self.num_estructuras+=1
            opciones = self.estructura_cubos.getActualEstructura(),posicion
            self.undoredo.addAction("crear", opciones)

        self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())
        self.render.updateRender()
    
            
    def liberarNodo(self,actor,opciones=None):
        
        #Liberar un nodo: Si es un borrado se le pasara el actor y el gestionara las estructuras,
        # Si proviende de la acción de cortar, se le indica los valores del elemento directamente
        # para proceder al borrado
        
        encontrado = False
        x=0
       ## print "LIBERAR NODO - lista de nodos ocupados : ", self.listOccupiedNodes
       ## print "LIBERAR NODO - actor :", actor 
        while not encontrado and x < len(self.listOccupiedNodes):
            # elem in self.listOccupiedNodes:
            elem = self.listOccupiedNodes[x]
             
            if elem[1] == actor:
                encontrado = True
                
                posicion = elem[0]
                (i,j,k) = elem[0]
                esfera = self.render.addSphere(round(i,0), round(j,0), round(k,0))
                self.listFreeNodes.append(((round(i,0), round(j,0), round(k,0)),esfera))
                self.listOccupiedNodes.pop(x)
                self.render.deleteActor(elem[1])
            x+=1
        if encontrado or opciones != None:
            if opciones == None:
                opciones = self.estructura_cubos.getActualEstructura(),posicion,self.estructura_cubos.getEstructuraInPos(posicion)
                self.undoredo.addAction("eliminar", opciones)
                borrada = self.estructura_cubos.getEstructuraInPos(posicion)
                self.estructura_cubos.delEstructuraInPos(posicion)
            else:
                self.undoredo.addAction("eliminar", opciones)
                estr_actual, pos,estr = opciones
                borrada = estr
                estr_actual.delEstructuraInPos(pos)
                
            self.ventana.refreshNavigation(self.estructura_cubos.getEstructura())
            self.render.updateRender()
            return borrada
        return
    def initializeEstructura(self,estructura):
        self.estructura_cubos = GestorEstructura()
        self.estructura_cubos.initializeGestor(estructura)
        del self.undoredo
        self.undoredo = UndoRedo(self)
        self.undoredo.setEstructura(self.estructura_cubos)
        self.copiedElems = []
        self.cutElems = []
        self.showEstructura(estructura, self.render, True)
        self.ventana.refreshNavigation(estructura)
    def importarEstructura(self,estructura):
        if (len(self.selectedObjects) > 0):
            for elem in self.selectedObjects:
                self.ocuparNodo(elem, estructura)