'''
    JSONConfigParser: Simple and easy editting of JSON files

    :copyright 2014: Alec Nikolas Reiter, contributors
    :license MIT: See LICENSE for details


'''

from .configparser import JSONConfigParser
from .utils import dict_, list_, fieldtypes, command, call
from .cli import cli
from . import commands, shell

version = '0.1.2'
