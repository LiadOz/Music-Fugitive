from contextlib import contextmanager
from functools import partial, wraps
from collections import defaultdict


def listify(func):
    """
    Used to turn function that takes only one variable to list
    of variables
    """
    @wraps(func)
    def func_wrapper(*args):
        if len(args) == 1:
            return func(*args)
        res = []
        for x in args:
            res.append(func(x))
        return res
    return func_wrapper


def quick_input(func):
    """
    Used to create infinite query from user
    """
    print('To stop input press enter')
    for value in iter(partial(input, 'Enter value: '), ''):
        func(value)


def merge_dicts(f, *args):
    """
    Returns merged dictionary from multiple dictionaries
    according to function f.
    If f is None the last value encountered will be set to the key.
    the first dictionary is changed if it is defaultdict.
    """
    if f is None:
        f = lambda x, y: y
    d = args[0]
    if type(d) is not defaultdict:
        d = defaultdict(int, d)

    for dictionary in args[1:]:
        for k, v in dictionary.items():
            d[k] = f(d[k], v)
    return d
