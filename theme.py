def _getValue(map, key, fallbackMap):
    try:
        return map[key]
    except KeyError:
        return fallbackMap[key]


_Default = {
    "Background": "#f9fedc",
    "AltBackground": "#fcc8ff",
}


class __colorTheme:
    def __init__(self, **kw):
        fallback = _getValue(kw, "fallback", {"fallback": _Default})
        self.Background = _getValue(kw, "Background", fallback)
        self.AltBackground = _getValue(kw, "AltBackground", fallback)


Default = __colorTheme(**_Default)
