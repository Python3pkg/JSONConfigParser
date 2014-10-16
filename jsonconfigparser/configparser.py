'''
    Build a JSON Configuration Parser that can view, write and edit
    a JSON conf file.

    :copyright 2014: Alec Nikolas Reiter, contributors
    :license MIT: See LICENSE for more details
'''


import json

from collections import UserDict
from contextlib import suppress
from pprint import pprint

from jsonpath_rw import parse

from .utils import root

class JSONConfigParser(UserDict):
    '''Essentially a wrapper around json.load and json.dump.'''
    def __init__(self, storage, source=None, encoder=None, decoder=None):
        self.storage = storage
        self.encoder = encoder or json.JSONEncoder
        self.decoder = decoder or json.JSONDecoder
        self.data = {}

        if source:
            self.read(source)

    def read(self, fp):
        '''Reads a file containing JSON and loads it into the
        JSONConfigParser.data dict. If an empty file is read,
        we simply ignore the exception.
        '''

        with suppress(ValueError):
            # if the JSON file is empty
            # json.load will throw a ValueError
            # we'll ignore it

            with open(fp, 'a+') as fh:
                # `a` opens file for appending
                # `+` creates the file if it does not exist
                # rewind to begining of file because append
                fh.seek(0)
                self.data.update(json.load(fh, cls=self.decoder))


    def view(self, path=root):
        '''Pretty prints an endpoint in the JSON.
        '''
        expr = parse(path)
        matches = expr.find(self.data)

        print('\n')
        for m in matches:
            print("{}:".format(m.full_path))
            pprint(m.value, indent=4)

    def write(self):
        '''Persists the current instance information to disk.'''
        with open(self.storage, 'w+') as fh:
            json.dump(self.data, fh, indent=4, sort_keys=True, cls=self.encoder)
