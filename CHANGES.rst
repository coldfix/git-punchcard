Changes
=======

2.0.4
~~~~~
Date: 28.10.2021

- add pyqt as optional *gui* dependency, e.g.: ``pip install git-punchcard[gui]``
- migrate from Travis CI to GitHub Actions


2.0.3
~~~~~
Date: 31.10.2019

- include license file in source distribution


2.0.2
~~~~~
Date: 31.10.2019

- automatic deployments
- changes in setup and testing


2.0.1
~~~~~
Date: 26.03.2019

- fix: default to current directory if no input pathes were passed by the user


2.0.0
~~~~~
Date: 26.03.2019

- turn ``-C`` into positional argument, remove ``-C`` option
- allow multiple input files
- allow passing ``-`` and files with ``git log`` output as input files
- remove obsolete dependency on docopt
- allow passing country codes and names instead of timezone (using first
  available timezone in case of ambiguity)
- match timezones case-insensitively
- show git command and number of commits
- show error message without traceback for common errors


1.4.0
~~~~~
Date: 26.03.2019

- learn ``--period Y/X`` parameter to specify Y/X axes
- can plot histograms by leaving one of the axes empty
- understand ``-v`` as alias for ``--version``


1.3.0
~~~~~
Date: 21.03.2019

- log options are now passed directly without ``--`` same as the other options
- drop dependency on docopt


1.2.0
~~~~~
Date: 21.03.2019

- fix setup.py exception if called without runtime dependencies
- import pytz only if needed
- learn a ``-C DIR`` parameter to pass the path to the git repository
- learn a ``--version`` parameter to show the script version
- fix error when passing options and git options at the same time
- turn into a module and use setuptools entry_points to generate script


1.1.0
~~~~~
Date: 11.03.2019

- add ``--title`` parameter
