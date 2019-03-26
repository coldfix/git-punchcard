#!/usr/bin/env python
"""
Generate a github-like punchcard for git commit activity.

Usage:
    git-punchcard [<input path>...] [<options>]
                  [--] [<log options>] [<revision range>] [-- <path>...]

Options:
    -o FILE, --output FILE          Set output file
    -t TZ, --timezone TZ            Set timezone
    -p PERIOD, --period PERIOD      Graphed time period, e.g.: "wday/hour"
    -w WIDTH, --width WIDTH         Plot width in inches
    -g, --grid                      Enable grid
    --title TITLE                   Set graph title

    -h                              Show this help
    -v, --version                   Show version and exit

Input pathes can be

- files with output from `git log --pretty=format:%ai` (or '-' for stdin)
- folders corresponding to git repositories

All further options are passed directly to `git log` and can be used to
restrict the range of commits taken into account. For more info, see `git
help log`.
"""

__version__ = '2.0.0'
__author__  = 'Thomas Gläßle'
__email__   = 'thomas@coldfix.de'
__license__ = 'Unlicense'
__uri__     = 'https://github.com/coldfix/git-punchcard'

import numpy as np
import matplotlib.pyplot as plt

import os
import sys
import shlex
import subprocess
from datetime import datetime, timedelta
from argparse import ArgumentParser


def argument_parser():
    parser = ArgumentParser()
    parser.format_help = lambda: __doc__.lstrip()
    add_argument = parser.add_argument
    add_argument('-o', '--output',   type=str)
    add_argument('-t', '--timezone', type=str)
    add_argument('-p', '--period',   type=str)
    add_argument('-w', '--width',    type=int)
    add_argument('--title',          type=str)
    add_argument('-g', '--grid',     action='store_true')
    add_argument('-v', '--version',  action='version', version=__version__)
    return parser


def main(args=None):
    parser = argument_parser()
    options, remaining = parser.parse_known_args(args)
    output   = options.output
    tz_name  = options.timezone
    period   = options.period
    grid     = options.grid
    title    = options.title
    width    = options.width or 10

    # Detect passed input files/folders versus git options, note that if you
    # have weirdly named files in your local directory, you must pass '--' to
    # ensure that git_opts are recognized properly:
    git_dirs = []
    git_opts = []
    for i, arg in enumerate(remaining):
        if arg == '--':
            git_opts.extend(remaining[i+1:])
            break
        elif arg == '-' or os.path.exists(arg):
            git_dirs.append(arg)
        else:
            git_opts.append(arg)

    dates = []
    for folder in git_dirs:
        try:
            dates.extend(get_commit_times(folder, git_opts))
        except subprocess.CalledProcessError:
            raise SystemExit(1)
    if not dates:
        raise SystemExit("No commits match the specified restrictions.")
    print("Processing {} commits.".format(len(dates)))

    if tz_name:
        dates = dates_to_timezone(dates, tz_name)

    period = period or 'wday/hour'
    fig = plot_date_counts(
        dates, period, width=width, grid=grid, title=title)

    savefig(fig, output)


