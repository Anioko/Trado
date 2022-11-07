import nox


@nox.session(
    python=['3.10', '3.11'],
    reuse_venv=True)
def tests(session):
    """Runs a test build on packgaes"""
    with session.chdir("requirements"):
        session.install('-r', 'dev.txt')
        session.install('pytest')
    with session.chdir(".."):
        session.run('pytest')


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', '--import-order-style', 'google')
