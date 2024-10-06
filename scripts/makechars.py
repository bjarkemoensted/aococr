from collections import defaultdict
import pathlib

from aococr import config

# Letter maps from: https://github.com/mstksg/advent-of-code-ocr/blob/main/src/Advent/OCR/LetterMap.hs


#######################################################################################################################
##                                        Small (6x4 pixel) font                                                     ##
#######################################################################################################################

smol_chars = "ABCEFGHIJKLOPRSUYZ"
smol_widths = defaultdict(lambda: 4, {"I": 3, "Y": 5})

smol = """
.##..###...##..####.####..##..#..#.###...##.#..#.#.....##..###..###...###.#..#.#...#.####
#..#.#..#.#..#.#....#....#..#.#..#..#.....#.#.#..#....#..#.#..#.#..#.#....#..#.#...#....#
#..#.###..#....###..###..#....####..#.....#.##...#....#..#.#..#.#..#.#....#..#..#.#....#.
####.#..#.#....#....#....#.##.#..#..#.....#.#.#..#....#..#.###..###...##..#..#...#....#..
#..#.#..#.#..#.#....#....#..#.#..#..#..#..#.#.#..#....#..#.#....#.#.....#.#..#...#...#...
#..#.###...##..####.#.....###.#..#.###..##..#..#.####..##..#....#..#.###...##....#...####
"""

#######################################################################################################################
##                                       Larger (10x6 pixel) font                                                    ##
#######################################################################################################################

lorge_chars = "ABCEFGHJKLNPRXZ"
lorge_widths = defaultdict(lambda: 6)

lorge = """
..##...#####...####..######.######..####..#....#....###.#....#.#......#....#.#####..#####..#....#.######
.#..#..#....#.#....#.#......#......#....#.#....#.....#..#...#..#......##...#.#....#.#....#.#....#......#
#....#.#....#.#......#......#......#......#....#.....#..#..#...#......##...#.#....#.#....#..#..#.......#
#....#.#....#.#......#......#......#......#....#.....#..#.#....#......#.#..#.#....#.#....#..#..#......#.
#....#.#####..#......#####..#####..#......######.....#..##.....#......#.#..#.#####..#####....##......#..
######.#....#.#......#......#......#..###.#....#.....#..##.....#......#..#.#.#......#..#.....##.....#...
#....#.#....#.#......#......#......#....#.#....#.....#..#.#....#......#..#.#.#......#...#...#..#...#....
#....#.#....#.#......#......#......#....#.#....#.#...#..#..#...#......#...##.#......#...#...#..#..#.....
#....#.#....#.#....#.#......#......#...##.#....#.#...#..#...#..#......#...##.#......#....#.#....#.#.....
#....#.#####...####..######.#.......###.#.#....#..###...#....#.######.#....#.#......#....#.#....#.######
"""


fontkwargs = {
    (6, 4): dict(characters=smol_chars, widths=smol_widths, ascii_glyphs=smol),
    (10, 6): dict(characters=lorge_chars, widths=lorge_widths, ascii_glyphs=lorge)
}


def break_letters(characters, widths: dict, ascii_glyphs: str):
    """Iterates over character, ascii art representation"""
    ind = 0

    lines = ascii_glyphs.strip().splitlines()
    for char in characters:
        width = widths[char]
        symbol = "\n".join([line[ind:ind+width] for line in lines])
        ind += (width + 1)
        yield char, symbol
    #


def format_rep(fontsize):
    kwargs = fontkwargs[fontsize]
    
    char_glyph_separator = "="
    part_separator = "\n\n"

    parts = []
    for char, symbol in break_letters(**kwargs):
        partlines = [char, char_glyph_separator, symbol]
        part = "\n".join(partlines)
        parts.append(part)
    
    res = part_separator.join(parts)
    
    return res


def preprocess():
    for fontsize, outfile in config.DATA_FILES.items():
        s = format_rep(fontsize)
        outfile.parent.mkdir(parents=True, exist_ok=True)
        outfile.write_text(s, encoding=config.ENCODING)
        print(f"Wrote fontsize {fontsize} to {outfile}")
        

if __name__ == '__main__':
    preprocess()
