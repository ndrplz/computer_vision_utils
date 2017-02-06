from __future__ import print_function
import glob
import os
import os.path as path
import pickle
import sys
from sklearn.utils import shuffle


def get_file_list_recursively(top_directory, allowed_extension=[]):

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


def dump_list_to_txt(list, filepath):

    with open(filepath, 'wb') as f:
        for str in list:
            f.write('{}\n'.format(str))


def load_list(filepath):

    if not path.exists(filepath):
        raise IOError('File "{}" not found.'.format(filepath))

    f_name, f_ext = path.splitext(filepath)

    file_list = []

    if f_ext == '.txt':
        with open(filepath, 'rb') as f:
            for line in f:
                file_list.append(line.strip())  # remove trailing newline
    elif f_ext == '.pickle':
        with open(filepath, 'rb') as f:
            file_list = pickle.load(f)
    else:
        raise ValueError('Unable to handle files with extension: "{}"'.format(f_ext))

    return file_list


def split_list_into_pieces(file_path, max_len, output_dir, shuffle_list=False):
    """
    Split list into N pieces of "max_len" elements each
    :param file_path:
    :param max_len:
    :param output_dir:
    :param shuffle_list:
    :return:
    """
    if not path.exists(output_dir):
        os.makedirs(output_dir)

    list_full = load_list(file_path)

    file_path, ext = path.splitext(file_path)
    file_path, file_name = path.split(file_path)

    if shuffle_list:
        list_full = shuffle(list_full)

    counter = 0
    for offset in range(0, len(list_full), max_len):
        counter += 1
        list_chunk = list_full[offset:offset + max_len]
        dump_list_to_txt(list_chunk, path.join(output_dir, '{}_{:06d}{}'.format(file_name, counter, ext)))


if __name__ == '__main__':

    split_list_into_pieces('data/frames_train.txt', max_len=20000, output_dir='data/train_splits', shuffle_list=True)
