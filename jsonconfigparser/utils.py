from jsonpath_rw import parse

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
    '''Accepts a string delimited by commas (`,`) and returns a list.
    Optionally accepts a secondary callable to convert the list values.'''

    if not captured:
        return partial(list_, secondary=secondary)

    captured = [str.strip(v) for v in captured.split(',')]

    if secondary:
        captured = [secondary(v) for v in captured]

    return captured


def dict_(captured=None, secondary=None):
    '''Accepts a string delimited by commas (`,`). Which are then split
    again by colons (`:`).

    Optionally accepts a secondary callable for converting either
    the key or the value. The callable must accept and return both.
    If the conversion fails, it must raise only AttributeError,
        TypeError or ValueError.
    '''

    if not captured:
        return partial(dict_, secondary=secondary)

    captured = [str.strip(p) for p in captured.split(',')]
    captured = [p.split(':') for p in captured]
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
