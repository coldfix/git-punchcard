from setuptools import setup


def read_file(path):
    """Read a file in binary mode."""
    with open(path, 'rb') as f:
        return f.read()


def exec_file(path):
    """Execute a python file and return the `globals` dictionary."""
    namespace = {}
    exec(read_file(path), namespace, namespace)
    return namespace


metadata = exec_file('git-punchcard')
long_description = read_file('README.rst').decode('utf-8')

setup(
    name=metadata['__title__'],
    version=metadata['__version__'],
    description=metadata['__summary__'],
    long_description=long_description,
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url=metadata['__uri__'],
    license=metadata['__license__'],
    scripts=['git-punchcard'],
    install_requires=[
        'numpy',
        'matplotlib',
        'docopt',
        'pytz',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: Public Domain',
        'Topic :: Software Development :: Version Control :: Git',
    ],
)
