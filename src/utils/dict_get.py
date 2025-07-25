def dict_get(d, keys, default=""):

    current = d
    for key in keys:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default
    return current
