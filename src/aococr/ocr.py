from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

try:
    import numpy as np
    _has_numpy = True
except ImportError:
    _has_numpy = False

from aococr import config
from aococr.parsing import string_to_list
from aococr.resources import read_resource
from aococr.scanner import Scanner  # TODO numpy version

_default_on_off = ("#", ".")


def _pixel_vals_by_frequency(data) -> tuple:
    """Attempts to infer which pixel values mean on/off in the input.
    It is assumed that the most common character means off,
    and the remaining character means on.
    An error is raised if the input does not contain exactly 2 distinct values."""
    
    if isinstance(data, str):
        data = string_to_list(data)

    counts = Counter(val for row in data for val in row)
    observed = sorted(counts.keys(), key=lambda val: counts[val])
    return tuple(observed)


def infer_fontsize(shape):
    height, width = shape
    for fontsize in config.FONTSIZES:
        font_height, _ = fontsize
        if height == font_height:
            return fontsize
        #
    raise ValueError(f"Could not infer an available font size for input shape ({height}x{width}).")


def ocr(
        data: str|list|np.ndarray,
        pixel_on_off_values: tuple|None|str = None,
        glyph_dimensions_pixels: tuple=None
    ) -> str:
    """Parses the ASCII art representations of letters sometimes encountered in Advent of Code (AoC).
    Whereas most problems have solutions which produce interger outputs, a few output stuff like:

    .##..###...##.
    #..#.#..#.#..#
    #..#.###..#...
    ####.#..#.#...
    #..#.#..#.#..#
    #..#.###...##.

    A human can easily parse the above into "ABC", but it's nice to be able to do programatically.

    This function can parse ascii art-like data like the above into a string.

    data: The ascii art-like data to be parsed. Multiple formats can be used:
        string: Plaintext, with newlines characters separating the lines.
        list of lists, with each element of the inner list being a single character.
        numpy array: 2D string array where each element is a single character. Other values
            (e.g. integer array) will also be attempted interpreted.
    pixel_on: AoC tends to use "#" and "." to represent pixels being on/off, respectively.
        If the input uses different symbols, pixel_on will be interpreted as the pixel being on,
        and converted to "#" when matched against known glyphs. As the data may only contain 2
        distinct pixel values, the remaining value is assumed to mean off.
        If no argument is provided, the values are inferred from the data.
        An error is thrown if the data do not contain exactly 2 distinct pixel values.
    glyph_dimension_pixels (tuple): AoC has featured ascii art stuff with various font sizes.
        A specific font size can be specified here in a (height_in_pixels, width_in_pixels) format.
        The supported values are (6, 4), and (10, 6) - the only ones occurring to my knowledge.
        If not provided, the size is inferred from the data, going by the height, assuming a single
        line of characters in the input."""
    
    # Turn into standard format

    if pixel_on_off_values == "auto":
        observed_vals = _pixel_vals_by_frequency(data=data)
        reverse = observed_vals[::-1]
        brute = (
            ocr(
                data=data,
                pixel_on_off_values=tup,
                glyph_dimensions_pixels=glyph_dimensions_pixels
            )
            for tup in (observed_vals, reverse)
        )

        best = max(brute, key=len)
        return best

    replacements = None


    if pixel_on_off_values is None:
        pass
    else:
        replacements = dict(zip(pixel_on_off_values, _default_on_off, strict=True))
    
    
    scanner = Scanner(data=data, replacements=replacements)

    # Load the characters and ascii art glyphs
    fontsize = infer_fontsize(scanner.data_shape())
    char_glyphs_pairs = read_resource(fontsize=fontsize)

    res = ""

    # Scan left to right across the input, looking for matching ASCII art-like glyphs
    while not scanner.done():
        # Check for matches at the current location
        for char, glyph in char_glyphs_pairs:
            if scanner.match(glyph, skip_ahead_on_match=True):
                res += char
                break
            #
        else:
            # If no glyphs match, skip ahead to the next line
            scanner.skip_ahead()
    
    return res


_ex = """
$$$$$ff$f$$$$$$$$$$f$$$ff$$$ff$$ff$$ff$
$fff$f$f$ffffff$$ff$f$ffff$$ff$$ff$$ff$
$$$f$$ff$fffff$f$ff$f$ffff$$ff$$ff$$$$$
$fff$f$ff$$ff$ff$$$ff$ffff$$ff$$ff$$ff$
$fff$f$ffff$$fff$ffff$f$ff$$ff$$ff$$ff$
$$$$$ff$$$$f$$$$$fff$$$f$$ff$$ff$$f$ff$
"""

if __name__ == '__main__':
    code = ocr(_ex, pixel_on_off_values="auto")
    print(code)
