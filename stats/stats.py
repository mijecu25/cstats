r"""STATS

stats provides statistic and information about your directories

Usage:
    stats (ls | list) [<path>]
    stats -h | --help
    stats -s | --size

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Refer to http://docopt.org/ for documentation on how to structure the docopt

import sys as system
import time
import os

from docopt import docopt

__author__ = 'Miguel Velez'
__version__ = '0.1.2.2'


def _get_entry_info(entry):
    return os.stat(entry)


def list_files(path):
    """
    List the files and directories in the specified path
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    # Sort the files by alphabetical order
    sorted(files)

    # Print the files
    for entry in files:
        # Get some file information
        # try:
            file_info = _get_entry_info(entry)

            print entry.ljust(20),\
                str(file_info.st_size).ljust(10),\
                time.ctime(file_info.st_ctime).ljust(30),\
                time.ctime(file_info.st_mtime).ljust(30)

        # except WindowsError:
        #     print 'Could not find ', entry


def get_size_directory(path):
    """
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    total_size = 0

    for entry in files:
        file_info = _get_entry_info(entry)

        total_size += file_info.st_size

    print 'Size of current directory: ' + str(total_size)


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
            list_files('.')
        else:
            # Else, pass the path provided by the user
            list_files(args[0])

    # If the user wants the size of the directory
    elif arguments['-s'] or arguments['--size']:
        # Pass the current path
        get_size_directory('.')


# Start the program
if __name__ == '__main__':
    main(system.argv[2:])
