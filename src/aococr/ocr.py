from aococr import config
from aococr.parsing import string_to_list
from aococr.resources import read_resource
from aococr.scanner import Scanner

_default_on_off = ("#", ".")


def _pixel_vals_by_frequency(data) -> tuple:
    """Returns a tuple of the unique pixel values contained in the input."""
    
    if isinstance(data, str):
        data = string_to_list(data)

    unique = {val for row in data for val in row}
    res = tuple(sorted(unique))
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


def parse_pixels(
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
        If the input uses different symbols, the symbols can by passed as a tuple.
        For instance, if using "x" and " " to represent pixels being on and off, passing
        pixel_on_off_values = ("x", " ") then be converted into ("#", ".") before any pattern matching
        is done.
        pixel_on_off_values = "auto" can be used to attempt to infer the values automatically.
    fontsize (tuple): The size (height x width) in pixels of the ascii art fonts to parse.
        Fonts of sizes (6, 4) and (10, 6) are available.
        If not specified, font size is inferred from the height of the input."""
    
    # If inferring the pixel on/off values, try both possible interpretations
    if pixel_on_off_values == "auto":

        observed_vals = _pixel_vals_by_frequency(data=data)
        reverse = observed_vals[::-1]
        
        # Assume the result with the greatest length corresponds to the correct on/off vals
        brute = (
            parse_pixels(
                data=data,
                pixel_on_off_values=tup,
                fontsize=fontsize
            )
            for tup in (observed_vals, reverse)
        )

        best = max(brute, key=len)
        return best


    if pixel_on_off_values is None:
        replacements = None
    else:
        replacements = dict(zip(pixel_on_off_values, _default_on_off, strict=True))
    
    # Make a scanner instance to scan across input
    scanner = Scanner(data=data, replacements=replacements)

    # If fontsize isn't specified, infer from data. Getting shape from the scanner after it has handled type conversion
    if fontsize is None:
        fontsize = infer_fontsize(scanner.data_shape())
    
    # Read in the known ASCII art glyphs and the characters they represent
    char_glyphs_pairs = read_resource(fontsize=fontsize)

    # Scan across data, keeping any characters with matched glyphs
    res = ""

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


if __name__ == '__main__':
    pass
