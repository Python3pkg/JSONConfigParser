#!/usr/bin/env python3

'''
    Command line interface for JSONConfigParser.

    :copyright: Alec Nikolas Reiter, contributors
    :license MIT: See ..LICENSE for details
'''


import argparse

from .configparser import JSONConfigParser
from .utils import call

parser = argparse.ArgumentParser()

# positional arguments
parser.add_argument(
    "file",
    help="Path to config file, may be relative or absolute."
    )
parser.add_argument("command", help="Action to take on the config file")

# optional arguments
parser.add_argument(
    "-p",
    "--path",
    help="Specific field to act on. If not passed, act on the whole file.",
    default="$"
    )

parser.add_argument(
    "-o",
    "--other",
    help="Used with the addfile command to read in another file.",
    default=""
    )

parser.add_argument(
    "-v",
    "--value",
    help="Used with several commands that require a value.",
    default=""
    )

parser.add_argument(
    "-m",
    "--multi",
    help="Boolean flag for the append command for handling multiple results "
    "along the path. Defaults to false.",
    action="store_true"
    )

parser.add_argument(
    '-c',
    '--convert',
    help="Optional conversion flag.",
    default=False
    )


def cli():
    ''' Entry point for CLI functionality. This is what is run when `jsonconf`
    is called on the command line.
    '''

    args = parser.parse_args()
    kwargs = vars(args)
    source = kwargs.pop('file')
    command = kwargs.pop('command')

    conf = JSONConfigParser(source=source, storage=source)
    call(command, conf, **kwargs)
    conf.write()

if __name__ == "__main__":
    cli()
