import numpy as np
import pytest

from aococr import config
from aococr.parsing import arr_to_str
from aococr.resources import read_resource


n_samples = 100
rs = np.random.RandomState(seed=42)


@pytest.fixture
def glyphdict():
    res = dict()
    for fontsize in config.FONTSIZES:
        res[fontsize] = read_resource(fontsize)
    
    return res


@pytest.fixture
def glyphdict_np(glyphdict):
    res = {k: [(char, np.array(glyph)) for char, glyph in v] for k, v in glyphdict.items()}
    return res


def make_random_ascii_with_solution(char_glyph_pairs):
    inds = rs.choice(a=list(range(len(char_glyph_pairs))), size=10, replace=True)
    
    couples = (char_glyph_pairs[i] for i in inds)

    chars, glyphs = zip(*couples)
    solution = "".join(chars)
    ascii_ = np.hstack(glyphs)
    return solution, ascii_


@pytest.fixture
def example_code_ascii_pairs(glyphdict_np):
    res = [make_random_ascii_with_solution(data) for data in glyphdict_np.values() for _ in range(n_samples)]
    return res


@pytest.fixture
def example_codes(example_code_ascii_pairs):
    return [tup[0] for tup in example_code_ascii_pairs]


@pytest.fixture
def example_ascii_numpy(example_code_ascii_pairs):
    return [tup[1] for tup in example_code_ascii_pairs]


@pytest.fixture
def example_ascii_list(example_ascii_numpy):
    return [m.tolist() for m in example_ascii_numpy]


@pytest.fixture
def example_ascii_list(example_ascii_numpy):
    return [m.tolist() for m in example_ascii_numpy]


@pytest.fixture
def example_ascii_str(example_ascii_numpy):
    return [arr_to_str(m) for m in example_ascii_numpy]


_chars = "';lsdfjbasvkegad[okd#$@#$23514#]."


@pytest.fixture
def example_ascii_str_swapped(example_ascii_str):
    vals = list(set(_chars))
    res = []
    for s in example_ascii_str:
        replace = dict(zip(["#", "."], rs.choice(vals, size=2, replace=False)))
        res.append(''.join(replace.get(c, c) for c in s))
    return res


if __name__ == '__main__':
    stuff = read_resource((6, 4))
    
    for k, v in stuff:
        m = np.array(v)
    
    print(np.hstack([m, m]))