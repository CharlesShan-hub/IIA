from pandas import read_excel
from pandas import read_csv

def load_excel(path, **kawgs):
	return read_excel(path, **kawgs)

def load_csv(path, **kawgs):
	return read_csv(path, **kawgs)