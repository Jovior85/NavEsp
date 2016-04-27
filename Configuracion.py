from ConfigParser import ConfigParser
import os,sys

class Configuracion:
    def __init__(self):
        self.fichero = os.getcwd()+"/config.ini"
        self.f =None
        if (not os.path.exists(self.fichero)):
            self.f = open(self.fichero,'w+')
            self.config = ConfigParser()
            self.config.add_section("Directories")
            self.config.set("Directories", "stacks_dir", os.getcwd())
            self.config.set("Directories", "saves_dir", os.getcwd())
            self.savefiles = os.getcwd()
            self.stackfiles = os.getcwd()
            #self.config.read(self.fichero)
            self.config.write(self.f)
        else:
            self.config = ConfigParser()
            self.config.read(self.fichero)
	    if (not self.config.has_section("Directories")):
	    	self.config.add_section("Directories")
		self.config.set("Directories", "stacks_dir", os.getcwd())
		self.config.set("Directories", "saves_dir", os.getcwd())
		self.savefiles = os.getcwd()
		self.stackfiles = os.getcwd()
	        self.config.set("Directories", "saves_dir", os.getcwd())
        	self.config.set("Directories", "stacks_dir", os.getcwd())
            	##self.config.write(self.fichero)
	    else:
            	self.savefiles = self.config.get("Directories", "Saves_dir")
	        self.stackfiles = self.config.get("Directories", "Stacks_dir")
    
    
    def getSaveDir(self):
        return self.savefiles
    
    def getStackDir(self):
        return self.stackfiles
    
    def setSaveDir(self,dire):
        self.config.set("Directories", "saves_dir", dire)
        self.savefiles = dire
        if not self.f:
            self.f = open(self.fichero,'w+')
        self.config.write(self.f)
	self.f.close()
	self.f = None
    def setStackDir(self,dire):
        self.config.set("Directories", "stacks_dir", dire)
        self.stackfiles = dire
        if not self.f:
            self.f = open(self.fichero,'w+')
        self.config.write(self.f)
	self.f.close()
	self.f = None
