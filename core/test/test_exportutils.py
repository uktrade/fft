from core.exportutils import is_number


def test_is_number_num():
    assert is_number("3") == 3


def test_is_number_float():
    assert is_number("3.1") == 3.1


def test_is_number_string():
    assert is_number("abc") == "abc"


def test_is_number_hex():
    assert is_number("A") == "A"
