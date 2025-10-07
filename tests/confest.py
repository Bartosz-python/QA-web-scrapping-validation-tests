import pytest
from playwright.sync_api import sync_playwright

def url_test_data() -> list:
    return [
    ("https://wikipedia.pl", "https://wikipedia.pl"),
    ("https:/onet", False),
    ("asd://wp.pl", False),
    ("http://Onet.pl", "http://Onet.pl")
]

def is_proper_type_data() -> list:
    return [
    ("string", str, "string"),
    (4, int, 4),
    (True, bool, True),
]