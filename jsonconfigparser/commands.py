from . import convert_input, list_, dict_, fieldtypes

def view(conf, field):
    conf.view(field)

def add_file(conf, existing):
    file = input("Please enter an additional config file to concat: ")
    conf.read(file)
    conf.write(existing)

def add_field(conf, file):
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
    conf.write(file)

def delete(conf, file, field=None):
    if field is None:
        msg = 'Are you sure you want to erase the whole config file?'
    else:
        msg = "Are you sure you want to erase the {} field?".format(field)

    confirm = input("{} [y/n]: ".format(msg))

    if confirm.lower().startswith('n'):
        return
    elif confirm.lower().startswith('y'):
        if field is None:
            conf.data = {}
        else:
            del conf[field]
    else:
        print("Invalid response.")
        return

    conf.write(file)

def default():
    print("That is an invalid action.")

def edit(conf, file, field=None):
    if not field:
        field = input("Please enter a field name to edit: ")

    t = str(type(conf[field]))

    t = fieldtypes.get(t, str)
    conf[field] = convert_input(
        converter=t,
        msg="Please enter a value for {}: ".format(field)
        )
    conf.write(file)

