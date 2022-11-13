import sys

import nox

PYTHON_VERSION = sys.version_info
version = '.'.join([str(PYTHON_VERSION[0]), str(PYTHON_VERSION[1])])
print(version)


@nox.session(python=[version], reuse_venv=True)
def tests(session):
    """Runs a test build on packgaes"""
    """with session.chdir("requirements"):
        session.install('-r', 'dev.txt')
        session.install('pytest')
    with session.chdir(".."):"""
    session.run('pytest')


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', '--import-order-style', 'google')
