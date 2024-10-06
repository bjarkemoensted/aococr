import copy

from aococr.parsing import string_to_list


class Scanner:
    """Helper class for scanning across a 2D array to make pattern matching easier.
    Works by sliding a window spanning all rows across the array.
    Maintains the index of the left edge of the window, and exposes functionality to
    move the index forward, and grab the subarray corresponding to windows of a given pixel width
    starting at the index."""

    _data_type = list

    def __init__(self, data: str|list, replacements: dict=None):
        """data: numpy string array with values "#" (on) and "." (off).
        spacing: Assumed spacing between characters. Defaults to 0."""

        self.m = self.standardize_data(data)
        if replacements:
            self.replace_characters(replacements)
        _, self.edge = self.shape(self.m)
        self.ind = 0
    
    @classmethod
    def shape(cls, m):
        height = len(m)
        width = len(m[0])
        return height, width
    
    def replace_characters(self, replacements: dict):
        self.m = copy.deepcopy(self.m)
        rows, cols = self.data_shape()
        for i in range(rows):
            for j in range(cols):
                val = self.m[i][j]
                self.m[i][j] = replacements[val]

    def data_shape(self):
        return self.shape(self.m)
    
    @classmethod
    def standardize_data(cls, data):
        if isinstance(data, str):
            return string_to_list(data)
        elif isinstance(data, list):
            return data
        else:
            raise TypeError(f"Unsupported data type: {type(data)}.")
        #

    def skip_ahead(self, n_pixels=1):
        """Skips n pixels ahead towards the right"""
        self.ind += n_pixels

    def get_slice(self, left: int, right: int):
        res = [line[left: right] for line in self.m]
        return res

    def peek(self, window_width: int):
        """Returns an array corresponding to a windows n pixels wide, starting from the index.
        Does not alter the current index."""
        
        left = self.ind
        right = self.ind + window_width
        
        # Throw an error if the right edge falls off
        if right > self.edge:
            raise IndexError(f"Window right edge at {right} falls off (array width: {self.edge})")
        
        res = self.get_slice(left=left, right=right)
        return res
    
    def pop(self, window_width: int):
        """Returns contents of a window n pixels wide starting from index.
        Moves index a corresponding distance forward."""

        res = self.peek(window_width=window_width)
        self.skip_ahead(window_width)
        return res
    
    @classmethod
    def _equal(cls, a, b):
        if cls.shape(a) != cls.shape(b):
            return False
        
        rows, cols = cls.shape(a)
        return all(a[i][j] == b[i][j] for i in range(rows) for j in range(cols))

    def match(self, target, skip_ahead_on_match=True) -> bool:
        """Accepts a target and returns a bool indicating whether a window starting at
        the scanner's current index matches the input.
        If skip_ahead_on_match (default: True), the index is moved forward by the window width."""

        assert isinstance(target, self._data_type)
        _, window_width = self.shape(target)

        try:
            snippet = self.peek(window_width)
            # Explicitly check that the dimensions match as well
            shape_matches = self.shape(target) == self.shape(snippet)
            is_match = shape_matches and self._equal(target, snippet)
        except IndexError:
            is_match = False
        
        if is_match and skip_ahead_on_match:
            self.pop(window_width)

        return is_match
    
    def done(self) -> bool:
        """Bool indicating whether the scanner has any data left."""
        res = self.ind >= self.edge
        return res
    #


if __name__ == '__main__':
    pass