def dates_to_timezone(dates, tz_name):
    """Transform a list of datetime objects to specified timezone."""
    tz, delta = parse_timezone(tz_name)
    sec = int(delta.total_seconds())
    deltastr = '{:+03}:{:02}'.format(sec // 3600, sec // 60 % 60) if sec else ''
    print("Timezone: {}{}".format(tz, deltastr))
    return [date.astimezone(tz) + delta for date in dates]


def parse_timezone(tz_name):
    """Parse and return a tuple ``(timezone, timedelta)``."""
    from pytz import timezone
    delta = timedelta(0)
    for sign in '+-':
        if sign in tz_name:
            tz_name, offset = tz_name.split(sign)
            parts = [int(x) for x in (sign + offset).split(':')]
            delta = timedelta(**dict(zip(['hours', 'minutes'], parts)))
            break
    tz_name = tz_name or 'UTC'
    matches = find_timezone_name(tz_name)
    if not matches:
        raise SystemExit(
            'Unknown timezone: {!r}.'.format(tz_name))
    return timezone(matches[0]), delta


def find_timezone_name(tz_name):
    """
    Return list of matching timezones by name, country code, or country name.
    Search is case insensitive.
    """
    from pytz import all_timezones_set, country_timezones, country_names
    if tz_name in all_timezones_set:
        return [tz_name]
    # Case insensitive matching:
    tz_name = tz_name.upper()
    timzones = {tz.upper(): tz for tz in all_timezones_set}
    if tz_name in timzones:
        return [timzones[tz_name]]
    # Select by country code:
    if tz_name in country_timezones:
        return country_timezones[tz_name]
    # Select by country name:
    country_codes = {
        name.upper(): code for code, name in country_names.items()}
    if tz_name in country_codes:
        return country_timezones[country_codes[tz_name]]
    return []


def plot_date_counts(dates, period='wday/hour', *,
                     width=10, grid=False, title=None):
    """
    Create and return a histogram/punchcard figure with ``dates`` counted as
    specified by ``period``.
    """
    if '/' in period:
        yname, xname = period.split('/')
        check_period(xname or yname, Classifiers.KNOWN)
        check_period(yname or xname, Classifiers.KNOWN)
    else:
        check_period(period, Classifiers.SHORT)
        xname, yname = Classifiers.SHORT[period]

    xdata, xlabel, xmin, xmax = getattr(Classifiers, xname or 'none')(dates)
    ydata, ylabel, ymin, ymax = getattr(Classifiers, yname or 'none')(dates)

    counts = np.zeros((xmax-xmin+1, ymax-ymin+1))
    for x, y in zip(xdata, ydata):
        counts[x - xmin][y - ymin] += 1

    fig, ax = makefig(width=width, grid=grid, title=title)
    if xname and yname:
        punchcard(ax, counts[:, ::-1], xlabel, ylabel[::-1])
    else:
        histogram(ax, counts[:, ::-1], xlabel, ylabel[::-1])
    return fig


def check_period(period, allowed):
    if period not in allowed:
        raise SystemExit(
            "Unknown period: {!r}, must be one of: [{}]"
            .format(period, ', '.join(allowed)))


def get_commit_times(folder, git_opts):
    folder = folder or '.'
    if folder == '-':
        print("Reading dates from STDIN".format(folder))
        stdout = sys.stdin.read()
    elif os.path.isfile(folder):
        print("Reading dates from {!r}".format(folder))
        with open(folder) as f:
            stdout = f.read()
    else:
        argv = ['git', '-C', folder, 'log', '--pretty=format:%ai'] + git_opts
        cmdl = ' '.join(map(shlex.quote, argv))
        print("Running: {!r}".format(cmdl))
        stdout = subprocess.check_output(argv).decode('utf-8')
    return [
        datetime.strptime(line, '%Y-%m-%d %H:%M:%S %z')
        for line in stdout.splitlines()
    ]


class Classifiers:

    KNOWN = ['year', 'month', 'wday', 'hour']
    SHORT = {
        'year': ('month', 'year'),
        'month': ('month', 'wday'),
        'wday': ('hour', 'wday'),
    }

    def year(dates):
        values = [d.year for d in dates]
        first = min(values)
        last = max(values)
        labels = [str(year) for year in range(first, last+1)]
        return (values, labels, first, last)

    def month(dates):
        values = [d.month for d in dates]
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return (values, labels, 1, 12)

    def wday(dates):
        values = [d.weekday() for d in dates]
        labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return (values, labels, 0, 6)

    def hour(dates):
        values = [d.hour for d in dates]
        labels = ['{}'.format(x) for x in range(25)]
        return (values, labels, 0, 23)

    def none(dates):
        values = [0 for d in dates]
        labels = []
        return (values, labels, 0, 0)


def set_ticks(ax, axis, labels, size, **kwargs):
    set_lim    = getattr(ax, 'set_{}lim'.format(axis))
    set_ticks  = getattr(ax, 'set_{}ticks'.format(axis))
    set_labels = getattr(ax, 'set_{}ticklabels'.format(axis))

    set_lim(0, size)
    set_ticks(np.arange(size + 1), minor=False)
    set_ticks(np.arange(size) + 0.5, minor=True)
    ax.tick_params(axis=axis, which='minor', length=0)

    if len(labels) == size:
        # labels centered in bin
        set_labels(["" for _ in range(size+1)], minor=False)
        set_labels(labels, minor=True, **kwargs)
    else:
        # labels at bin edges:
        set_labels(labels, minor=False, **kwargs)
        set_labels(["" for _ in range(size)], minor=True)


def makefig(width=10, grid=False, title=None):
    fig, ax = plt.subplots()
    fig.tight_layout()
    fig.set_figwidth(width)
    ax.set_title(title)
    ax.grid(grid)
    return fig, ax


def histogram(ax, counts, xlabels, ylabels, rwidth=0.85, **kwargs):
    num = counts.size
    if xlabels:
        set_ticks(ax, 'x', xlabels, num)
        orientation = 'vertical'
        counts = counts[:, 0]
    else:
        set_ticks(ax, 'y', ylabels, num)
        orientation = 'horizontal'
        counts = counts[0, :]
    return ax.hist(
        range(num), range(num+1), weights=counts,
        orientation=orientation, rwidth=rwidth, **kwargs)


def punchcard(ax, counts, xlabels, ylabels):
    ax.set_aspect(1, adjustable='box')
    set_ticks(ax, 'x', xlabels, counts.shape[0])
    set_ticks(ax, 'y', ylabels, counts.shape[1])
    max_radius = 0.9
    for (x, y), value in np.ndenumerate(counts / counts.max() * max_radius):
        if value > 0:
            draw_circle(
                ax, x + 0.5, y + 0.5,
                value ** 0.50 / 2,
                value ** 0.25)


def savefig(fig, output=None):
    if output:
        fig.savefig(output, bbox_inches='tight')
    else:
        plt.show()


def draw_circle(ax, x, y, radius, opacity=1):
    color = (1-opacity, 1-opacity, 1-opacity)
    ax.add_patch(plt.Circle(
        (x, y), radius, color=color,
        linestyle=None, linewidth=0))


if __name__ == '__main__':
    main()
