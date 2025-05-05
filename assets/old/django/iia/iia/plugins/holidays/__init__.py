APP_NAME = '节日'   # 这个是插件的名字
PATH_NAME = 'holidays'  # 这个是文件夹的名字

from iia.storage import Storage
from iia.plugins.holidays.holidays import HolidayArray

holidays = HolidayArray() # 所有的节日
# holidays.load("test")
holidays.load("lunar")
holidays.load("twenty_four_solar_terms")
holidays.load("world")
# holidays.calculate(2024)

def test_function():
    print("In!!!!!")
    return 100

def get_year(year):
    year = int(year[0])
    holidays.calculate(year)
    return holidays.to_json()
# storage = Storage()
# storage.create_table('users', {
#     'id': 'INTEGER PRIMARY KEY',
#     'name': 'TEXT',
#     'age': 'INTEGER'})

# print(globals())
