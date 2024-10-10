# **aococr** - Advent of Code ASCII-art character recognition
OCR tool in python for Advent of Code (AoC) ASCII art.

Som AoC puzzles produce a result which uses values '#', and '.' to mimic pixels turned on/off in a display, like below:

    .##..###...##.
    #..#.#..#.#..#
    #..#.###..#...
    ####.#..#.#...
    #..#.#..#.#..#
    #..#.###...##.

Converting the above string into the string 'ABC' is a task which, unaccaptably, requires a human to think and type for a few seconds.

This package exposes functionality to automatically parse ASCII art-like displays like the above into strings. It can be called in two ways in python, via the `aococr` method, or via the `aoc-ocr` command-line tool.

Variations like fontsize of the ASCII glyphs and handling other characters than "#" / "." Should™ be handled automatically. If not, see the `aococr` docstring.

## Installation
`pip install aococr`

## In python:

```python
from aococr import aococr

display_string = """
.##..###...##.
#..#.#..#.#..#
#..#.###..#...
####.#..#.#...
#..#.#..#.#..#
#..#.###...##.
"""

s = aococr(display_string)
print(s)  # prints "ABC"
```

The `aococr` method accepts several data types:
* list of lists of characters
* strings, which are stripped of trailing/leading whitespace and converted into lists of lists
* numpy-arrays (though numpy is not a dependency)

## From command line
```bash
aoc-ocr < some_file.txt
```

## Credit
The ASCII-glyphs come from mstksg's [advent-of-code-ocr
](https://github.com/mstksg/advent-of-code-ocr/) Haskell library, which [lists contributions](https://github.com/mstksg/advent-of-code-ocr/?tab=readme-ov-file#credit) to collecting the fonts to Reddit users 
 u/usbpc102,
u/TheShallowOne,
and @gilgamec.
