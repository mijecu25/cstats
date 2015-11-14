"""CSTATS

cstats provides statistic and information about your directories.

Usage:
    cstats (ls | list) [<path>]
    cstats (l | largest) [-r] [<path>]
    cstats (s | size) [-r] [<path>]
    cstats (c | count) [-r] [<path>]
    cstats (t | type) [-r] [<path>]
    cstats (e | extension) [-r] [<path>]
    cstats (a | all) [-r] [<path>]
    cstats (-h | --help)
    cstats --version

Options:
    -r  Recursive call. Used to apply the command to the directories of the path
    -h --help  Show this screen.
    --version  Show version.

"""

import sys as system
import time
import os
import operator
import Queue
import math

from docopt import docopt

__author__ = 'Miguel Velez - miguelvelezmj25'
__version__ = '0.2.1.1'

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


def _format_size(size):
    """
    Format the size value to correct unit in kB, MB, GB, or TB.

    :param value:
    :return:
    """

    # Check how many terabytes there are
    tera_bytes = round(size / math.pow(10, 12), 3)

    # If there are terabytes
    if tera_bytes >= 0.1:
        formatted = str(tera_bytes) + ' TB'
        return formatted

    # Check how many gigabytes there are
    giga_bytes = round(size / math.pow(10, 9), 3)

    # If there are gigabytes
    if giga_bytes >= 0.1:
        formatted = str(giga_bytes) + ' GB'
        return formatted

    # Check how many megabytes there are
    mega_bytes = round(size / math.pow(10, 6), 3)

    # If there are megabytes
    if mega_bytes >= 0.1:
        formatted = str(mega_bytes) + ' MB'
        return formatted

    # Check how many kilobytes there are
    kilo_bytes = round(size / math.pow(10, 9), 3)

    # If there are kilobytes
    if kilo_bytes >= 0.1:
        formatted = str(kilo_bytes) + ' kB'
        return formatted

    # There are less than kilobyte. Return just the value
    formatted = str(round(size, 3)) + ' bytes'
    return formatted


def _get_entry_info(path, entry):
    """
    Get information and attributes from the entry in the
    specified path.
    """

    # If the path does not end with a '/'
    if path[-1:] != '/':
        # Add the '/'
        path += '/'

    # Get information and attributes from the entry in the path
    info = os.stat(path + entry)

    # Return the information
    return info


def _remove_directory_slash(path):
    """
    Remove the '/' at the end of the path if present.

    :param path:
    :return:
    """

    # If the path ends with a '/'
    if path[-1:] == '/':
        # Remove the '/'
        path = path[:-1]

    # Return the path
    return path


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
        print entry.ljust(50),\
            'size ' + str(file_info.st_size).ljust(10),\
            'modified ' + time.ctime(file_info.st_mtime).ljust(50)


def get_size_directory(path, recursive=False):
    """
    Get the size of the specified directory. The default is to do a non recursive execution. This means that
    the size of the folders represent the size that they take in memory and the contents are not included. If you want
    the contents of directories to be included in the analysis, set the recursive paramater to True.

    :param recursive:
    :param path:
    """

    # Remove the '/' from the end of the path if present
    path = _remove_directory_slash(path)

    # Create a new queue of paths
    paths = Queue.Queue()
    # Add the passed path
    paths.put(path)

    # Variable for the total size
    total_size = 0

    # While there are more paths to analyze
    while not paths.empty():
        # Get the current path
        current_path = paths.get()

        # Get the files and directories in the path
        files = os.listdir(current_path)

        # Loop through each file
        for entry in files:
            # If we are doing a recursive call and the current entry is a directory
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                # Put the new path in the paths queue
                paths.put(current_path + '/' + entry)
                # Continue to the next iteration of the loop
                continue

            # Get the information of the file
            file_info = _get_entry_info(current_path, entry)

            # If there is no file info
            if file_info is None:
                # Just jump to the next iteration of the loop
                continue

            # Add the size of the current file to the total
            total_size += file_info.st_size

    # Print the total size of the current directory
    print 'Size of current directory ' + _format_size(total_size)

    # Return the total size
    return total_size


