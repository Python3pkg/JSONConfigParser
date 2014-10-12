from jsonconfigparser import commands, JSONConfigParser

import pytest

def test_view_command(tmpdir, capsys):
    
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)
    conf["package"] = "jsonconfigparser"

    commands.view(conf, '$.package')

    captured, _ = capsys.readouterr()

    assert "jsonconfigparser" in captured

def test_add_file(tmpdir):
    test_one = tmpdir.join("test1.json")
    test_two = tmpdir.join("test2.json")
    test_two.write('{"test":"Yes"}')
    conf = JSONConfigParser(storage=test_one.strpath)

    commands.add_file(conf, test_two.strpath)

    assert "test" in conf
    assert conf['test'] == "Yes"

def test_add_field(tmpdir):
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    commands.add_field(conf, "$.package", "jsonconfigparser")

    assert "package" in conf
    assert conf["package"] == "jsonconfigparser"


def test_append_immutable_raises_error(tmpdir):
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)
    conf['packages'] = 'jsonconfigparser'

    with pytest.raises(TypeError) as excinfo:
        commands.append(conf, "$.packages", "jsonconfigparser")

    assert "mutable container" in str(excinfo.value)
   

def test_append_to_list(tmpdir):
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)
    conf['packages'] = []

    commands.append(conf, "$.packages", "jsonconfigparser")

    assert "jsonconfigparser" in conf['packages']

def test_append_multi_raise_error(tmpdir):
    test_file = tmpdir.join("test.join")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['packages'] = [[], []]

    with pytest.raises(AttributeError) as excinfo:
        commands.append(conf, '$.packages.[*]', "Test")

    assert excinfo.value

def test_append_to_dict(tmpdir):
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['settings'] = {}

    commands.append(conf, "$.settings", {"testing":"Yes"})

    assert conf['settings']['testing'] == "Yes"


def test_append_to_mutliple_list(tmpdir):

    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['packages'] = [[], []]

    commands.append(conf, '$.packages.[*]', "Test", multi=True)

    assert "Test" in conf['packages'][0]
    assert "Test" in conf['packages'][1]

def test_append_to_multiple_dict(tmpdir):
    
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['packages'] = [{}, {}]

    commands.append(conf, '$.packages.[*]', {"installed":True}, multi=True)

    assert all(n['installed'] for n in conf['packages'])


def test_append_convert_to_list(tmpdir):

    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['things'] = []

    commands.append(conf, "$.things", "1 2 3", convert=True)

    assert ["1", "2", "3"] in conf['things']


def test_append_convet_to_dict(tmpdir):

    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['things'] = []

    commands.append(conf, "$.things", "color=purple", convert=True)

    assert {"color":"purple"} in conf['things']


def test_delete(tmpdir):
    
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)
    conf['things'] = []

    commands.delete(conf, "$.things")

    assert "things" not in conf

    commands.delete(conf, "$")

    assert not conf.data

def test_edit(tmpdir):
    
    test_file = tmpdir.join("test.json")
    conf = JSONConfigParser(storage=test_file.strpath)

    conf['testing'] = False

    commands.edit(conf, "$.testing", True)

    assert conf['testing']
