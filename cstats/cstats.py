"""CSTATS

cstats provides statistic and information about your directories

Usage:
    cstats (ls | list) [<path>]
    cstats (s | size) [<path>]
    cstats (t | type) [<path>]
    cstats (-h | --help)
    cstats --version

Options:
    -h --help  Show this screen.
    --version  Show version.

"""

import sys as system
import time
import os
import operator

from docopt import docopt

__author__ = 'Miguel Velez - miguelvelezmj25'
__version__ = '0.2.0.3'

__cstats_version = 'cstats version "' + __version__ + '"\n' \
                                                      'author "' + __author__ + '"'
__music_extensions = {'3gp', 'act', 'aiff', 'aac', 'amr', 'ape', 'au', 'awb', 'dct', 'dss', 'dvf', 'flac', 'gsm',
                      'iklax', 'ivs', 'm4a', 'm4p', 'mmf', 'mp3', 'mpc', 'msv', 'ogg', 'oga', 'opus', 'ra', 'rm',
                      'raw', 'sln', 'tta', 'vox', 'wav', 'wma', 'wv', 'webm'}
__photo_extensions = {'tif', 'tiff', 'gif', 'jpeg', 'jpg', 'jif', 'jfif', 'jp2', 'jpx', 'j2k', 'j2c', 'fpx', 'pcd',
                      'png'}
__document_extensions = {'pdf', 'doc', 'docx', 'log', 'msg', 'odt', 'pages', 'rtf', 'tex', 'txt', 'wpd', 'wps', 'csv',
                         'dat', 'gbr', 'ged', 'key', 'keychain', 'pps', 'ppt', 'pptx', 'sdf', 'tar', 'vcf', 'xml',
                         'xlr', 'xls', 'xlsx', 'db', 'dbf', 'mdb', 'pdb', 'sql', 'apk', 'jar', 'asp', 'aspx', 'cer',
                         'cfm', 'csr', 'css', 'htm', 'html', 'js', 'jsp', 'php', 'rss', 'xhtml', '7z', 'cbr', 'deb',
                         'gz', 'pkg', 'rar', 'rpm', 'sitx', 'tar.gz', 'zip', 'zipx', 'c', 'class', 'cpp', 'cs', 'dtd',
                         'fla', 'h', 'java', 'lua', 'm', 'pl', 'py', 'sh', 'sln', 'swift', 'vcxproj', 'xcodeproj'}
__video_extensions = {'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'drc', 'gif', 'gifv', 'mng', 'avi', 'mov', 'qt',
                      'wmv', 'yuv', 'rm', 'rmvb', 'asf', 'mp4', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', '.mpg',
                      'mpeg,' 'm2v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b'}
__file_types = {'Music': __music_extensions, 'Photos': __photo_extensions, 'Documents': __document_extensions, 'Videos':
                __video_extensions}


def _get_entry_info(path, entry):
    """
    Get information and attributes from the entry in the
    specified path.
    """

    # If the path ends with a '/'
    if path[-1:] == '/':
        # Remove the '/'
        path = path[:-1]

    # Get information and attributes from the entry in the path
    info = os.stat(path + '/' + entry)

    # Return the information
    return info


def list_files(path):
    """
    List the files and directories in the specified path.
    :param path:
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    # Sort the files by alphabetical order
    sorted(files)

    print 'Total files ' + str(len(files))

    # Loop through each file
    for entry in files:
        # Get some file information
        file_info = _get_entry_info(path, entry)

        # If there is no file info
        if file_info is None:
            # Just jump to the next iteration of the loop
            continue

        # Print name, size, created time, modified time
        print entry.ljust(20),\
            'size ' + str(file_info.st_size).ljust(10),\
            'modified ' + time.ctime(file_info.st_mtime).ljust(50)


def get_size_directory(path):
    """
    Get the size of the specified directory
    :param path:
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    # Variable for the total size
    total_size = 0

    # Loop through each file
    for entry in files:
        # Get the information of the file
        file_info = _get_entry_info(path, entry)

        # If there is no file info
        if file_info is None:
            # Just jump to the next iteration of the loop
            continue

        # Add the size of the current file to the total
        total_size += file_info.st_size

    # Print the total size of the current directory
    print 'Size of current directory ' + str(total_size) + ' bytes'

    # Return the total size
    return total_size


def get_file_types(path):
    """
    Get a list of the file types of the specified directory
    :param path:
    """

    # Get the files and directories in the path
    files = os.listdir(path)

    # The dictionary with the counts of the file types
    current_file_types = {'Other': 0, 'Folders': 0}

    # Loop through each file
    for entry in files:
        # Split each file and extension
        file_extension = entry.split('.')

        # Variable to check if we added to an existing type
        not_found = True

        # If the file has a name and extension or it begins with a dot
        if len(file_extension) == 2 or entry[0] == '.':
            # For each file type in the map of existing types
            for file_type in __file_types:
                # If the file extensions is part of one of the current types
                if file_extension[1] in __file_types[file_type]:
                    # If there is already a count for the file type
                    if file_type in current_file_types:
                        # Increment the count by 1
                        current_file_types[file_type] += 1
                    else:
                        # Create a new entry with the first element
                        current_file_types[file_type] = 1

                    # Since we increased the count, we found something
                    not_found = False
                    # Do not keep searching in other file types
                    break

            # If we did not find anything associated to the file extension
            if not_found:
                # The file is of type other
                current_file_types['Other'] += 1
        else:
            # The current entry is a folder
            current_file_types['Folders'] += 1

    # Sort the values in the map based on the counter in reverse order
    sorted_types = sorted(current_file_types.items(), key=operator.itemgetter(1), reverse=True)

    # For each file type in the file types
    for file_type in sorted_types:
        # If we found at least one element of this type
        if file_type[1] > 0:
            # Print the type and count
            print file_type[0] + ' ' + str(file_type[1])

    # Return the map of all of the types and counters
    return current_file_types


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
    # If the user wants the size of the directory
    elif arguments['s'] or arguments['size']:
        if len(args) == 0:
            # Pass the current path
            get_size_directory('.')
        else:
            # Else, pass the path provided by the user
            get_size_directory(args[0])
    # If the user wants alits of the types of files of the directory
    elif arguments['t'] or arguments['type']:
        if len(args) == 0:
            # Pass the current path
            get_file_types('.')
        else:
            # Else, pass the path provided by the user
            get_file_types(args[0])
    else:
        # Print the man page
        print __doc__


# Start the program
if __name__ == '__main__':
    # print 'All arguments ' + str(system.argv)
    main()
