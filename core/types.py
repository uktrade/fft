from typing import Literal, TypedDict


MonthIndex = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Month = Literal[
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
    "jan",
    "feb",
    "mar",
]
Months = tuple[
    Literal["apr"],
    Literal["may"],
    Literal["jun"],
    Literal["jul"],
    Literal["aug"],
    Literal["sep"],
    Literal["oct"],
    Literal["nov"],
    Literal["dec"],
    Literal["jan"],
    Literal["feb"],
    Literal["mar"],
]


class MonthsDict[T](TypedDict):
    apr: T
    may: T
    jun: T
    jul: T
    aug: T
    sep: T
    oct: T
    nov: T
    dec: T
    jan: T
    feb: T
    mar: T
