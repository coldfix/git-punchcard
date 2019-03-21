git-punchcard
=============

Simple git punchcard utility, inspired by git-punchcard-plot_ but rewritten
for python3 with matplotlib.

.. _git-punchcard-plot: https://github.com/guanqun/git-punchcard-plot

|Screenshot|


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

The syntax of the command is as follows:

.. code-block:: bash

    git punchcard [options] [-- [log options] [revision range] [-- pathes]]

To get a list of available options, type:

.. code-block:: bash

    git punchcard --help        # for our own options

    git help log                # for possible git log options

    git help gitrevisions       # for revision range

The most important options are:

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


Advanced examples
~~~~~~~~~~~~~~~~~

You can pass additional ``git log`` options after a ``--``. This can for
example be used to restrict the range of commits and/or limit to commits
performed by a certain author:

.. code-block:: bash

    # include only commits by specific author:
    git punchcard -- --author=myself

    # consider only only the 20 commits:
    git punchcard -- master~20..master

    # commits within a certain time frame:
    git punchcard -- --since="1 year ago" --until=now

    # show at which times a certain file/folder is usually edited:
    # (the second -- is for git log):
    git punchcard -- --follow -- src
    git punchcard -- --follow -- docs

    # show at which times, people like to merge:
    git punchcard -- --merges

You can even to restrict to certain pathes within the git repository as
follows (note the second ``--`` is passed to and needed for the ``git log``
command line):

.. code-block:: bash

    git punchcard -- -- README.rst

Track evolution of commit activity over the years:

.. code-block:: bash

    for year in {2016..2019}; do
        git punchcard -o $year.png --title $year \
            -- --since 1.1.$year --until 31.12.$year
    done


.. resources:

.. |Screenshot| image:: https://raw.githubusercontent.com/coldfix/git-punchcard/master/screenshot.png
   :target:             https://raw.githubusercontent.com/coldfix/git-punchcard/master/screenshot.png
   :alt:                Screenshot
