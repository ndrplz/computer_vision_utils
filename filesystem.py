import os
import sys
import os.path as path


def get_file_list_recursively(top_directory, allowed_extension=[]):
    """
    Get list of full paths of all files found under root directory "top_directory".
    If a list of allowed file extensions is provided, files are filtered according to this list.
	
    :param top_directory: root of the hirearchy
    :param allowed_extension: list of extensions to filter result
    :return: list of files found under top_directory (with full path)
    """
    if not path.exists(top_directory):
        raise ValueError('Directory "{}" does NOT exist.'.format(top_directory))

    file_list = []

    for cur_dir, cur_subdirs, cur_files in os.walk(top_directory):

        for file in cur_files:

            f_name, f_ext = path.splitext(file)

            if f_ext:
                if allowed_extension and f_ext not in allowed_extension:
                    pass  # skip this file
                else:
                    file_list.append(path.join(cur_dir, file))
                    sys.stdout.write('\r[{}] - currently found {:06d} files'.format(top_directory, len(file_list)))
                    sys.stdout.flush()
            else:
                pass  # todo decide what to do with files without extension

    return file_list