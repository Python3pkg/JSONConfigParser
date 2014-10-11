from collections import MutableMapping, MutableSequence
from functools import partial
from operator import delitem, setitem

from jsonpath_rw import parse, Root

from . import list_, dict_, fieldtypes
from .utils import command, act_on_path, root, set_on_path

@command
def view(json, path):
    '''A stored command for the view method of the JSONConfigParser
    object.
    '''

    print('\n{}:'.format(path))
    act_on_path(
        json.data,
        path,
        # the view method only accepts
        # an endpoint to pprint and aop
        # attempts to pass the walked JSON path
        # and the final endpoint to the callable
        lambda j,p: json.view(j)
        )
    print('\n')

@command
def add_file(json, file):
    '''Updates the JSONConfigParser object with another JSON file.
    '''
    json.read(file)

@command
def add_field(json, path, value):
    '''Adds another field to the JSONConfigParser object.
    '''
    set_on_path(json.data, path, value)

@command
def append(json, path, value, multi=False):
    expr = parse(path)
    matches = expr.find(json.data)

    if not all(isinstance(m.value, (MutableMapping, MutableSequence)) for m \
        in matches):
            raise TypeError("Expected mutable container at endpoint for {}."
                "".format(path))

    if len(matches) > 1 and not multi:
        raise AttributeError("Multiple paths found for {}. Please specify the "
        "multi flag if this is intended.".format(path))

    def guess_action(container):
        '''Guess if we're dealing with a dict/object endpoint
        or a list/array endpoint.

        Returns the appropriate converter and action callable for act_on_path
        '''
        if isinstance(container, MutableMapping):
            return lambda j,f,v: json[f].update(dict_(v))
        return lambda j,f,v: json[f].extend(list_(v))

    for match in matches:
        action = guess_action(match.value)
        action = partial(action, v=value)
        act_on_path(json, path, action)

@command
def delete(json, path=None):
    '''Deletes a JSONPath endpoint from the JSONConfigParser object.
    '''
    if not path or path == '$':
        json.data = {}
    else:
        act_on_path(json.data, path, delitem)

@command
def edit(json, path, value):
    '''Updates the value at the JSONPath endpoint.
    '''
    set_on_path(json.data, path, value)
