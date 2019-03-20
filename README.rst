git-punchcard
=============

Simple git punchcard utility, inspired by git-punchcard-plot_ but rewritten
for python3 with matplotlib.

.. _git-punchcard-plot: https://github.com/guanqun/git-punchcard-plot


Installation
~~~~~~~~~~~~

**The pragmatic way:** The script can be obtained from PyPI:

.. code-block:: bash

    pip install --user git-punchcard

Also, make sure that ``~/.local/bin`` is in ``$PATH``. If it is not there, add
the following lines to ``.bashrc`` or ``.zshrc``:

.. code-block:: bash

    PATH=$PATH:$HOME/.local/bin


**The elegant way:** Get pipx_ and then run ``pipx install git-punchcard`` to
install into an isolated environment.


**The crude way:** Alternatively, simply drop the ``git-punchcard`` script
into ``~/.local/bin`` and add that folder to PATH.


.. _pipx: https://github.com/pipxproject/pipx


Usage
~~~~~

Show a github-like punchcard plot with grid:

.. code-block:: bash

    git punchcard --grid

By default, the author's local timezone is used for the plot. In order to use
a fixed timezone for all commits, you have to specify a ``--timezone``
argument, e.g.:

.. code-block:: bash

    git punchcard --timezone CET

Set the directory of the git repository as follows:

.. code-block:: bash

    git punchcard -C /path/to/repo

You can pass additional ``git log`` options after a ``--``. This can for
example be used to restrict the range of commits and/or limit to commits
performed by a certain author:

.. code-block:: bash

    git punchcard -- --author=myself master~20..master

You can even to restrict to certain pathes within the git repository as
follows (note the second ``--`` is passed to and needed for the ``git log``
command line):

.. code-block:: bash

    git punchcard -- -- README.rst
