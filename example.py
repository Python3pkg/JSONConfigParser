from jsonconfigparser import JSONConfigParser, convert_input, list_, dict_


fields = {
    'name' : {'msg' : 'Please enter your username'},
    'email' : {'msg' : 'Please enter your email.'},
    'twitter' : {
        'msg' : "Please enter your pulic and private Twitter API keys.",
        "converter" : dict_(secondary=lambda k,v: (k.lower(), v))
        },
    'colors' : {
        'msg' : "Please enter a list of your favorite colors",
        'converter' : list_
        }
    }


conf = JSONConfigParser()

conf.read('example.conf')

if not conf.data:
    for field, settings in sorted(fields.items()):
        conf[field] = convert_input(**settings)

conf.write('example.conf')
conf.view()