def get_file_types(path, recursive=False):
    """
    Get a list of the file types of the specified directory

    :param recursive:
    :param path:
    """

    # Remove the '/' from the end of the path if present
    path = _remove_directory_slash(path)

    # Create a new queue of paths
    paths = Queue.Queue()
    # Add the passed path
    paths.put(path)

    # The dictionary with the counts of the file types
    current_file_types = {'Other': 0, 'Folders': 0}

    # While there are more paths to analyze
    while not paths.empty():
        # Get the current path
        current_path = paths.get()

        # Get the files and directories in the path
        files = os.listdir(current_path)

        # Loop through each file
        for entry in files:
            # If we are doing a recursive call and the current entry is a directory
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                # Put the new path in the paths queue
                paths.put(current_path + '/' + entry)

            # Split each file and extension
            file_extension = entry.split('.')

            # Variable to check if we added to an existing type
            not_found = True

            # If the file is not a directory
            if not os.path.isdir(os.path.join(current_path, entry)):
                # If the file does not have an extension
                if len(file_extension) == 1:
                    # The file is of type other
                    current_file_types['Other'] += 1
                else:
                    # For each file type in the map of existing types
                    for file_type in __file_types:
                        # If the file extensions is part of one of the current types
                        if file_extension[-1].lower() in __file_types[file_type]:
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


def get_extension_usage(path, recursive=False):
    """
    Get a list of the number of times an extension has been used

    :param recursive:
    :param path:
    """

    # Remove the '/' from the end of the path if present
    path = _remove_directory_slash(path)

    # Create a new queue of paths
    paths = Queue.Queue()
    # Add the passed path
    paths.put(path)

    # The dictionary with the counts of the extensions
    extension_count = {}

    # While there are more paths to analyze
    while not paths.empty():
        # Get the current path
        current_path = paths.get()

        # Get the files and directories in the path
        files = os.listdir(current_path)

        # Loop through each file
        for entry in files:
            # If we are doing a recursive call and the current entry is a directory
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                # Put the new path in the paths queue
                paths.put(current_path + '/' + entry)
                # Continue to the next iteration of the loop
                continue

            # Split each file and extension
            file_extension = entry.split('.')

            # If the file does not have an extension
            if len(file_extension) == 1:
                # Continue to the next iteration of the loop
                continue

            # If there is already a count for the extension
            if file_extension[-1].lower() in extension_count:
                # Increment the count by 1
                extension_count[file_extension[-1].lower()] += 1
            else:
                # Create a new entry with the first element
                extension_count[file_extension[-1].lower()] = 1

    # Sort the values in the map based on the counter in reverse order
    sorted_extensions = sorted(extension_count.items(), key=operator.itemgetter(1), reverse=True)

    # For each file type in the extension
    for extension in sorted_extensions:
        # Print the extension and count
        print '.' + extension[0] + ' ' + str(extension[1])

    # Return the map of all of the extensions and counters
    return extension_count


def get_directory_count(path, recursive=False):
    """
    Get the count of the number of files and directories in the specified directory. The default is to do a non
    recursive execution. This means that the content of the directories is no included in the analysis. If you want
    the contents of directories to be included in the analysis, set the recursive paramater to True.

    :param recursive:
    :param path:
    """

    # Remove the '/' from the end of the path if present
    path = _remove_directory_slash(path)

    # Create a new queue of paths
    paths = Queue.Queue()
    # Add the passed path
    paths.put(path)

    # Variable for the total count
    total_count = {'Directories': 0, 'Files': 0}

    # While there are more paths to analyze
    while not paths.empty():
        # Get the current path
        current_path = paths.get()

        # Get the files and directories in the path
        files = os.listdir(current_path)

        # Loop through each file
        for entry in files:
            # If we are doing a recursive call and the current entry is a directory
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                # Put the new path in the paths queue
                paths.put(current_path + '/' + entry)

            # If the entry is a directory
            if os.path.isdir(os.path.join(current_path, entry)):
                total_count['Directories'] += 1
            else:
                total_count['Files'] += 1

    # Sort the values in the map based on the counter in reverse order
    sorted_count = sorted(total_count.items(), key=operator.itemgetter(1), reverse=True)

    # For each entry
    for directory_count in sorted_count:
        # Print the type and count
        print directory_count[0] + ' ' + str(directory_count[1])

    # Return the total count of directories and files
    return total_count


