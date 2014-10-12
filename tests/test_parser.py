from jsonconfigparser import JSONConfigParser

def test_init(tmpdir):
    test_file = tmpdir.join('test.conf')
    conf = JSONConfigParser(storage=test_file.strpath)

    assert conf.storage == test_file.strpath
    assert hasattr(conf, 'data')


def test_read(tmpdir):
    test_file = tmpdir.join('conf.json')
    test_file.write('{"test":"Yes"}')

    conf = JSONConfigParser(storage=test_file.strpath)
    conf.read(test_file.strpath)

    assert "test" in conf.data

def test_initread(tmpdir):
    test_file = tmpdir.join('conf.json')
    test_file.write('{"test":"Yes"}')

    conf = JSONConfigParser(storage=test_file.strpath, source=test_file.strpath)

    assert "test" in conf.data

def test_write(tmpdir):
    test_file = tmpdir.join('test.conf') 
    conf = JSONConfigParser(storage=test_file.strpath)
    conf['test'] = "Yes"
    conf.write()

    contents = test_file.read()

    assert "test" in contents
    assert "Yes" in contents

def test_view(tmpdir, capsys):
    test_file = tmpdir.join('test.conf')
    conf = JSONConfigParser(storage=test_file.strpath)
    conf['test'] = "Yes"
    conf.view('$')

    captured, _ = capsys.readouterr()

    assert "$" in captured
    assert "'test'" in captured
    assert "'Yes'" in captured

def test_multiview(tmpdir, capsys):
    test_file = tmpdir.join('test.conf')
    conf = JSONConfigParser(storage=test_file.strpath)
    conf["packages"] = ["jsonconfigparser", "ply", "decorator"]

    conf.view("$.packages.[*]")

    captured, _ = capsys.readouterr()

    assert "packages.[1]" in captured
    assert "ply" in captured
