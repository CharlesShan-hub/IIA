import pandas as pd
import numpy as np
import datetime

#The Gregorian calendar day
def GregorianCalendarDay():
	data = pd.read_excel('./resources/time/默认时间事件.xlsx',sheet_name='中国阳历节日')

	year = 2022
	month = 1
	day = 1

	for item in np.array(data).tolist():
		if item[2] == 0: # 普通日期
			holiday = datetime.date(year,item[1],item[3])
		else: # 某月第n周形式日期
			week = datetime.date(year, item[1], 1).weekday() + 1
			if week <= item[3]:
				day = (item[3] - week) + 7*(item[2] - 1) + 1
			else:
				day = 7*(item[2] - 1) + item[3] + (7 - week + 1)
			holiday = datetime.date(year,item[1],day)

		print(holiday,item[4])

#GregorianCalendarDay()

#The lunar festival
def LunarFestival():
	data = pd.read_excel('./resources/time/默认时间事件.xlsx',sheet_name='中国阴历节日')
	
	year = 2022
	month = 1
	day = 1

	for item in np.array(data).tolist():
		

LunarFestival()
