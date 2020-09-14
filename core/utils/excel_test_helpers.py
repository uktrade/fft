from typing import (
    Dict,
    TypeVar,
)

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class FakeWorkSheet(Dict[_KT, _VT]):
    title = None


class FakeCell:
    value = None

    def __init__(self, value):
        self.value = value
