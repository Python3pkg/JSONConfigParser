import shlex

from functools import partial
from inspect import getfullargspec
from operator import setitem

from jsonpath_rw import parse, Root

__registry = {}

root = str(Root())

def command(f):
    '''Stores a function and the names of its arguments in a registry global.
    The function name has underscores stripped out.

    Returns the function unchanged to the namespace.

    :param f function: The function to be wrapped
    '''

    name = f.__name__.replace('_', '')

    info = [f]
    info.extend(getfullargspec(f).args)

    __registry[name] = tuple(info)
    return f

def call(fname, json, source):
    '''Looks up a function by its name in the registry global and
    extracts the correct agruments from a source (such as an argparse result)
    and calls the function with the json and other arguments. The result is not
    returned to the caller.


    :param fname str: The string name of the function to be called.
    :param json: A JSON representation
    :param source obj: An object that contains the arguments needed for
        the function being called.

        ```
            call('addfield', json, args)
        ```

    '''
    f, *kwargs = __registry.get(fname)
    kwargs = {n:getattr(source, n) for n in kwargs if n != 'json'}
    f(json=json, **kwargs)


def act_on_path(json, path, action):
    '''Converts a JSONpath to a literal path in the JSON
    and preforms an action on the endpoint.

    :param action: A callable that accepts the penultimate endpoint and the
        index or key of the endpoint as the first two arguments.
        For additional arguments, tools such as `functools.partial` must
        be used.

    '''

    if path == root:
        return action(json, path)

    def process(item):
        # JSONpath indicies are denoted by [integer]
        # to be converted to a Python integer the brackets
        # must stripped out
        if '[' in item:
            item = item.replace('[', '').replace(']', '')
            item = int(item)
        return item

    *path, final = [process(item) for item in path.split('.') if item != root]

    json = json.data

    for item in path:
        json = json[item]

    return action(json, final)

def set_on_path(json, path, value):
    '''Sets an item at the end of a JSONpath.
    '''
    # setitem y u no kwargs?!
    action = lambda j, f, v: setitem(j, f, v)
    action = partial(action, v=value)
    act_on_path(json, path, action)

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
        dict_("key=value color=purple name=justanr")
         -> dict('key':'value', 'color':'purple', 'name':'justanr')

        ```

    Optionally accepts a secondary callable for converting either
    the key or the value. The callable must accept and return both.
    If the conversion fails, it must raise only AttributeError,
        TypeError or ValueError.
    '''

    if not captured:
        return partial(dict_, secondary=secondary)

    captured = shlex.split(captured)
    captured = [kv.split('=') for kv in captured]

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
