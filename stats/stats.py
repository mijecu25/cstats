r"""STATS

stats provides statistic and information about your directories

Usage:
    stats (ls | list) [<path>]
    stats -h | --help

Options:
  -h --help        Show this screen.
  --version     Show version.
"""

# Refer to http://docopt.org/ for documentation on how to structure the docopt

import sys as system
import os

from docopt import docopt

__author__ = 'Miguel Velez'
__version__ = '0.1.1'


def _list_files(path):
    """
    List the files and directories in the specified path
    """
    files = os.listdir(path)

    for entry in files:
        print entry


# Main method
def main(args):
    """
    Main Method of the stats program.
    """

    # Get the arguments from docopt
    arguments = docopt(__doc__, version=('stats ' + __version__))

    # If the user wants to list the files
    if arguments['ls'] or arguments['list']:
        # If the user did not specify a path
        if len(args) == 0:
            # Pass the current path
            _list_files('.')
        else:
            # Else, pass the path provided by the user
            _list_files(args[0])


# Start the program
if __name__ == '__main__':
    main(system.argv[2:])
