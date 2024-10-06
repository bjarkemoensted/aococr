from aococr.ocr import parse_pixels
from aococr.parsing import string_to_list


def test_meh(glyphdict):
    assert isinstance(glyphdict, dict)


def test_ocr_string_input(example_codes, example_ascii_str):
    for code, data in zip(example_codes, example_ascii_str):
        output = parse_pixels(data)
        assert code == output
    #


def test_ocr_list_input(example_codes, example_ascii_list):
    for code, data in zip(example_codes, example_ascii_list):
        output = parse_pixels(data)
        assert code == output
    #


def test_robust_to_char_swap(example_codes, example_ascii_numpy):    
    for code, data in zip(example_codes, example_ascii_numpy):
        output = parse_pixels(data)
        assert code == output
    #


def test_robust_to_char_swap(example_ascii_str, example_ascii_str_swapped):    
    for data, swapped in zip(example_ascii_str, example_ascii_str_swapped):
        a = parse_pixels(data)
        b = parse_pixels(swapped, pixel_on_off_values="auto")
        good = a == b
        assert good
    #


def test_swap_list(example_ascii_list, example_ascii_str_swapped):    
    for data, swapped in zip(example_ascii_list, example_ascii_str_swapped):
        a = parse_pixels(data)
        list_ = string_to_list(swapped)
        b = parse_pixels(list_, pixel_on_off_values="auto")
        good = a == b
        assert good
    #
