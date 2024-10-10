import argparse
import sys

from aococr import parsing
from aococr.parsing import arr_to_str, string_to_list
from aococr.resources import read_resource

_default_on_off = ("#", ".")


def shape(data):
    """Shape method that works with both numpy arrays and lists of lists."""
    height = len(data)
    width = len(data[0])
    assert all(len(row) == width for row in data)

    return height, width


def replace_chars(data, pixel_on_off_values: tuple) -> list:
    replace = dict(zip(pixel_on_off_values, _default_on_off, strict=True))
    res = [[replace[char] for char in row] for row in data]
    return res


class Scanner:
    """Helper class for scanning left to right across some data and recognize any known glyphs"""

    def __init__(self, char_glyph_pairs: list):
        """char_glyph_pairs is a list of (char, glyph) tuples where char is a single character,
        and glyph can be a numpy array or list-of-lists representing a series of ASCII art-like
        glyphs."""

        self.char_glyph_pairs = char_glyph_pairs

    def __call__(self, data) -> str:
        """Scans across input data, noting any matching characters.
        Returns a string representing the matched characters.
        Interprets any index out of bounds as a non-match, so take care to check dimensions."""

        rows, cols = shape(data)

        res = ""
        pos = 0  # The left edge of the sliding window

        # Go over data and check for any matching glyphs
        while pos < cols:
            for char, glyph in self.char_glyph_pairs:
                # It's a match if the glyphs shape fits in the remainder of the data, and all elements match
                height, width = shape(glyph)
                dim_match = height <= rows and pos + width <= cols
                char_match = (data[i][pos+j] == glyph[i][j] for i in range(height) for j in range(width))
                match = dim_match and all(char_match)

                # If it's a match, note the matching character and shift the window by the glyphs width
                if match:
                    res += char
                    pos += width
                    break
                #
            else:
                # If not match, shift the window 1 pixel to the right
                pos += 1
            #
        return res



def aococr(
        data,
        pixel_on_off_values: tuple|None|str = None,
        fontsize: tuple=None
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
            (e.g. integer array) will also be attempted to be interpreted.
    pixel_on_off_values: tuple of the symbols representing pixels being on/off.
        AoC tends to use "#" and "." to represent pixels being on/off, respectively.
        If the input data uses different symbols, the symbols can by passed as a tuple.
        For instance, if using "x" and " " to represent pixels being on and off, passing
        pixel_on_off_values = ("x", " ") then be converted into ("#", ".") before any pattern matching
        is done.
        For the default (None), the characters in the input are checked. If they're "#" and ".", no
        conversion is done. Otherwise, both possible replacements are attempted, and whichever one
        results in more matching characters is retained.
    fontsize (tuple): The size (height x width) in pixels of the ascii art fonts to parse.
        Fonts of sizes (6, 4) and (10, 6) are available.
        If not specified, font size is inferred from the height of the input."""
    
    if isinstance(data, str):
        data = parsing.string_to_list(data)
    
    # Infer fontsize if none is provided
    if fontsize is None:
        fontsize = parsing.infer_fontsize(shape(data))

    # Make a scanner with the relevant font
    char_glyph_pairs = read_resource(fontsize=fontsize)
    scanner = Scanner(char_glyph_pairs=char_glyph_pairs)

    # Determine which, if any, replacements of pixel values to perform
    replacements = ()
    pixel_vals_in_data = {char for row in data for char in row}
    uses_standard_values = pixel_vals_in_data == set(_default_on_off)

    if isinstance(pixel_on_off_values, tuple):
        # If a replacement tuple is specified, use it
        replacements = (pixel_on_off_values,)
    elif pixel_on_off_values is None:
        if uses_standard_values:
            # If the input consists of "#" and ".", use as-is
            pass
        else:
            # Otherwise, try interpreting both as on/off
            vals = tuple(pixel_vals_in_data)
            replacements = (vals, vals[::-1])
    else:
        raise ValueError

    if not replacements:
        res = scanner(data)
    else:
        # use the replacement(s) and keep the longest result
        swaps = (replace_chars(data=data, pixel_on_off_values=r) for r in replacements)
        res = max((scanner(swap) for swap in swaps), key=len)
    
    return res


_cli_description = \
"""Converts Advent of Code ASCII art-like strings into letters.
For example, converts

.##..###...##.
#..#.#..#.#..#
#..#.###..#...
####.#..#.#...
#..#.#..#.#..#
#..#.###...##.

Into "ABC"
"""


def ocr_cli() -> None:
    """CLI version to run ocr on stdin"""
    parser = argparse.ArgumentParser(description=_cli_description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()
    data = sys.stdin.read()
    res = aococr(data=data)
    sys.stdout.write(res)



if __name__ == '__main__':
    pass


def display(m):
    """Prints ASCII art-like glyphs in a way that looks good on the terminal.
    Replaces '.' with empty space " " to make reading easier.
    Works with strings, lists of lists, and numpy arrays."""

    if isinstance(m, str):
        m = string_to_list(m)

    replace = {".": " "}
    s = arr_to_str(m=m, char_replacements=replace)
    print(s)
