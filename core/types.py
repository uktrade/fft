from typing import Literal, TypedDict


FinancialPeriods = tuple[
    Literal[1],
    Literal[2],
    Literal[3],
    Literal[4],
    Literal[5],
    Literal[6],
    Literal[7],
    Literal[8],
    Literal[9],
    Literal[10],
    Literal[11],
    Literal[12],
]

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