def get_largest_file(path, recursive=False):
    """

    :param recursive:
    :param path:
    :return:
    """

    # Remove the '/' from the end of the path if present
    path = _remove_directory_slash(path)

    # Create a new queue of paths
    paths = Queue.Queue()
    # Add the passed path
    paths.put(path)

    # Variables to keep track of the largest file
    largest_path = ''
    largest_name = ''
    largest_size = 0

    # While there are more paths to analyze
    while not paths.empty():
        # Get the current path
        current_path = paths.get()

        # Get the files and directories in the path
        files = os.listdir(current_path)

        # Loop through each file
        for entry in files:
            # If we are doing a recursive call and the current entry is a directory
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                # Put the new path in the paths queue
                paths.put(current_path + '/' + entry)
                # Continue to the next iteration of the loop
                continue

            # Get some file information
            file_info = _get_entry_info(current_path, entry)

            # If the size of the current file is larger than the largest
            if file_info.st_size > largest_size:
                # Get the size
                largest_size = file_info.st_size
                # Get the name
                largest_name = entry
                # Get the path
                largest_path = current_path

    # If there is no file in the directory
    if largest_size == 0:
        print 'The directory you specified only has directories'

        return

    # Print the information about the largest file
    print 'Largest file \"' + str(largest_name) + '\"'
    print 'Size ' + _format_size(largest_size)
    print 'Path ' + str(largest_path + '/')


def _list_analysis(args):
    """
    Run the list analysis.

    :param args:
    :return:
    """

    # If the user did not specify a path
    if len(args) == 0:
        # Pass the current path
        list_files('.')
    else:
        # Else, pass the path provided by the user
        list_files(args[-1])


def _size_analysis(args, docopt_arguments):
    """
    Run the size analysis.

    :param args:
    :param docopt_arguments:
    :return:
    """
    # If this is a recursive command
    if docopt_arguments['-r']:
        # If there are not arguments
        if len(args) == 1:
            # Pass the current path
            get_size_directory('.', True)
        else:
            # Else, pass the path provided by the user
            get_size_directory(args[1], True)
    else:
        # If there are not arguments
        if len(args) == 0:
            # Pass the current path
            get_size_directory('.')
        else:
            # Else, pass the path provided by the user
            get_size_directory(args[0])


def _type_analysis(args, docopt_arguments):
    """
    Run the type analysis.

    :param args:
    :param docopt_arguments:
    :return:
    """
    # If this is a recursive command
    if docopt_arguments['-r']:
        # If there are not arguments
        if len(args) == 1:
            # Pass the current path
            get_file_types('.', True)
        else:
            # Else, pass the path provided by the user
            get_file_types(args[1], True)
    else:
        # If there are not arguments
        if len(args) == 0:
            # Pass the current path
            get_file_types('.')
        else:
            # Else, pass the path provided by the user
            get_file_types(args[0])


def _count_analysis(args, docopt_arguments):
    """
    Run the count analysis.

    :param args:
    :param docopt_arguments:
    :return:
    """
    # If this is a recursive command
    if docopt_arguments['-r']:
        # If there are not arguments
        if len(args) == 1:
            # Pass the current path
            get_directory_count('.', True)
        else:
            # Else, pass the path provided by the user
            get_directory_count(args[1], True)
    else:
        # If there are not arguments
        if len(args) == 0:
            # Pass the current path
            get_directory_count('.')
        else:
            # Else, pass the path provided by the user
            get_directory_count(args[0])


