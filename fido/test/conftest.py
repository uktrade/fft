# Used to detect if running from within a pytest run
# https://docs.pytest.org/en/latest/example/simple.html
# required because save in the meta model logchange (in core), save the changes to the log table, with the userid
# but the userid is not valid when we are running from test...


def pytest_configure(config):
    import core
    print('In pytest_configure')
    core._called_from_test = True


def pytest_unconfigure(config):
    import core
    print('In pytest_unconfigure')
    del core._called_from_test
