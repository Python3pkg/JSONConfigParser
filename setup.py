import os, sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    # Taken from the py.test setuptools integration page 
    # http://pytest.org/latest/goodpractises.html
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

def read(fp):
    fp = os.path.join(
        os.path.dirname(__file__),
        fp
        )

    with open(fp) as fh:
        data = fh.readlines()

    return data

requires = read("REQUIREMENTS")
# if installed under the editable flag, this will be present
# so we need to strip it out.
requires = [d.strip('\n') for d in requires if "JSONConfigParser" not in d ]

test_requires = [d.strip('\n') for d in read("TEST_REQUIREMENTS")]

if __name__ == '__main__':

    setup(
        name="jsonconfigparser",
        version="0.1.0",
        author="Alec Nikolas Reiter",
        author_email="alecreiter@gmail.com",
        description="Quick and easy editting of JSON files.",
        license="MIT",
        url="https://github.com/justanr/JSONConfigParser",
        keywords="CLI json config",
        packages=["jsonconfigparser"],
        classifiers=[
            'Development Status :: 3 - Alpha' ,
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License'
            ],
        install_requires=requires,
        tests_requires=test_requires,
        cmdclass = {'tests' : PyTest},
        entry_points={
            'console_scripts':
                ['jsonconf=jsonconfigparser:cli']
            },
        test_suite='tests',
        )
