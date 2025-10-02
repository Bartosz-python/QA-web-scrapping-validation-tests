import validators

def url_validator(full_url: str) -> str:
    """Function validating given URL."""
    if validators.url(full_url):
        return full_url
    return False

def is_proper_type(element: str, type: any) -> str:
    """Checks if an element is proper for the project's data type"""
    if not isinstance(element, type):
        raise Exception("WRONG TYPE OF DATA !!!")
    return element

def is_existing(element: str) -> str:
    """Return inner text if element exists, else fallback"""
    if not element:
        return "No data available"
    return element.inner_text()

def convert_if_in_hashmap(element: any, dict: dict) -> any:
    if element in dict:
        element = dict[element]
        return element
    element = "Rating out of bounds"
    return element


