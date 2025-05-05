import logger
import warehouse

LOG_MODULE = 'Mapping'

def test_get(name=None):
    name='MySheetWarehouse'
    return warehouse._test_show_info(name,con = '''SELECT NUM1,NUM2 from DataSet1''')