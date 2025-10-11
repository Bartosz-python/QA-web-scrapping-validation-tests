import validators
from typing import Optional, Any
from playwright.sync_api import ElementHandle

def url_validator(full_url: str) -> Any:
    """Function validating given URL."""
    if validators.url(full_url):
        return full_url
    return False

def is_proper_type(element: str, expected_type: type) -> Any:
    """Checks if an element is proper for the project's data type"""
    if not isinstance(element, expected_type):
        raise Exception("WRONG TYPE OF DATA !!!")
    return element

def is_existing(element: Optional[ElementHandle]) -> str:
    """Return inner text if element exists, else fallback"""
    if not element:
        return "No data available"
    return element.inner_text()

def convert_to_int_if_in_hashmap(element: Any, dictionary: dict) -> Any:
    """For the project's sake this function converts the star rating from the string to int"""
    if element in dictionary:
        element = dictionary[element]
        return element
    return "No such element in the hashmap"