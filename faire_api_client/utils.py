def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    https://stackoverflow.com/a/11326230
    """
    return "/".join(map(lambda x: str(x).strip('/').rstrip('/'), args))