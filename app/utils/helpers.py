def _pick(d, *keys, default=None):
    """First non-empty value among several possible key names."""
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return default
