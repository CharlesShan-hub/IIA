class Test():
	"""docstring for Test"""
	def __init__(self,**kwg):
		self.real = False
		self.kwg=kwg
		print(kwg['a'])

	def add(self,a,b):
		return a+b

class Child(Test):
	"""docstring for Child"""
	def __init__(self,**kwg):
		super(Child,self).__init__(**kwg)
		print(self.real)
		
test = Child(a=1)
	