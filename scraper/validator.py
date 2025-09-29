import validators

def url_validator(full_url: str) -> str:
    """Function validating given URL."""
    if validators.url(full_url):
        return full_url
    return False
