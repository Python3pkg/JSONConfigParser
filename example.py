import argparse

from jsonconfigparser import (JSONConfigParser, convert_input, 
    list_, dict_, fieldtypes)

parser = argparse.ArgumentParser()

# positional arguments
parser.add_argument(
    "file", 
    help="Path to config file, may be relative or absolute."
    )
parser.add_argument("action", help="Action to take on the config file")

# optional arguments
parser.add_argument(
    "--field", 
    help="Specific field to act on. If not passed, act on the whole file.",
    default=None
    )

# run the parser and collect the arguments
args = parser.parse_args()

# open up our json config file and read it.
conf = JSONConfigParser()
conf.read(args.file)

# define actions
def view():
    conf.view(args.field)

def add_file():
    file = input("Please enter an additional config file to concat: ")
    conf.read(file)
    conf.write(args.file)

def add_field():
    name, field = convert_input(
        converter=list_,
        msg='Please enter a name and type of field: '
        )
    
    field = fieldtypes.get(field, str)

    captured = convert_input(
        converter=field,
        msg="Please enter a value for {}".format(name)
        )

    conf[name] = captured
    conf.write(args.file)

def delete():
    if args.field is None:
        msg = 'Are you sure you want to erase the whole config file?'
    else:
        msg = "Are you sure you want to erase the {} field?".format(args.field)

    confirm = input("{} [y/n]: ".format(msg))

    if confirm.lower().startswith('n'):
        return
    elif confirm.lower().startswith('y'):
        if args.field is None:
            conf.data = {}
        else:
            del conf[args.field]
    else:
        print("Invalid response.")
        return

    conf.write(args.file)

def default():
    print("That is an invalid action.")

def edit():
    if not args.field:
        args.field = input("Please enter a field name to edit: ")

    t = str(type(conf[args.field]))

    t = fieldtypes.get(t, str)
    conf[args.field] = convert_input(
        converter=t,
        msg="Please enter a value for {}: ".format(args.field)
        )
    conf.write(args.file)


# stuff actions into a dictionary for easy use
actions = {
    "view" : view,
    "addfile" : add_file,
    "addfield" : add_field,
    "delete" : delete,
    "default" : default,
    "edit" : edit
    }

if __name__ == "__main__":
    actions.get(args.action, default)()
