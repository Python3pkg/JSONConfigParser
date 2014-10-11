import shlex

from inspect import getfullspec

from jsonpath_rw import parse

__registry = {}

def command(f):
    '''Stores a function and the names of its arguments in a registry global.
    Returns the function unchanged to the namespace.
    '''
    __registry[f.__name__] = tuple([f, *getfullargspec(f).args])
    return f

def call(fname, json, source):
    '''Looks up a function by its name in the registry global and
    extracts the correct agruments from a source (such as an argparse result)
    and calls the function with the json and other arguments.
    '''
    f, **kwargs = _registry.get(fname)
    kwargs = {n:getattr(source, n) for n in kwargs if n != 'json'}
    f(json=json, **kwargs)

def convert_input(msg, converter=str):
    '''A helper to provide typed input.

    :param converter: A callable to convert the input
        If converter fails, it must raise ValueError, 
        TypeError or AttributeError
    :param msg str: A message to the user to display.

    '''
    msg = "{}: ".format(msg)

    while True:
        captured = input(msg)

        try:
            captured = converter(captured)
        except (AttributeError, TypeError, ValueError) as e:
            print(e)
        else:
            return captured

def list_(captured=None, secondary=None):
    '''Accepts a space separated string and returns a list of values.
    Optionally accepts a secondary callable to convert the list values.'''

    if not captured:
        return partial(list_, secondary=secondary)

    captured = shlex.split(captured)

    if secondary:
        captured = [secondary(v) for v in captured]

    return captured


def dict_(captured=None, secondary=None):
    '''Accepts a space delimited string and breaks them into k=v pairs.

        ```
        dict_(":q

        ```

    Optionally accepts a secondary callable for converting either
    the key or the value. The callable must accept and return both.
    If the conversion fails, it must raise only AttributeError,
        TypeError or ValueError.
    '''

    if not captured:
        return partial(dict_, secondary=secondary)

    captured = 

    if secondary:
        captured = [secondary(k,v) for k,v in captured]

    return dict(captured)

fieldtypes = {
    'str'   : str,
    'int'   : int,
    'list'  : list_,
    'dict'  : dict_,
    'float' : float,
    }
