class Father(object):
	"""docstring for Father"""
	def __init__(self, arg):
		self.arg = arg
		self.tag = 0

class Children1(Father):
	def __init__(self,arg):
		self.arg = arg
		self.tag = 1

class Children2(Father):
	def __init__(self,arg):
		self.arg = arg
		self.tag = 2

object1 = Father(0)
object2 = Children1(1)
object3 = Children2(2)
print(object1.tag,object2.tag,object3.tag)
print(type(object1),type(object2),type(object3))