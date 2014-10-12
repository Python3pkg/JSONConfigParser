from collections import MutableMapping, MutableSequence
from functools import partial
from operator import delitem

from jsonpath_rw import parse

from . import list_, dict_, fieldtypes
from .utils import command, act_on_path, root, set_on_path

@command
def view(json, path):
    '''A stored command for the view method of the JSONConfigParser
    object.
    '''
    json.view(path)

@command
def add_file(json, other):
    '''Updates the JSONConfigParser object with another JSON file.
    '''
    json.read(other)

@command
def add_field(json, path, value):
    '''Adds another field to the JSONConfigParser object.
    '''
    set_on_path(json, path, value)

@command
def append(json, path, value, multi=False, convert=False):
    expr = parse(path)
    matches = expr.find(json)

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

        Returns a callable that will either append or update depending on the
        container type.
        '''
        if isinstance(container, MutableMapping):
            return lambda j, f, v: j[f].update(v)
        return lambda j, f, v: j[f].append(v)

    if convert:
        if '=' in value:
            value = dict_(value)
        else:
            value = list_(value)

    for match in matches:
        action = guess_action(match.value)
        action = partial(action, v=value)
        act_on_path(json, str(match.full_path), action)

@command
def delete(json, path=None):
    '''Deletes a JSONPath endpoint from the JSONConfigParser object.
    '''
    if not path or path == '$':
        json = {}
    else:
        act_on_path(json, path, delitem)

@command
def edit(json, path, value):
    '''Updates the value at the JSONPath endpoint.
    '''
    set_on_path(json, path, value)
