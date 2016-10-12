"""CSTATS

cstats provides statistic and information about your directories.

Usage:
    cst (ls | list) [<path>]
    cst (l | largest) [-r] [<path>]
    cst (s | size) [-r] [<path>]
    cst (c | count) [-r] [<path>]
    cst (t | type) [-r] [<path>]
    cst (e | extension) [-r] [<path>]
    cst (a | all) [-r] [<path>]
    cst (-h | --help)
    cst --version

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
__version__ = '0.2.1.4'

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

    tera_bytes = round(size / math.pow(10, 12), 3)

    if tera_bytes >= 0.1:
        formatted = str(tera_bytes) + ' TB'
        return formatted

    giga_bytes = round(size / math.pow(10, 9), 3)

    if giga_bytes >= 0.1:
        formatted = str(giga_bytes) + ' GB'
        return formatted

    mega_bytes = round(size / math.pow(10, 6), 3)

    if mega_bytes >= 0.1:
        formatted = str(mega_bytes) + ' MB'
        return formatted

    kilo_bytes = round(size / math.pow(10, 3), 3)

    if kilo_bytes >= 0.1:
        formatted = str(kilo_bytes) + ' kB'
        return formatted

    formatted = str(round(size, 3)) + ' bytes'
    return formatted


def _get_entry_info(path, entry):
    """
    Get information and attributes from the entry in the
    specified path.
    """

    if path[-1:] != '/':
        path += '/'

    info = os.stat(path + entry)

    return info


def _remove_directory_slash(path):
    """
    Remove the '/' at the end of the path if present.

    :param path:
    :return:
    """

    if path[-1:] == '/':
        path = path[:-1]

    return path


def list_files(path):
    """
    List the files and directories in the specified path.
    :param path:
    """

    files = os.listdir(path)
    sorted(files)

    print 'Total files ' + str(len(files))

    for entry in files:
        file_info = _get_entry_info(path, entry)

        if file_info is None:
            continue

        print entry.ljust(50), 'size ' + str(file_info.st_size).ljust(10), \
            'modified ' + time.ctime(file_info.st_mtime).ljust(35)


def get_size_directory(path, recursive=False):
    """
    Get the size of the specified directory. The default is to do a non recursive execution. This means that
    the size of the folders represent the size that they take in memory and the contents are not included. If you want
    the contents of directories to be included in the analysis, set the recursive paramater to True.

    :param recursive:
    :param path:
    """

    path = _remove_directory_slash(path)
    paths = Queue.Queue()
    paths.put(path)
    total_size = 0

    while not paths.empty():
        current_path = paths.get()
        files = os.listdir(current_path)

        for entry in files:
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                paths.put(current_path + '/' + entry)
                continue

            file_info = _get_entry_info(current_path, entry)

            if file_info is None:
                continue

            total_size += file_info.st_size

    print 'Size of current directory ' + _format_size(total_size)

    return total_size


def get_file_types(path, recursive=False):
    """
    Get a list of the file types of the specified directory

    :param recursive:
    :param path:
    """

    path = _remove_directory_slash(path)
    paths = Queue.Queue()
    paths.put(path)
    current_file_types = {'Other': 0, 'Folders': 0}

    while not paths.empty():
        current_path = paths.get()
        files = os.listdir(current_path)

        for entry in files:
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                paths.put(current_path + '/' + entry)

            file_extension = entry.split('.')
            not_found = True

            if not os.path.isdir(os.path.join(current_path, entry)):
                if len(file_extension) == 1:
                    current_file_types['Other'] += 1
                else:
                    for file_type in __file_types:
                        if file_extension[-1].lower() in __file_types[file_type]:
                            if file_type in current_file_types:
                                current_file_types[file_type] += 1
                            else:
                                current_file_types[file_type] = 1

                            not_found = False
                            break

                    if not_found:
                        current_file_types['Other'] += 1
            else:
                current_file_types['Folders'] += 1

    sorted_types = sorted(current_file_types.items(), key=operator.itemgetter(1), reverse=True)

    for file_type in sorted_types:
        if file_type[1] > 0:
            print file_type[0] + ' ' + str(file_type[1])

    return current_file_types


def get_extension_usage(path, recursive=False):
    """
    Get a list of the number of times an extension has been used

    :param recursive:
    :param path:
    """

    path = _remove_directory_slash(path)
    paths = Queue.Queue()
    paths.put(path)
    extension_count = {}

    while not paths.empty():
        current_path = paths.get()
        files = os.listdir(current_path)

        for entry in files:
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                paths.put(current_path + '/' + entry)
                continue

            file_extension = entry.split('.')

            if len(file_extension) == 1:
                continue

            if file_extension[-1].lower() in extension_count:
                extension_count[file_extension[-1].lower()] += 1
            else:
                extension_count[file_extension[-1].lower()] = 1

    sorted_extensions = sorted(extension_count.items(), key=operator.itemgetter(1), reverse=True)

    for extension in sorted_extensions:
        print '.' + extension[0] + ' ' + str(extension[1])

    return extension_count


def get_directory_count(path, recursive=False):
    """
    Get the count of the number of files and directories in the specified directory. The default is to do a non
    recursive execution. This means that the content of the directories is no included in the analysis. If you want
    the contents of directories to be included in the analysis, set the recursive paramater to True.

    :param recursive:
    :param path:
    """

    path = _remove_directory_slash(path)
    paths = Queue.Queue()
    paths.put(path)
    total_count = {'Directories': 0, 'Files': 0}

    while not paths.empty():
        current_path = paths.get()
        files = os.listdir(current_path)

        for entry in files:
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                paths.put(current_path + '/' + entry)

            if os.path.isdir(os.path.join(current_path, entry)):
                total_count['Directories'] += 1
            else:
                total_count['Files'] += 1

    sorted_count = sorted(total_count.items(), key=operator.itemgetter(1), reverse=True)

    for directory_count in sorted_count:
        print directory_count[0] + ' ' + str(directory_count[1])

    return total_count


def get_largest_file(path, recursive=False):
    """
    :param recursive:
    :param path:
    :return:
    """

    path = _remove_directory_slash(path)

    paths = Queue.Queue()
    paths.put(path)
    largest_path = ''
    largest_name = ''
    largest_size = 0

    while not paths.empty():
        current_path = paths.get()

        files = os.listdir(current_path)

        for entry in files:
            if recursive and os.path.isdir(os.path.join(current_path, entry)):
                paths.put(current_path + '/' + entry)
                continue

            file_info = _get_entry_info(current_path, entry)

            if file_info.st_size > largest_size:
                largest_size = file_info.st_size
                largest_name = entry
                largest_path = current_path

    if largest_size == 0:
        print 'The directory you specified only has directories'

        return

    print 'Largest file \"' + str(largest_name) + '\"'
    print 'Size ' + _format_size(largest_size)
    print 'Path ' + str(largest_path + '/')


def _list_analysis(args):
    """
    Run the list analysis.

    :param args:
    :return:
    """

    if len(args) == 0:
        list_files('.')
    else:
        list_files(args[-1])


def _size_analysis(args, docopt_arguments):
    """
    Run the size analysis.

    :param args:
    :param docopt_arguments:
    :return:
    """
    if docopt_arguments['-r']:
        if len(args) == 1:
            get_size_directory('.', True)
        else:
            get_size_directory(args[1], True)
    else:
        if len(args) == 0:
            get_size_directory('.')
        else:
            get_size_directory(args[0])


def _type_analysis(args, docopt_arguments):
    """
    Run the type analysis.

    :param args:
    :param docopt_arguments:
    :return:
    """
    if docopt_arguments['-r']:
        if len(args) == 1:
            get_file_types('.', True)
        else:
            get_file_types(args[1], True)
    else:
        if len(args) == 0:
            get_file_types('.')
        else:
            get_file_types(args[0])


def _count_analysis(args, docopt_arguments):
    """
    Run the count analysis.

    :param args:
    :param docopt_arguments:
    :return:
    """
    if docopt_arguments['-r']:
        if len(args) == 1:
            get_directory_count('.', True)
        else:
            get_directory_count(args[1], True)
    else:
        if len(args) == 0:
            get_directory_count('.')
        else:
            get_directory_count(args[0])


def _largest_analysis(args, docopt_arguments):
    """
    Run the largest analysis

    :param args:
    :param docopt_arguments:
    :return:
    """

    if docopt_arguments['-r']:
        if len(args) == 1:
            get_largest_file('.', True)
        else:
            get_largest_file(args[1], True)
    else:
        if len(args) == 0:
            get_largest_file('.')
        else:
            get_largest_file(args[0])


def _extension_analysis(args, docopt_arguments):
    """
    Run the extension analysis

    :param args:
    :param docopt_arguments:
    :return:
    """

    if docopt_arguments['-r']:
        if len(args) == 1:
            get_extension_usage('.', True)
        else:
            get_extension_usage(args[1], True)
    else:
        if len(args) == 0:
            get_extension_usage('.')
        else:
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


def main():
    """
    Main Method of the cstats program.
    """

    args = system.argv[2:]
    docopt_arguments = docopt(__doc__, version=__cstats_version)

    print 'cstats started analyzing on ' + time.strftime("%c") + '\n'
    start_time = time.time()

    if docopt_arguments['ls'] or docopt_arguments['list']:
        _list_analysis(args)
    elif docopt_arguments['a'] or docopt_arguments['all']:
        _all_analysis(args, docopt_arguments)
    elif docopt_arguments['s'] or docopt_arguments['size']:
        _size_analysis(args, docopt_arguments)
    elif docopt_arguments['e'] or docopt_arguments['extension']:
        _extension_analysis(args, docopt_arguments)
    elif docopt_arguments['t'] or docopt_arguments['type']:
        _type_analysis(args, docopt_arguments)
    elif docopt_arguments['c'] or docopt_arguments['count']:
        _count_analysis(args, docopt_arguments)
    elif docopt_arguments['l'] or docopt_arguments['largest']:
        _largest_analysis(args, docopt_arguments)
    else:
        print __doc__

    end_time = time.time()

    print '\nExecution took ' + str(round(end_time - start_time, 4)) + ' seconds'


if __name__ == '__main__':
    main()
