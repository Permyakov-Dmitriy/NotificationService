import re


def string_to_arrays_int(string):
    res = list(map(int, re.split(r"[^0-9]", string)))

    return res[:-2], res[-2:]