"""CSTATS

cstats provides statistic and information about your directories

Usage:
    cstats
    cstats (ls | list) [<path>]
    cstats (-h | --help)
    cstats --version

Options:
    -h --help  Show this screen.
    --version  Show version.

"""




# Usage:
#     cstats (ls | list) [<path>]
#     cstats (s | size) [<path>]

#     cstats -v | --version
#
# Options:
#




import sys as system
import time
import os

from docopt import docopt

__author__ = 'Miguel Velez - miguelvelezmj25'
__version__ = '0.2.0.1'

__cstats_version = 'cstats version "' + __version__ + '"\n' \
                                                      'author "' + __author__ + '"'


def _get_entry_info(path, entry):
    """
    Get information and attributes from the entry in the
    specified path.
    """

    # If the path ends with a '/'
    if path[-1:] == '/':
        # Remove the '/'
        path = path[:-1]

    # Try
    # try:
    #     # Get information and attributes from the entry in the path
    info = os.stat(path + '/' + entry)
    # except WindowsError:
    #     # The might be some windows error, so set the result to None
    #     info = None
    # Return the information
    return info


def list_files(path):
    """
    List the files and directories in the specified path.
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    # Sort the files by alphabetical order
    sorted(files)

    # Loop through each file
    for entry in files:
        # Get some file information
        file_info = _get_entry_info(path, entry)

        # If there is no file info
        if file_info is None:
            # Just jump to the next iteration of the loop
            continue

        # print str(file_info)

        # Print name, size, created time, modified time
        print entry.ljust(20),\
            'size: ' + str(file_info.st_size).ljust(10),\
            'modified: ' + time.ctime(file_info.st_mtime).ljust(30)
            # time.ctime(file_info.st_birthtime).ljust(30),\


def get_size_directory(path):
    """
    Get the size of the specified directory
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    # Variable for the total size
    total_size = 0

    # Loop through each file
    for entry in files:
        # Get the information of the file
        file_info = _get_entry_info(entry, path)

        # If there is no file info
        if file_info is None:
            # Just jump to the next iteration of the loop
            continue

        # Add the size of the current file to the total
        total_size += file_info.st_size

    # Print the total size of the current directory
    print 'Size of current directory: ' + str(total_size)

    # Return the total size
    return total_size


# Main method
def main():
    """
    Main Method of the cstats program.
    """

    # Get optional arguments for path
    args = system.argv[2:]
    # print 'Arguments: ' + str(args)

    # Get the arguments from docopt
    arguments = docopt(__doc__, version=__cstats_version)

    # print 'Docopt arguments: ' + str(arguments)

    # print '\n'

    # If the user wants to list the files
    if arguments['ls'] or arguments['list']:
        # If the user did not specify a path
        if len(args) == 0:
            # Pass the current path
            list_files('.')
        else:
            # Else, pass the path provided by the user
            list_files(args[0])
    else:
        # Print the man page
        print __doc__

    # # If the user wants the size of the directory
    # elif arguments['s'] or arguments['size']:
    #     if len(args) == 0:
    #         # Pass the current path
    #         get_size_directory('.')
    #     else:
    #         # Else, pass the path provided by the user
    #         get_size_directory(args[0])
    # else:


# Start the program
if __name__ == '__main__':
    # print 'All arguments ' + str(system.argv)
    main()
