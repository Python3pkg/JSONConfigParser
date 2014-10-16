'''

    Interactive Prompt for JSONConfigParser

    :copyright 2014: Alec Nikolas Reiter, contributors
    :license MIT: See LICENSE for more details


'''

import readline
import shlex
import sys

from functools import partial

from .configparser import JSONConfigParser
from .utils import call, command, root, __registry

__prompt = "JSON >>> "
__exit = False

def autocomplete(text, state):
    actions = [c for c in sorted(__registry.keys()) if c.startswith(text)]

    if state > len(actions):
        return None
    return actions[state]

def interpret(action):
    
    kwargs = {'multi':False, 'path':root, 'convert':False}

    action, *arguments = shlex.split(action)

    if action == 'shell':
        raise NotImplementedError("Can't spawn shell from inside shell.")

    for idx, item in enumerate(arguments):
        if item.startswith(root):
            kwargs['path'] = item
        elif any(m in item for m in ['-m', '--multi']):
            kwargs['multi'] = True
        elif any(o in item for o in ['-o', '--other']):
            kwargs['other'] = arguments[idx+1]
        elif any(c in item for c in ['-c', '--convert']):
            kwargs['convert'] = arguments[idx+1]
        elif any(v in item for v in ['-v', '--value']):
            kwargs['value'] = arguments[idx+1]

    return partial(call, fname=action, **kwargs)



def run(json):
    global __exit, __prompt

    readline.set_completer_delims("\t")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    while True:
        action = ""
        
        try:
            line = input("{}".format(__prompt)).strip()
        except KeyboardInterrupt:
            if __exit:
                sys.exit(0)
            else:
                print("Press ^C again to quit. Otherwise run another command.")
                __exit = True
                continue

        if not line:
            continue
        
        try:
            interpret(line)(json=json)
        except (NotImplementedError, KeyError,
            TypeError, ValueError) as e:
            print('{!s}: {!s}'.format(type(e).__name__, e))
            continue

        __exit = False
