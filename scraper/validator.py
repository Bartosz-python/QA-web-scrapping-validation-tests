import validators

def url_validator(full_url) -> str:
    if validators.url(full_url):
        return full_url
    return "Issues with URL!"
