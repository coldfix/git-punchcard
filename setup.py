from setuptools import setup


def exec_file(path):
    """Execute a python file and return the `globals` dictionary."""
    with open(path, 'rb') as f:
        code = compile(f.read(), path, 'exec')
    namespace = {}
    try:
        exec(code, namespace, namespace)
    except ImportError:     # ignore missing dependencies at setup time
        pass                # and return dunder-globals anyway!
    return namespace


metadata = exec_file('git_punchcard.py')

setup(
    version=metadata['__version__'],
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url=metadata['__url__'],
    license=metadata['__license__'],
)
