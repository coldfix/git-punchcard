#!/usr/bin/env python
"""
Generate a github-like punchcard for git commit activity.

Usage:
    git-punchcard [-o FILE] [-C DIR] [-t TZ]
                  [--grid] [-w WIDTH] [--title TITLE]
                  [-- <GIT-OPTIONS>...]

Options:
    -C DIR, --git-dir DIR           Set path for git repository
    -o FILE, --output FILE          Set output file
    -t TZ, --timezone TZ            Set timezone
    -w WIDTH, --width WIDTH         Plot width in inches
    -g, --grid                      Enable grid
    --title TITLE                   Set graph title

All further options are passed directly to `git log` and can be used to
restrict the range of commits taken into account. For more info, see `git
help log`.
"""

__version__ = '1.2.0'
__author__  = 'Thomas Gläßle'
__email__   = 'thomas@coldfix.de'
__license__ = 'Unlicense'
__uri__     = 'https://github.com/coldfix/git-punchcard'

import docopt
import numpy as np
import matplotlib.pyplot as plt

import subprocess
from datetime import datetime, timedelta


def main(args=None):
    options  = docopt.docopt(__doc__, args, version=__version__)
    git_opts = options['<GIT-OPTIONS>']
    folder   = options['--git-dir']
    output   = options['--output']
    tz_name  = options['--timezone']
    grid     = options['--grid']
    title    = options['--title']
    width    = int(options['--width'] or 10)

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = ['{}'.format(x) for x in range(25)]

    dates = get_commit_times(folder, git_opts)

    if tz_name:
        from pytz import timezone
        try:
            tz = timezone(timedelta(hours=float(tz_name)))
        except ValueError:
            tz = timezone(tz_name)
        dates = [date.astimezone(tz) for date in dates]

    counts = np.zeros((7, 24))
    for date in dates:
        counts[date.weekday()][date.hour] += 1

    punchcard(
        counts.T[:, ::-1], hours, days[::-1],
        output=output, width=width, grid=grid, title=title)


def get_commit_times(folder, git_opts):
    folder = folder or '.'
    argv = ['git', '-C', folder, 'log', '--pretty=format:%ai'] + git_opts
    stdout = subprocess.check_output(argv).decode('utf-8')
    return [
        datetime.strptime(line, '%Y-%m-%d %H:%M:%S %z')
        for line in stdout.splitlines()
    ]


def punchcard(counts, xlabels, ylabels, output=None, width=10, grid=False,
              title=None):

    fig, ax = plt.subplots()
    fig.tight_layout()
    fig.set_figwidth(width)

    def set_ticks(axis, labels, size):
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
            set_labels(labels, minor=True)
        else:
            # labels at bin edges:
            set_labels(labels, minor=False)
            set_labels(["" for _ in range(size)], minor=True)

    ax.set_title(title)
    ax.set_aspect(1, adjustable='box')
    set_ticks('x', xlabels, counts.shape[0])
    set_ticks('y', ylabels, counts.shape[1])
    ax.grid(grid)

    max_radius = 0.9
    for (x, y), value in np.ndenumerate(counts / counts.max() * max_radius):
        if value > 0:
            draw_circle(
                ax, x + 0.5, y + 0.5,
                value ** 0.50 / 2,
                value ** 0.25)

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
