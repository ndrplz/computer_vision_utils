from __future__ import print_function
import glob
import os
import os.path as path
import pickle
import sys
from sklearn.utils import shuffle


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


def dump_list(input_list, file_path):
    """
    Dump list to file, either in "txt" or binary ("pickle") mode.
    Dump mode is chosen accordingly to "file_path" extension.

    :param input_list: list object to dump
    :param file_path: path of the dump file
    :return: None
    """
    f_name, f_ext = path.splitext(file_path)

    if f_ext != '.txt' and f_ext != '.pickle':
        raise ValueError('File extension not supported. Allowed: {".txt", ".pickle"}. Provided: "{}"'.format(f_ext))

    with open(file_path, 'wb') as f:
        if f_ext == '.txt':
            for str in input_list:
                f.write('{}\n'.format(str))
        else:
            pickle.dump(input_list, f)


def load_list(file_path):
    """
    Load list from file, either in "txt" or binary ("pickle") mode.
    Load mode is chosen accordingly to "file_path" extension.

    :param file_path: dump file
    :return: list object
    """
    if not path.exists(file_path):
        raise IOError('File "{}" does not exist.'.format(file_path))

    f_name, f_ext = path.splitext(file_path)

    file_list = []

    with open(file_path, 'rb') as f:
        if f_ext == '.txt':
            for line in f:
                file_list.append(line.strip())  # remove trailing newline
        elif f_ext == '.pickle':
            file_list = pickle.load(f)
        else:
            raise ValueError('File extension not supported. Allowed: {".txt", ".pickle"}. Provided: "{}"'.format(f_ext))

    return file_list


def split_list_into_pieces(file_path, max_elements, output_dir, shuffle_list=False):
    """
    Split a file containing a list into a variable number of chunks of at most "max_elements" each.

    :param file_path: file containing the input list
    :param max_elements: max elements allowed into each chunk
    :param output_dir: output directories in which each chunk is dumped
    :param shuffle_list: if True, input list is shuffled before chunking
    :return: None
    """
    if not path.exists(output_dir):
        os.makedirs(output_dir)

    list_full = load_list(file_path)

    file_path, ext = path.splitext(file_path)
    file_path, file_name = path.split(file_path)

    if shuffle_list:
        list_full = shuffle(list_full)

    counter = 0
    for offset in range(0, len(list_full), max_elements):
        list_chunk = list_full[offset:offset + max_elements]
        dump_list(list_chunk, path.join(output_dir, '{}_{:06d}{}'.format(file_name, counter, ext)))
        counter += 1


if __name__ == '__main__':

    mylist = ['a', 'b', 'c', 'd', 'e']

    dump_list(mylist, 'prova.txt')
    dump_list(mylist, 'prova.pickle')

    mylist = load_list('prova.txt')
    mylist = load_list('prova.pickle')

    split_list_into_pieces('prova.txt', max_elements=2, output_dir='.', shuffle_list=True)
    split_list_into_pieces('prova.pickle', max_elements=2, output_dir='.', shuffle_list=True)

    for i in range(0, 3):
        print(load_list('prova_{:06d}.txt'.format(i)))
        print(load_list('prova_{:06d}.pickle'.format(i)))
