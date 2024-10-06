from importlib.metadata import version

__version__ = version("aococr")

from aococr.scanner import Scanner
from aococr.ocr import parse_pixels
