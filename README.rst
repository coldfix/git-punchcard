git-punchcard
=============

Simple git punchcard utility, inspired by git-punchcard-plot_ but rewritten
for python3 with matplotlib.

.. _git-punchcard-plot: https://github.com/guanqun/git-punchcard-plot


Installation
~~~~~~~~~~~~

The script can be obtained from PyPI:

.. code-block:: bash

    pip install --user git-punchcard

Alternatively, simply drop the ``git-punchcard`` script into ``~/.local/bin``
and add that folder to PATH.


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

You can pass additional ``git log`` options to restrict the range of commits
or author after ``--``, for example:

.. code-block:: bash

    git punchcard -- --author=myself master~20..master

Set the directory of the git repository as follows:

.. code-block:: bash

    git -C /path/to/repo punchcard
