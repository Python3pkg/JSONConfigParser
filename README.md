#JSONConfigParser
A JSON config editor built on top of [jsonpath-rw.](https://github.com/kennknowles/python-jsonpath-rw/).

##Use
Right now there is an example of building a CLI utility in the examples directory.

It can also be used programmatically as well by importing the `JSONConfigParser` class and the commands modules.

###Example CLI App

This is built with argparse. Using it is as simple as:

    ./example conf.json view -p $

That command will view the entire JSON file. Other actions include:

| command  | description                                                                                                                           |                                                                                                                                                                                                                                |
|----------|---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| addfile  | Concatenates a second JSON file onto the current. Warning: This will overwrite any shared keys.                                       | `./example.py conf.json addfile -o path/to/other.json`                                                                                                                                                                         |
| addfield | Adds a key and value to a specified JSONPath                                                                                          | `./example.py conf.json addfield -p $.name -v jsonconfigparser`                                                                                                                                                                |
| append   | Appends a value to the specified JSONPath. Optionally, converts the field to another type. Optionally, apply to every found endpoint. | `./example.py conf.json append -p $.things.[0] -v "Star bellied sneeches"`  `./example.py conf.json append -p $.products.hats -v "23.44" -t float`  `./example.py conf.json append -p $.products.[*].descript -v "A thing" -m` |
| delete   | Deletes an item from the specific JSONPath.                                                                                           | `./example.py conf.json delete $.products.hats`                                                                                                                                                                                |
| edit     | Reset the value at the endpoint of the JSONPath                                                                                       | `./example.py conf.json edit -p $.products.hats.descript -v "A really cool hat."`                                                                                                                                              |


Arguments:

| flags        | description                                                                                                                                               |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| -p/--path    | The path flag the only acceptable value is a JSONPath string                                                                                              |
| -o/--other   | The other file flag, used with addfile to concatenate files together                                                                                      |
| -v/--value   | The value flag, used with any action that requires a value                                                                                                |
| -m/--multi   | The multi boolean flag. Currently only used with append action. Defaults to false, if True append will add the value to every path found                  |
| -c/--convert | The conversion flag. Currently only used with append. Defaults to False. If passed, a value must be provided of `int`, `float`, `list`, `dict`, or `str`. |


##Todo:
There are several things that I want to do, small and big:

* Apply the conversion and multi flags to edit and delete as well.
* Construct an interactive prompt (probably using some combo of readlines and curses)
* Clean up the whole package up and turn what I can into classes/objects.

##NOTE: 
There is an issue with installing `jsonpath-rw` within setuptools. 
Currently, running `pip install -r REQUIREMENTS` is the best option after running `pip install --editable .`
