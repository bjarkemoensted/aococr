from functools import cache

from aococr import config
from aococr.parsing import string_to_list


@cache
def read_resource(fontsize: tuple):
    fn = config.DATA_FILES[fontsize]
    text = fn.read_text(encoding=config.ENCODING)
    parts = text.split("\n\n")
    
    res = []
     
    for part in parts:
        character, glyph = tuple(part.split("\n=\n"))
        glyph_as_list = string_to_list(glyph)
        res.append((character, glyph_as_list))
    
    return res


if __name__ == '__main__':
    for fontsize in config.FONTSIZES:
        print(fontsize)
        res = read_resource(fontsize)
        print(res)
    #
