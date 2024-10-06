import pathlib

_here = pathlib.Path(__file__).parent.resolve()

FONTSIZES = (
    (6, 4),
    (10, 6)
)

def _make_filename(fontsize):
    height, width = fontsize
    fn = f"fontsize_{height}x{width}.txt"
    return fn

DATA_DIR = (_here / "data").resolve()
DATA_FILES = {fontsize: DATA_DIR / _make_filename(fontsize) for fontsize in FONTSIZES}
ENCODING = "utf-8"
