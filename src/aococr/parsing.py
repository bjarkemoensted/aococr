def string_to_list(data: str) -> list:
    cleaned = data.strip()
    res = [list(line) for line in cleaned.splitlines()]
    return res


def arr_to_str(m, char_replacements: dict=None) -> str:
    """Converts array to a string, with rows separated by newlines.
    Takes an optional dict for replacement characters."""

    if char_replacements is None:
        char_replacements = dict()

    lines = [''.join([char_replacements.get(char, char) for char in line]) for line in m]
    res = "\n".join(lines)
    return res


def display(m):
    """Prints an array of characters in a way that looks good on the terminal.
    Replaces '.' with empty space " " to make reading easier."""

    replace = {".": " "}
    s = arr_to_str(m=m, char_replacements=replace)
    print(s)
