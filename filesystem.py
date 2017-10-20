import os
import sys
import uuid
from os.path import exists
from os.path import join
from os.path import dirname
from os.path import splitext


def get_file_list_recursively(top_directory, allowed_extensions=[]):
    """
    Get list of full paths of all files found under root directory "top_directory".
    If a list of allowed file extensions is provided, files are filtered according to this list.
    
    Parameters
    ----------
    top_directory: str
        Root of the hierarchy
    allowed_extensions: list
        List of extensions to filter result

    Returns
    -------
    file_list: list
        List of files found under top_directory (with full path)
    """
    if not exists(top_directory):
        raise ValueError('Directory "{}" does NOT exist.'.format(top_directory))

    file_list = []

    for cur_dir, cur_subdirs, cur_files in os.walk(top_directory):

        for file in cur_files:

            f_name, f_ext = splitext(file)

            if f_ext:
                if allowed_extensions and f_ext not in allowed_extensions:
                    pass  # skip this file
                else:
                    file_list.append(join(cur_dir, file))
                    sys.stdout.write('\r[{}] - found {:06d} files...'.format(top_directory, len(file_list)))
                    sys.stdout.flush()
            else:
                pass  # todo decide what to do with files without extension

    sys.stdout.write(' Done.\n')

    return file_list


def give_unique_id_to_all_files_in_hierarchy(top_directory):
    """
    Rename with a unique identifier all the files in a directory hierarchy.
     
    Parameters
    ----------
    top_directory: str
        Root of the hierarchy

    Returns
    -------
    None
    """

    file_list = get_file_list_recursively(top_directory)

    for file_path in file_list:

        # Split path to maintain absolute path and extension
        file_dir    = dirname(file_path)
        _, file_ext = splitext(file_path)

        # Generate the new path with unique id
        file_uuid     = str(uuid.uuid4())
        file_new_path = join(file_dir, file_uuid + file_ext)

        os.rename(file_path, file_new_path)
