import warehouse

class BirthdayWarehouse(warehouse.Warehouse):
	"""docstring for Warehouse"""
	def __init__(self, **kwg):
		super(BirthdayWarehouse, self).__init__(**kwg)

	def add_people(self,**kwg):
		con = 'INSERT INTO BIRTHDAY (NAME,YEAR,MON,DAY) VALUES ("{}","{}","{}","{}")'.format(kwg['name'],kwg['year'],kwg['mon'],kwg['day'])
		self.operation_base_repo(name="TestRepo1",con=con)

	def get_birthday(self,**kwg):
		con = '''SELECT NAME,YEAR,MON,DAY from BIRTHDAY'''
		print(self.operation_base_repo(name="TestRepo1",con=con))