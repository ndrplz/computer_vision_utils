import os
import sys
import os.path as path


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
    if not path.exists(top_directory):
        raise ValueError('Directory "{}" does NOT exist.'.format(top_directory))

    file_list = []

    for cur_dir, cur_subdirs, cur_files in os.walk(top_directory):

        for file in cur_files:

            f_name, f_ext = path.splitext(file)

            if f_ext:
                if allowed_extensions and f_ext not in allowed_extensions:
                    pass  # skip this file
                else:
                    file_list.append(path.join(cur_dir, file))
                    sys.stdout.write('\r[{}] - found {:06d} files...'.format(top_directory, len(file_list)))
                    sys.stdout.flush()
            else:
                pass  # todo decide what to do with files without extension

    sys.stdout.write(' Done.\n')

    return file_list
