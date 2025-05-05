from datetime import datetime, date, timedelta
import calendar
from lunardate import LunarDate
import json
from abc import ABC, abstractmethod
from typing import Union

class Holiday(ABC):
    """
    Abstract base class for defining holidays.

    Attributes:
    - **kwargs: Arbitrary keyword arguments to set as attributes.

    Methods:
    - calculate(year): Abstract method to calculate the holiday date for a given year.
    - to_lunar(solar_date): Static method to convert a solar date to a lunar date.
    - to_solar(year, month, day): Static method to convert a lunar date to a solar date.
    """

    def __init__(self, **kwargs):
        """
        Initialize the holiday with arbitrary keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.date = {}

    def _has_attr(self,attr_name_list):
        for attr_name in attr_name_list:
            assert hasattr(self, attr_name)

    @abstractmethod
    def calculate(self, year) -> Union[None, date]:
        """
        Abstract method to calculate the holiday date for a given year.

        Args:
        - year: The year for which to calculate the holiday date.

        Returns:
        - Union[None, date]: The holiday date, or None if the holiday does not occur in the given year.
        """
        pass

    @staticmethod
    def to_lunar(solar_date) -> LunarDate:
        """
        Convert a solar date to a lunar date.

        Args:
        - solar_date: The solar date to convert.

        Returns:
        - LunarDate: The corresponding lunar date.
        """
        return LunarDate.fromSolarDate(solar_date.year, solar_date.month, solar_date.day)

    @staticmethod
    def to_solar(year, month, day) -> date:
        """
        Convert a lunar date to a solar date.

        Args:
        - year: The lunar year.
        - month: The lunar month.
        - day: The lunar day.

        Returns:
        - date: The corresponding solar date.
        """
        return LunarDate(year, month, day).toSolarDate()

    def to_json(self):
        """
        Serialize the object's attributes to a dictionary.
        """
        obj_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):  # 忽略私有属性
                obj_dict[key] = value
        print(obj_dict)
        return obj_dict

class FixHoliday(Holiday):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._has_attr(["month", "day", "lunar"])

    def calculate(self, year):
        if self.lunar == True: # type: ignore
            self.date[year] = self.to_solar(year,self.month,self.day) # type: ignore
        else:
            self.date[year] =  datetime(year, self.month, self.day) # type: ignore
        return self.date[year]

class SolarTermsHoliday(Holiday):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calculate(self, year):
        # https://wenku.baidu.com/view/7b9cd48283d049649b665891.html?fr=aladdin664466&ind=1&aigcsid=0&qtype=0&lcid=1&queryKey=%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E8%AE%A1%E7%AE%97%E6%96%B9%E6%B3%95&_wkts_=1714704957026&bdQuery=%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E8%AE%A1%E7%AE%97%E6%96%B9%E6%B3%95
        D = 0.2422
        C = {
            "立春": 3.87, "雨水": 18.74,"惊蛰": 5.63, "春分": 20.646,
            "清明": 4.81, "谷雨": 20.1,"立夏": 5.52, "小满": 21.04,
            "芒种": 5.678, "夏至": 21.37,"小暑": 7.108, "大暑": 22.83,
            "立秋": 7.5, "处暑": 23.13,"白露": 7.646, "秋分": 23.042,
            "寒露": 8.318, "霜降": 23.438,"立冬": 7.438, "小雪": 22.36,
            "大雪": 7.18, "冬至": 21.94,"小寒": 5.4055, "大寒": 20.12
        }
        M = {
            "立春": 2, "雨水": 2,"惊蛰": 3, "春分": 3,
            "清明": 4, "谷雨": 4,"立夏": 5, "小满": 5,
            "芒种": 6, "夏至": 6,"小暑": 7, "大暑": 7,
            "立秋": 8, "处暑": 8,"白露": 9, "秋分": 9,
            "寒露":10, "霜降":10,"立冬":11, "小雪":11,
            "大雪":12, "冬至":12,"小寒": 1, "大寒": 1
        }

        Y = int(str(year)[2:])  # 年代数的后2位
        L = (year - 2000 - 1) // 4  # 闰年数

        # 计算节气的日期
        base_date = datetime(year, 1, 6)  # 将"小寒"作为基准日期
        day = int((Y * D + C[self.solar_term] - L))
        month = M[self.solar_term]

        self.date[year] = datetime(year, month, day)
        return self.date[year]

class WeekInMonthHoliday(Holiday):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weekday = self.weekday - 1

    def calculate(self, year):
        # 获取该月份的第一天
        first_day = datetime(year, self.month, 1)
        # 获取该月份的第一天是星期几
        first_weekday = first_day.weekday()
        # 计算第一个星期 self.weekday 的日期
        if first_weekday <= self.weekday:
            offset = self.weekday - first_weekday
        else:
            offset = 7 - (first_weekday - self.weekday)
        first_weekday_date = first_day + timedelta(days=offset)

        # 生成该月份所有星期 self.weekday 的日期列表
        weekday_dates = [first_weekday_date + timedelta(weeks=i) for i in range(5)]

        # 获取第 week_num 个星期 self.weekday 的日期
        if self.week_num < 0:
            holiday_date = weekday_dates[self.week_num]  # 负数索引倒数
        elif self.week_num <= len(weekday_dates):
            holiday_date = weekday_dates[self.week_num - 1]
        else:
            raise ValueError(f"Invalid week_num {self.week_num} for month {self.month}")

        self.date[year] = holiday_date.date()
        return self.date[year]

class LastInMonthHoliday(Holiday):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last = self.last-1

    def calculate(self, year):
        # 获取该月份的最后一天日期
        last_day = calendar.monthrange(year, self.month)[1]
        holiday_day = last_day - self.last

        self.date[year] = datetime(year, self.month, holiday_day).date()
        return self.date[year]

class HolidayArray(list):
    def __init__(self, base_path="./iia/plugins/holidays"):
        super().__init__()
        self.base_path = base_path

    def load(self, file, base_path=None):
        base_path = base_path or self.base_path
        try:
            full_path = f"{base_path}/{file}.json"
            with open(full_path, 'r') as file:
                holidays = json.load(file)
                for key,value in holidays.items():
                    if value["load"] == False:
                        continue
                    if value["type"] in globals():
                        holiday_class = globals()[value["type"]]
                        self.append(holiday_class(path=full_path,**value['params']))
            return True
        except FileNotFoundError:
            print(f"File {file}.json not found.")
            return False

    def calculate(self,year):
        for i in self:
            i.calculate(year)

    def to_json(self):
        temp = []
        for i in self:
            temp.append(i.to_json())
        return temp
