import pytest
import pytest_html
import xdist
from playwright.sync_api import sync_playwright
from src.validator import *
from tests.conftest import *

@pytest.mark.parametrize("url, expected", url_test_data())
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.validation
def test_url_validator(url: str, expected: any) -> any:
    assert url_validator(url) == expected

@pytest.mark.parametrize("element, type, expected", is_proper_type_data())
@pytest.mark.validation
@pytest.mark.smoke
def test_is_proper_type_valid(element: any, type: any, expected: any) -> any:
    assert is_proper_type(element, type) == expected

@pytest.mark.smoke
@pytest.mark.validation
def test_is_proper_type_invalid() -> any:
    with pytest.raises(Exception) as exc_info:
        is_proper_type("False", bool)

    assert str(exc_info.value) == "WRONG TYPE OF DATA !!!"

@pytest.mark.smoke
@pytest.mark.validation
def test_is_existing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
            
        page.goto("https://example.com")

        element = page.query_selector("h1")
        assert is_existing(element) == "Example Domain"

        element2 = page.query_selector("h2")
        assert is_existing(element2) == "No data available"

@pytest.mark.smoke
def test_convert_to_int_if_in_hashmap_valid():
    hashmap = {
        "test": 0,
        "test1": 1,
        "test2": 2
    }

    test_variable = "test"

    assert convert_to_int_if_in_hashmap(test_variable, hashmap) == 0

@pytest.mark.smoke
def test_convert_to_int_if_in_hashmap_invalid():
    hashmap = {
        "test": 0,
        "test1": 1,
        "test2": 2
    }

    test_variable = "test3"

    assert convert_to_int_if_in_hashmap(test_variable, hashmap) == "No such element in the hashmap"