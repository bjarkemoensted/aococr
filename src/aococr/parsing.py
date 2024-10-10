from aococr import config


def string_to_list(data: str) -> list:
    cleaned = data.strip()
    res = [list(line) for line in cleaned.splitlines()]
    return res


def arr_to_str(m, char_replacements: dict=None) -> str:
    """Converts array to a string, with rows separated by newlines.
    Takes an optional dict for replacement characters."""

    if char_replacements is None:
        char_replacements = dict()

    lines = [''.join([char_replacements.get(char, char) for char in line]) for line in m]
    res = "\n".join(lines)
    return res


def infer_fontsize(shape: tuple) -> tuple:
    """Attempts to infer fontsize from the shape of an input.
    This just assumes that input is a single line of ASCII art, so just goes by height,
    i.e. inputs with height 10 return (10, 6) and height 6 (6, 4)"""

    height, width = shape
    for fontsize in config.FONTSIZES:
        font_height, _ = fontsize
        if height == font_height:
            return fontsize
        #

    raise ValueError(f"Could not infer an available font size for input shape ({height}x{width}).")
