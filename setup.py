from setuptools import setup


def read_file(path):
    """Read a file in binary mode."""
    with open(path, 'rb') as f:
        return f.read()


def exec_file(path):
    """Execute a python file and return the `globals` dictionary."""
    namespace = {}
    try:
        exec(read_file(path), namespace, namespace)
    except ImportError:
        pass
    return namespace


metadata = exec_file('git_punchcard.py')

setup(
    version=metadata['__version__'],
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url=metadata['__uri__'],
    license=metadata['__license__'],
)
