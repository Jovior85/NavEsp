class ErrorNav:
	def __init__(self,value):
		self.type = value
	def __str__(self):
		if (self.type=="OutDim"):
			return "Posicion del objeto fuera de rango"
		elif (self.type == "NoTag"):
			return "Estructura sin tag"
		elif (self.type == "NoPos"):
			return "Estructura sin posicion"