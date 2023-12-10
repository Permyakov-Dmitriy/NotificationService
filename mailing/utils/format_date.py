import re


def string_to_arrays_int(string):
    '''Преобразовние в кортеж списков даты - время и временного пояса'''
    res = list(map(int, re.split(r"[^0-9]", string)))

    return res[:-2], res[-2:]