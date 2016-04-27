# -*- coding: utf-8 -*-


#from vtk import *
from PyQt4 import QtGui,QtCore

import vtk,threading

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#from PyQt4 import QtGui,QtCore
#import math
#from pyasn1.compat.octets import null
from vtk.util.misc import vtkGetDataRoot
import thread

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,parent=None):
        self.AddObserver("RightButtonPressEvent",self.middleButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent",self.middleButtonReleaseEvent)

    def middleButtonPressEvent(self,obj,event):
        ##print "Middle Button pressed"
      #  self.OnMiddleButtonDown()
        return
 
    def middleButtonReleaseEvent(self,obj,event):
        ##print "Middle Button released"
        self.OnRightButtonUp()
        return



class Render():

    def __init__(self,parent=None):
        self.parent = parent
        self.render= vtk.vtkRenderer()
        self.pantalla= None
        self.malla = []
        self.textos = []
        self.multiseleccion = False


    def addSphere(self,i,j,k):
        esfera = vtk.vtkSphereSource()
        esfera.SetRadius(0.15)#0.075
        esfera.SetCenter(float(i),float(j),float(k))            
        esfera.SetThetaResolution(12)
        esfera.SetPhiResolution(12)
        '''
        jpegfile = "/home/jose/Documentos/PFC/PFC/sphere_1.jpg"
        # Read the image data from a file
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(jpegfile)
                # Create texture object
        texture = vtk.vtkTexture()
        if vtk.VTK_MAJOR_VERSION <= 5:
            texture.SetInput(reader.GetOutput())
        else:
            texture.SetInputConnection(reader.GetOutputPort())
        # Map texture coordinates
        map_to_sphere = vtk.vtkTextureMapToSphere()
        if vtk.VTK_MAJOR_VERSION <= 5:
            map_to_sphere.SetInput(esfera.GetOutput())
        else:
            map_to_sphere.SetInputConnection(esfera.GetOutputPort())
        map_to_sphere.PreventSeamOn()
         
        # Create mapper and set the mapped texture as input
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(map_to_sphere.GetOutput())
        else:
            mapper.SetInputConnection(map_to_sphere.GetOutputPort())
        '''
        
        planeMapper = vtk.vtkPolyDataMapper()
        planeMapper.SetInputConnection(esfera.GetOutputPort())
        planeActor = (vtk.vtkActor())
        planeActor.SetMapper(planeMapper)#mapper planeMapper
       ## planeActor.SetTexture(texture)
        planeActor.GetProperty().SetColor(0.7,0.7,0.7)
        planeActor.GetProperty().SetDiffuse(0.5)
        planeActor.GetProperty().SetSpecular(0.4)
        self.render.AddActor(planeActor)
        return planeActor

    def createText(self,(x,y,z),texto, color = False ):
        
        rep = vtk.vtkCaptionActor2D()
        rep.SetCaption(texto)
        rep.GetTextActor().GetTextProperty().SetJustificationToCentered()
        rep.GetTextActor().GetTextProperty().SetVerticalJustificationToCentered()
        if color != False:
            rep.GetTextActor().GetTextProperty().SetColor(0.5,0.2,0.2)
            rep.GetTextActor().GetTextProperty().SetShadow(0)
            rep.GetTextActor().GetTextProperty().SetBold(1)


        else:
            rep.GetTextActor().GetTextProperty().SetColor(1.0,1.0,1.0)
            rep.GetTextActor().GetTextProperty().SetShadow(0)
            rep.GetTextActor().GetTextProperty().SetBold(1)
        rep.SetAttachmentPoint(x,y,z)
        rep.PickableOff()
        self.render.AddActor2D(rep)
        #print "TEXTO AGREGAR : ",str((x,y,z))
        encontrado = False
        for elem in self.textos:
            if elem[0] == (x,y,z):
                encontrado = True
        if encontrado == False:
            self.textos.append(((x,y,z),rep))
        return

        #widget = vtk.vtkCaptionWidget()
        #widget.SetInteractor(self.pantalla)
        #widget.SetCaptionActor2D(rep)
        #widget.On()
        #texto = vtk.vtkTextActor()
        #texto.GetTextProperty().SetFontSize(12)
        #texto.SetPosition2(10, 40)
        #self.render.AddActor2D(texto)
        #texto.SetInput("Texto de prueba")
        #texto.GetTextProperty().SetColor(1.4,0.0,0.0)
       ## texto.SetBackgroundColor(0.9,0.9,0.9)
    def deleteText(self,(x,y,z),all=False):
        if all:
            for elem in self.textos:
                self.deleteActor(elem[1])
            del self.textos
            self.textos = []
        else:
            #print "TEXTO QUITAR : ",str((x,y,z))
            i=0
            #print self.textos
            for i in range(len(self.textos)):
                if self.textos[i][0] == (x,y,z):
                    self.deleteActor(self.textos[i][1])
                    self.textos.pop(i)
                    self.updateRender()
                    return
                i+=1
        
    def addCube(self,pos,tam,img=False):
        jpegfile = "struct.jpg"
        
        # Read the image data from a file
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(jpegfile)
         
        (x,y,z) = pos
        (i,j,k) = tam

        cubito = vtk.vtkCubeSource()
        cubito.SetXLength(0.2*i)
        cubito.SetYLength(0.2*j)
        cubito.SetZLength(0.2*k)
        cubito.SetCenter((x,y,z)) 
        if img == True:
            
            # Create texture object
            texture = vtk.vtkTexture()
            if vtk.VTK_MAJOR_VERSION <= 5:
                texture.SetInput(reader.GetOutput())
            else:
                texture.SetInputConnection(reader.GetOutputPort())
            # Map texture coordinates
            map_to_sphere = vtk.vtkTextureMapToPlane()
            if vtk.VTK_MAJOR_VERSION <= 5:
                map_to_sphere.SetInput(cubito.GetOutput())
            else:
                map_to_sphere.SetInputConnection(cubito.GetOutputPort())
            #map_to_sphere.PreventSeamOn()
             
            # Create mapper and set the mapped texture as input
            mapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(map_to_sphere.GetOutput())
            else:
                mapper.SetInputConnection(map_to_sphere.GetOutputPort())
            
        

        planeMapper = vtk.vtkPolyDataMapper()
        planeMapper.SetInputConnection(cubito.GetOutputPort())
        planeActor = (vtk.vtkActor())
        if (img == True):
            planeActor.SetMapper(mapper)
        else:
            planeActor.SetMapper(planeMapper)# mapper planeMapper
        planeActor.DragableOn()
        planeActor.SetDragable(1)
        if (img== True):
            planeActor.SetTexture(texture)
        else:
            planeActor.GetProperty().SetColor(.0,.3,.6)
            planeActor.GetProperty().SetOpacity(0.95)
        #planeActor.GetProperty().SetAmbient(0)
        #planeActor.GetProperty().SetDiffuse(0.9)
        #planeActor.GetProperty().SetSpecular(0.1)
        self.render.AddActor(planeActor)
        
        return planeActor
    
    def unsetTransparency(self,actor):
       actor.GetProperty().SetOpacity(1.0)
    
    def setTransparency(self,actor):
       actor.GetProperty().SetOpacity(0.3)

    def setBrightness(self,actor):
        actor.GetProperty().SetSpecular(0.8)
    def unsetBrightness(self,actor):
        actor.GetProperty().SetSpecular(0.3)

    def clearRender(self):
        ##self.stopFPS()
        self.pantalla.GetRenderWindow().RemoveRenderer(self.render)
        del self.render
        self.render= vtk.vtkRenderer()
        self.pantalla.GetRenderWindow().AddRenderer(self.render)
        self.multiseleccion = False
        
    def getFPS(self):
        self.fps = 1.0/ self.render.GetLastRenderTimeInSeconds()
        print "FPS:", self.fps
    def startFPS(self):
        self.threadFPS = threading.Timer(5,self.getFPS())
        

    
    def stopFPS(self):
        print "Stopping FPS..."
        
    def removeActors(self):
       ## self.render.Clear()
        self.render.RemoveAllViewProps()
        '''
        actores = self.render.GetActors()
        i=0
        actor = actores.GetNextItem()
        while (actor):
            self.render.RemoveActor(actor)
            actor = actores.GetNextItem()
        '''
    def resize(self,x,y):
        self.pantalla.setGeometry(5,5,x,y)

    def setVTKMainWidget(self,widget):
        self.pantalla = vtk.qt4.QVTKRenderWindowInteractor.QVTKRenderWindowInteractor(widget)
        self.pantalla.GetRenderWindow().AddRenderer(self.render)
        ##print "(10,10,",widget.width,",",widget.height,")"
      #  self.pantalla.setGeometry(5,5,0,0)
        self.pantalla.RemoveAllObservers()     
        self.pantalla.AddObserver("KeyPressEvent",self.Keypress);
        self.pantalla.AddObserver("KeyReleaseEvent",self.Keyrelease);

    def setVTKPreviewWidget(self,widget):
        self.pantalla = vtk.qt4.QVTKRenderWindowInteractor.QVTKRenderWindowInteractor(widget)
        self.pantalla.GetRenderWindow().AddRenderer(self.render)
        ##print "(10,10,",widget.width,",",widget.height,")"
        self.pantalla.setGeometry(5,30,300,300)
        #self.pantalla.AddObserver("KeyPressEvent",self.Keypress);
        #self.pantalla.AddObserver("KeyReleaseEvent",self.Keyrelease);



    def Keyrelease(self,o,e):
        #print "Release : ", o.GetKeySym()
        self.multiseleccion = False
        
    def Keypress(self,o,e):
        #print "Esta siiii ",o
        
        if (o.GetControlKey() == 1) :
            self.multiseleccion = True;
       ## self.pantalla.setGeometry(10,10,widget.width(),widget.height())

        ##self.pantalla.setGeometry(0,0,0,0)
    def getMultiseleccion(self):
        return self.multiseleccion
    
    def setMouseEvents(self):
        picker = vtk.vtkPropPicker()
        self.pantalla.SetPicker(picker)
        self.pantalla.AddObserver("MouseMoveEvent", self.parent.moveThrough)#MouseMoveEvent,LeftButtonPressEvent
        self.pantalla.AddObserver("LeftButtonPressEvent", self.clickedLeft)
        #self.pantalla.AddObserver("RightButtonPressEvent", self.parent.rightClick)#MouseMoveEvent,LeftButtonPressEvent

    def clickedLeft(self,o,e):
       # print e
        #self.parent.clickOnLeft(o,e)
        if self.pantalla.GetRepeatCount() == 1:
            self.parent.doubleClickOnItem(o,e)
        self.parent.clickOnWorld(o,e)
    def isSomethingPick(self,o,e):
        picker = self.pantalla.GetPicker()
        x,y = self.pantalla.GetEventPosition()
        if picker.PickProp(x,y,self.pantalla.GetRenderWindow().GetRenderers().GetFirstRenderer()):
           # if picker == None:
           #     print "There is not picker!"
           # else:
           #     print "Picker Object! " # , picker.GetViewProp()
            if (picker.GetViewProp() == None):
                  ## print "there would be ... ", self.picker.GetViewProp()
                   actores = self.pantalla.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()
                  ## print actores
        return picker.GetViewProp()
    
    def getClickCoords(self):
        return self.pantalla.GetEventPosition()
        
    def showRender(self):
        
        jpegfile = "/home/jose/Documentos/PFC/PFC/sphere.jpg"
        # Read the image data from a file
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(jpegfile)
        reader.Update()
                # Create texture object
        texture = vtk.vtkTexture()
        
        if vtk.VTK_MAJOR_VERSION <= 5:
            texture.SetInput(reader.GetOutput())
        else:
            texture.SetInputConnection(reader.GetOutputPort())
        #self.render.SetTexturedBackground(True)
        
        #self.render.SetBackgroundTexture(texture)
        self.render.GradientBackgroundOn()
        self.render.SetBackground2(0.4,0.5,0.9)
        self.render.SetBackground(0.3,0.3,0.3)

        self.pantalla.Initialize()
        self.pantalla.Start()
    
    def updateRender(self):
        self.pantalla.Render()
       ## self.startFPS()

    def getRenderIterator(self):
        return self.pantalla

    def insertActor(self,Actor):
        self.render.AddActor(Actor)
        
    def deleteActor(self,Actor):
        self.render.RemoveActor(Actor)

    def setCamera(self):
       ## self.camera = vtk.vtkInteractorStyleTrackballCamera()
        self.pantalla.SetInteractorStyle(MyInteractorStyle())
        self.render.ResetCamera()

    def crear_malla(self,punto):
    	pos_x = punto[0]
    	pos_y = punto[1]
    	pos_z = punto[2]
    	tam_i = pos_x * 1.0
    	tam_j = pos_y * 1.0
    	tam_k = pos_z * 1.0
        cnt = len(self.malla)
        if (cnt > 1):
            del self.malla
            self.malla = []
	#for i in range(len(self.actores)):
		#print self.actores
		#if self.actores[i][0] == "malla":
		   #for elem in self.actores[i][1]:
			#self.ren1.RemoveActor(elem)
		   #del self.actores[i]
		   #break;
         # actores = self.render.GetActors()
         #elem = actores.GetNextItem()
         # while (elem):
         #     self.render.RemoveActor(elem)
         #     elem = actores.GetNextItem()
	##self.pantalla.RemoveRenderer(self.render)
	##del self.render
	##self.render= vtk.vtkRenderer()
	##self.pantalla.GetRenderWindow().AddRenderer(self.render)
    	for j in range(0,(pos_y+1)):
    		axis_j = j * 1.0
    		for i in range(0,(pos_x+1)):
    			axis = i * 1.0
    			plano = vtk.vtkLineSource()
    			plano.SetPoint1(axis,axis_j,0.0)
    			plano.SetPoint2(axis,axis_j,tam_k)
    			planeMapper = vtk.vtkPolyDataMapper()
    			planeMapper.SetInputConnection(plano.GetOutputPort())
    			planeActor = (vtk.vtkActor())
    			planeActor.SetMapper(planeMapper)
    			planeActor.PickableOff()
    			self.malla.append(planeActor)
    		for i in range(0,(pos_z+1)):
    			axis = i * 1.0
    			plano = vtk.vtkLineSource()
    			plano.SetPoint1(0.0,axis_j,axis)
    			plano.SetPoint2(tam_i,axis_j,axis)
    			planeMapper = vtk.vtkPolyDataMapper()
    			planeMapper.SetInputConnection(plano.GetOutputPort())
    			planeActor = (vtk.vtkActor())
    			planeActor.SetMapper(planeMapper)
    			planeActor.PickableOff()
                
    			self.malla.append(planeActor)
    
    	for j in range(0,(pos_z+1)):
    		axis_j = j * 1.0
    		for i in range(0,(pos_x+1)):
    			axis = i * 1.0
    			plano = vtk.vtkLineSource()
    			plano.SetPoint1(axis,0.0,axis_j)
    			plano.SetPoint2(axis,tam_j,axis_j)
    			planeMapper = vtk.vtkPolyDataMapper()
    			planeMapper.SetInputConnection(plano.GetOutputPort())
    			planeActor = (vtk.vtkActor())
    			planeActor.SetMapper(planeMapper)
    			planeActor.PickableOff()
    			self.malla.append(planeActor)
    	self.showMalla()
    	#for i in range(len(malla)):
    	#	self.render.AddActor(malla[i])
    	##self.actores.append(["malla",malla])
    	##self.actualizarRender(self.ren1)
    def showMalla(self):
        for i in range(len(self.malla)):
            self.render.AddActor(self.malla[i])
        self.pantalla.Render()
        
    def hideMalla(self):
        for i in range(len(self.malla)):
		    self.render.RemoveActor(self.malla[i])
        self.pantalla.Render()
    
    def isMallaActor(self,actor):
        for i in range(len(self.malla)):
            if (actor == self.malla[i]):return True
        return False
    
    def setStereo(self,num):
        if num == 1:
            self.pantalla.GetRenderWindow().SetStereoRender(0)
           ## self.render.StereoRenderOff()
            ##self.render.SetSteroCapableWindow(0)
        else:
            ##self.render.StereoRenderOn()
            ##self.render.SetStereoCapableWindow(1)
            self.pantalla.GetRenderWindow().SetStereoRender(1)

            if num == 2:
                ##self.render.SetStereoRender(1)
                self.pantalla.GetRenderWindow().SetStereoTypeToAnaglyph()
            if num == 3:
                ##self.render.SetStereoRender(1)
                self.pantalla.GetRenderWindow().SetStereoTypeToRedBlue()
            if num == 4:
                ##self.render.SetStereoRender(1)
                self.pantalla.GetRenderWindow().SetStereoTypeToInterlaced()
            if num == 5:
                ##self.render.SetStereoRender(1)
                self.pantalla.GetRenderWindow().SetStereoTypeToDresden()
        self.pantalla.Initialize()
        self.pantalla.Start()
    def getPosition(self):
        i = 0
        j = 0
        k = 0
            #print "picado"
            #print e
        x,y = self.pantalla.GetEventPosition()
        self.click = (x,y)
        z = 0
        #print "posicion: x: ",x," y:",y
        render = self.pantalla.GetRenderWindow().GetRenderers().GetFirstRenderer()
        render.SetDisplayPoint(x,y,z)
        ##print "COORD1: ", render.GetDisplayPoint()
        self.render.DisplayToWorld()
        ##print "COORD2: ", render.GetWorldPoint()
        (xv,yv,zv,tv) = self.render.GetWorldPoint()
        return (xv,yv,zv)
    
    def getActorByPosition(self,pos):
        ((xv),(yv),(zv)) = pos
        
        actores = self.render.GetActors()
        actores.InitTraversal()
        encontrado = False
        finactor = actores.GetLastActor()
        actor = actores.GetNextActor()
        while actor != actores.GetLastProp():## and self.seleccion == False:
            if actor != None:
                coor1 = actor.GetCenter()
                coor2 = ((xv),(yv),(zv))
                res = sqrt((coor2[0] - coor1[0])**2+ (coor2[1] - coor1[1])**2 + (coor2[2] - coor1[2])**2)
                
                ##print "Coor Raton("+str(xv)+","+str(yv)+","+str(zv)+") / Coord actor ("+str(round(coor1[0],2))+","+str(round(coor1[1],2))+","+str(round(coor1[2],2))+") / Res "+str(res)
                
                if res < 2:
                    return actor
                actor = actores.GetNextActor()
        return None
            
    def setColor(self,color,actor):
        if actor != None:
            actor.GetProperty().SetColor(color)

            
    def picado (self,o, e):
        i = 0
        j = 0
        k = 0
            #print "picado"
            #print e
        x,y = self.pantalla.GetEventPosition()
        self.click = (x,y)
        z = 0
        #print "posicion: x: ",x," y:",y
        render = self.pantalla.GetRenderWindow().GetRenderers().GetFirstRenderer()
        render.SetDisplayPoint(x,y,z)
        ##print "COORD1: ", render.GetDisplayPoint()
        self.render.DisplayToWorld()
        ##print "COORD2: ", render.GetWorldPoint()
        (xv,yv,zv,tv) = self.render.GetWorldPoint()
    
        actores = self.render.GetActors()
        actores.InitTraversal()
        encontrado = False
        finactor = actores.GetLastActor()
        actor = actores.GetNextActor()
        while actor != actores.GetLastProp():## and self.seleccion == False:
            if actor != None:
                #print actor.GetCenter(),
                #print " Vs ",
                #print "(",(xv),",",(yv),",",(zv),")"
                coor1 = actor.GetCenter()
                coor2 = ((xv),(yv),(zv))
                ##print "Color: ",actor.GetProperty()
                if not sqrt((coor2[0] - coor1[0])**2+ (coor2[1] - coor1[1])**2 + (coor2[2] - coor1[2])**2) < 2:
                   ## print "Entra aqui-----------------------------------------------------------------------------"
                    actor.GetProperty().SetColor(0,5,0)
                else:
                    coor_new = (float(round(coor1[0])),float(round(coor1[1])),float(round(coor1[2])))
                    tipo = ""
                    actor.GetProperty().SetColor(3,1,3)

                    '''
                    for lista in self.estructura_cubos.getEstructuras():
                        if lista.getPosicion() == coor_new:
                            tipo = lista.getTipo()
                
                    if tipo == "Stack":
                        actor.GetProperty().SetColor(3,1,3)
                    
                    elif tipo == "Estructura":
                        actor.GetProperty().SetColor(3,3,1)
                    else:
                        actor.GetProperty().SetColor(1,1,1)
                    '''
                actor = actores.GetNextProp()
        #self.pantalla.GetRenderWindow().GetRenderers().SetDisplayPoint((x,y,z))
        #print self.pantalla.GetRenderWindow().GetRenderers().DisplayToWorld()
           ## picker = self.pantalla.GetPicker()
        #print picker.GetPickPosition()
        #print (picker)
    '''
    if self.en_mov == 1:
        print "Estamos aqui __________________--------_______"
        cubo = self.elemento_mover
        print "cubo es ",cubo.getDimensionposicion()
        (i,j,k) = cubo.getDimension()
        cubito = vtk.vtkCubeSource()
        cubito.SetXLength(0.1*i)
        cubito.SetYLength(0.1*j)
        cubito.SetZLength(0.1*k)
        (x,y,z,t) = render.GetWorldPoint()
        print "Las coordenadas son ",(x,y,z)
        cubito.SetCenter((x,y,z))
        planeMapper = vtk.vtkPolyDataMapper()
        planeMapper.SetInputConnection(cubito.GetOutputPort())
        planeActor = (vtk.vtkActor())
        planeActor.SetMapper(planeMapper)
        ##self.ren1.RemoveActor(self.actor_debajo)
        self.actor_debajo = planeActor
        self.ren1.AddActor(self.actor_debajo)

    #if picker.GetViewProp() == None:
    #    self.actor_debajo_sin_sel.GetProperty().SetColor(1,1,1)

        if picker.PickProp(x, y, self.pantalla.GetRenderWindow().GetRenderers().GetFirstRenderer()): #and self.seleccion == False:
        if self.elemento_debajo_sin_sel != None and self.elemento_debajo != self.elemento_debajo_sin_sel:
            tipo = ""
            for lista in self.estructura_cubos.getEstructuras():
                if lista.getPosicion() == self.elemento_debajo_sin_sel:
                    tipo = lista.getTipo()
            if tipo == "Stack":
                self.actor_debajo_sin_sel.GetProperty().SetColor(3,1,3)
            elif tipo == "Estructura":
                self.actor_debajo_sin_sel.GetProperty().SetColor(3,3,1)
            else:
                self.actor_debajo_sin_sel.GetProperty().SetColor(1,1,1)
        #print picker.GetViewProp().GetCenter()
        self.elemento_debajo_sin_sel = picker.GetViewProp().GetCenter()
        self.actor_debajo_sin_sel = picker.GetActor()
        self.elemento_debajo_sin_sel = (float(round(self.elemento_debajo_sin_sel[0])),float(round(self.elemento_debajo_sin_sel[1])),float(round(self.elemento_debajo_sin_sel[2])))
        if self.elemento_debajo != self.elemento_debajo_sin_sel:
            picker.GetViewProp().GetProperty().SetColor(1,3,1)
        if self.seleccion == True and self.elemento_debajo == self.elemento_debajo_sin_sel:
            self.actor_debajo.GetProperty().SetColor(3,1,1)
        ## i, j , k = #volume.GetPoint(volume.FindPoint(picker.GetPickPosition()))

    else:
        if self.seleccion == False and self.elemento_debajo_sin_sel != None:
            tipo = ""
            for lista in self.estructura_cubos.getEstructuras():
                if lista.getPosicion() == self.elemento_debajo_sin_sel:
                    tipo = lista.getTipo()
            if tipo == "Stack":
                self.actor_debajo_sin_sel.GetProperty().SetColor(3,1,3)
            elif tipo == "Estructura":
                self.actor_debajo_sin_sel.GetProperty().SetColor(3,3,1)
            else:
                self.actor_debajo_sin_sel.GetProperty().SetColor(1,1,1)
            self.actor_debajo_sin_sel = None
            self.elemento_debajo_sin_sel = None
    #print "posicion: i: ",i," j:",j," k:",k
    
       #print 'color:', self.pantalla.GetInteractorStyle().GetPickColor()  # rojo
       #print 'selection point:' , picker.GetSelectionPoint()
      #print 'pick position:' , picker.GetPickPosition()
    self.pantalla.Render()
    
    
    
    
    
    
	renWin = vtk.vtkRenderWindow()
	ren = vtk.vtkRenderer()	
	renWin.StereoCapableWindowOn()
	renWin.SetStereoRender(1)
	renWin.SetStereoTypeToCrystalEyes()
	#renWin.AddRenderer(ren1)
	renWin.SetSize(600, 600)
	'''


