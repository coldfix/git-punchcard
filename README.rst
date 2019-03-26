git-punchcard
=============

Simple git punchcard utility, inspired by git-punchcard-plot_ but rewritten
for python3 with matplotlib.

.. _git-punchcard-plot: https://github.com/guanqun/git-punchcard-plot

|Screenshot|


Installation
~~~~~~~~~~~~

Install or upgrade from PyPI_ as follows:

.. code-block:: bash

    pip install --user --upgrade git-punchcard

Also, make sure that ``$HOME/.local/bin`` is in ``$PATH``.

To avoid conflicts with other packages, I recommend installing into an
isolated environment, e.g. using pipx_:

.. code-block:: bash

    pipx install git-punchcard

.. _PyPI: https://pypi.org/project/git-punchcard
.. _pipx: https://github.com/pipxproject/pipx


Usage
~~~~~

Basic usage:

.. code-block:: bash

    git punchcard

Additional arguments can be specified as follows:

.. code-block:: bash

    git punchcard [options] [log options] [revision range] [-- pathes]

For more help on available options, type:

.. code-block:: bash

    git punchcard -h            # [options]
    git help log                # [log options]
    git help gitrevisions       # [revision]


Options
~~~~~~~

The most common builtin options are:

.. code-block:: bash

    # use a fixed timezone for all commits (case-sensitive):
    git punchcard --timezone CET

    # show punchcard with specified y/x axes:
    git punchcard -p year/month
    git punchcard -p wday/month

    # histogram with specified x axis:
    git punchcard -p /wday

    # set the directory of the git repository:
    git punchcard -C /path/to/repo

    # show a github-like punchcard plot with grid:
    git punchcard --grid

By default, each commit's local timezone is used for the plot.


git log options
~~~~~~~~~~~~~~~

Additionally, you can pass any options understood by ``git log`` to e.g.
restrict the range of commits and limit to commits performed by a certain
author:

.. code-block:: bash

    # include only commits by specific author:
    git punchcard --author=myself

    # consider only only the 20 commits:
    git punchcard master~20..master

    # commits within a certain time frame:
    git punchcard --since="1 year ago" --until=now

    # show at which times a certain file/folder is usually edited:
    git punchcard --follow -- README.rst docs

    # show at which times, people like to merge:
    git punchcard --merges


Advanced example
~~~~~~~~~~~~~~~~

Track evolution of commit activity over the years:

.. code-block:: bash

    for year in {2016..2019}; do
        git punchcard -o $year.png --title $year \
            --since 1.1.$year --until 31.12.$year
    done


.. resources:

.. |Screenshot| image:: https://raw.githubusercontent.com/coldfix/git-punchcard/master/screenshot.png
   :target:             https://raw.githubusercontent.com/coldfix/git-punchcard/master/screenshot.png
   :alt:                Screenshot
