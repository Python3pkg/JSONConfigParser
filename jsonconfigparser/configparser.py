'''
    Build a JSON Configuration Parser that can view, write and edit
    a JSON conf file.

    copyright 2014 Alec Nikolas Reiter
    license MIT
'''


import json

from collections import UserDict
from pprint import pprint

class JSONConfigParser(UserDict):
    '''Essentially a wrapper around json.load and json.dump.'''
    def __init__(self, encoder=None, decoder=None):
        self.encoder = encoder or json.JSONEncoder
        self.decoder = decoder or json.JSONDecoder
        self.data = {}

    def read(self, fp):
        '''Reads a file containing JSON and loads it into the
        JSONConfigParser.data dict. If an empty file is read,
        we simply ignore the exception.
        '''
        try:
            # `a` opens file for appending
            # `+` creates the file if it does not exist.
            with open(fp, 'a+') as fh:
                # rewind to begining of file
                fh.seek(0)
                self.data = json.load(fh, cls=self.decoder)

        except ValueError:
            # if the JSON file is empty
            # json.load will throw a ValueError
            # stating as much, for now, we'll ignore it
            pass

    def view(self):
        '''A shortcut for `pprint(JSONConfigParser.data, indent=4)`'''
        pprint(self.data, indent=4)

    def write(self, fp):
        '''Persists the current instance information to disk.'''
        with open(fp, 'w+') as fh:
            json.dump(self.data, fh, indent=4, sort_keys=True, cls=self.encoder)
