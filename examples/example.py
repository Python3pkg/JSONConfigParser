#!/usr/bin/env python3

import argparse

from collections import namedtuple

from jsonconfigparser import (
    JSONConfigParser, view, add_file, 
    add_field, delete, edit
    )

parser = argparse.ArgumentParser()

# positional arguments
parser.add_argument(
    "file", 
    help="Path to config file, may be relative or absolute."
    )
parser.add_argument("command", help="Action to take on the config file")

# optional arguments
parser.add_argument(
    "-f",
    "--field", 
    help="Specific field to act on. If not passed, act on the whole file.",
    default=None
    )

# run the parser and collect the arguments
args = parser.parse_args()

# open up our json config file and read it.
conf = JSONConfigParser()
conf.read(args.file)

# stuff actions into a dictionary for easy use
Command = namedtuple('Command', ['func', 'args'])

commands = {
    "view" : Command(view, [conf, args.field]),
    "addfile" : Command(add_file, [conf, args.file]),
    "addfield" : Command(add_field, [conf, args.file]),
    "delete" : Command(delete, [conf, args.file, args.field]),
    "edit" : Command(edit, [conf, args.file, args.field])
    }

if __name__ == "__main__":
    command = commands.get(
        args.command, 
        Command(
            lambda: print("Invalid Command."), 
            []
            )
        )
    command.func(*command.args)