def _largest_analysis(args, docopt_arguments):
    """
    Run the largest analysis

    :param args:
    :param docopt_arguments:
    :return:
    """

    # If this is a recursive command
    if docopt_arguments['-r']:
        # If there are not arguments
        if len(args) == 1:
            # Pass the current path
            get_largest_file('.', True)
        else:
            # Else, pass the path provided by the user
            get_largest_file(args[1], True)
    else:
        # If there are not arguments
        if len(args) == 0:
            # Pass the current path
            get_largest_file('.')
        else:
            # Else, pass the path provided by the user
            get_largest_file(args[0])


def _extension_analysis(args, docopt_arguments):
    """
    Run the extension analysis

    :param args:
    :param docopt_arguments:
    :return:
    """

    # If this is a recursive command
    if docopt_arguments['-r']:
        # If there are not arguments
        if len(args) == 1:
            # Pass the current path
            get_extension_usage('.', True)
        else:
            # Else, pass the path provided by the user
            get_extension_usage(args[1], True)
    else:
        # If there are not arguments
        if len(args) == 0:
            # Pass the current path
            get_extension_usage('.')
        else:
            # Else, pass the path provided by the user
            get_extension_usage(args[0])


def _all_analysis(args, docopt_arguments):
    """
    Run all analyses

    :param args:
    :param docopt_arguments:
    :return:
    """

    print 35 * '=' + ' ls - list ' + 35 * '='
    if docopt_arguments['-r']:
        _list_analysis(args[1:])
    else:
        _list_analysis(args)

    print '\n' + 35 * '=' + ' l - largest ' + 35 * '='
    _largest_analysis(args, docopt_arguments)

    print '\n' + 35 * '=' + ' s - size ' + 35 * '='
    _size_analysis(args, docopt_arguments)

    print '\n' + 35 * '=' + ' c - count ' + 35 * '='
    _count_analysis(args, docopt_arguments)

    print '\n' + 35 * '=' + ' t - type ' + 35 * '='
    _type_analysis(args, docopt_arguments)

    print '\n' + 35 * '=' + ' e - extension ' + 35 * '='
    _extension_analysis(args, docopt_arguments)


# Main method
def main():
    """
    Main Method of the cstats program.
    """

    # Get optional arguments for path
    args = system.argv[2:]

    # Get the arguments from docopt
    docopt_arguments = docopt(__doc__, version=__cstats_version)

    print 'cstats started analyzing on ' + time.strftime("%c") + '\n'
    start_time = time.time()

    # If the user wants to list the files
    if docopt_arguments['ls'] or docopt_arguments['list']:
        _list_analysis(args)
    # If the user wants to run a full analysis of the directory
    elif docopt_arguments['a'] or docopt_arguments['all']:
        _all_analysis(args, docopt_arguments)
    # If the user wants the size of the directory
    elif docopt_arguments['s'] or docopt_arguments['size']:
        _size_analysis(args, docopt_arguments)
    # If the user wants a list of the extensions in the directory
    elif docopt_arguments['e'] or docopt_arguments['extension']:
        _extension_analysis(args, docopt_arguments)
    # If the user wants a list of the types of files of the directory
    elif docopt_arguments['t'] or docopt_arguments['type']:
        _type_analysis(args, docopt_arguments)
    # If the user wants to count the directories and files inside a directory
    elif docopt_arguments['c'] or docopt_arguments['count']:
        _count_analysis(args, docopt_arguments)
    # If the user wants the largest file in the directory
    elif docopt_arguments['l'] or docopt_arguments['largest']:
        _largest_analysis(args, docopt_arguments)
    else:
        # Print the man page
        print __doc__

    end_time = time.time()

    print '\nExecution took ' + str(round(end_time - start_time, 4)) + ' seconds'

# Start the program
if __name__ == '__main__':
    # print 'All arguments ' + str(system.argv)
    main()
