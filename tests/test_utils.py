from jsonconfigparser import utils, JSONConfigParser
import pytest

def test_command_deco():
    
    @utils.command
    def underscored_func(json, arg):
        pass

    assert "underscoredfunc" in utils.__registry
    assert underscored_func in utils.__registry["underscoredfunc"]
    assert "arg" in utils.__registry['underscoredfunc']

def test_call():

    @utils.command
    def test_func(json, this, other):
        pass

    # generic data store
    # look into mocking solution for this
    store = lambda: None
    store.this = None
    store.other = None

    assert utils.call("testfunc", {}, store)

def test_call_propagates():

    @utils.command
    def test_func(json, this, other):
        raise TypeError(True)

    # generic data store
    # look into mocking solution for this
    store = lambda: None
    store.this = None
    store.other = None

    with pytest.raises(TypeError) as excinfo:
        utils.call('testfunc', {}, store)

    assert excinfo.value

def test_act_on_path(tmpdir, capsys):
    
    test_file = tmpdir.join('test.conf')
    conf = JSONConfigParser(storage=test_file.strpath)
    conf['test'] = "Yes"

    action = lambda j, f: print(j, f)

    utils.act_on_path(conf, '$', action)

    captured, _ = capsys.readouterr()

    assert '$' in captured
    assert 'test' in captured

    conf['packages'] = ['jsonconfigparser']

    utils.act_on_path(conf, "$.packages.[1]", action)

    captured, _ = capsys.readouterr()

    assert "1" in captured
    assert "jsonconfigparser" in captured

def test_set_on_path(tmpdir):
    
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)
    
    utils.set_on_path(conf, '$.packages', ['jsonconfigparser'])

    assert 'packages' in conf
    assert 'jsonconfigparser' == conf['packages'][0]

def test_list_converter():

    converted = utils.list_("1 2 3")

    assert isinstance(converted, list)
    assert "1" == converted[0]
    assert "2" == converted[1]
    assert "3" == converted[2]

def test_list__secondary():
    
    converted = utils.list_("1 2 3", secondary=int)

    assert 1 == converted[0]
    assert 2 == converted[1]
    assert 3 == converted[2]

    assert utils.list_(secondary=int)("1 2 3") == converted

def test_dict_converter():

    converted = utils.dict_("first=1 second=2 third=3")

    assert isinstance(converted, dict)
    assert converted["first"] == "1"
    assert converted["second"] == "2"
    assert converted["third"] == "3"

def test_dict__secondary():
    
    action = lambda k,v: (k.upper(), int(v))

    converted = utils.dict_("first=1 second=2", secondary=action)

    assert converted["FIRST"] == 1
    assert converted["SECOND"] == 2

    assert utils.dict_(secondary=action)("first=1 second=2") == converted
