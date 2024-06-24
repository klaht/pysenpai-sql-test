import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--fuzz", action="store_true", default=False
    )

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "fuzz: mark test as a fuzz test to be run with --fuzz option."
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--fuzz"):
        # --fuzz given in cli: do not skip slow tests
        return
    skip_fuzz = pytest.mark.skip(reason="need --fuzz option to run")
    for item in items:
        if "fuzz" in item.keywords:
            item.add_marker(skip_fuzz)