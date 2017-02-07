from __future__ import print_function
import pickle
import os.path as path
import sklearn.utils


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


def split_into_chunks(list_in, max_elements, shuffle=False):
    """
    Split a list a variable number of chunks of at most "max_elements" each.

    :param list_in: input list to be splitted
    :param max_elements: max elements allowed into each chunk
    :param shuffle: if True, input list is shuffled before chunking
    :return: list of lists. Each element is a chunk of list_in
    """

    if not isinstance(list_in, list):
        raise ValueError('Input must be a list.')

    list_out = []

    if shuffle:
        list_in = sklearn.utils.shuffle(list_in)

    counter = 0
    for offset in range(0, len(list_in), max_elements):
        list_chunk = list_in[offset:offset + max_elements]
        list_out.append(list_chunk)
        counter += 1

    return list_out


if __name__ == '__main__':

    mylist = ['a', 'b', 'c', 'd', 'e']

    split_into_chunks(mylist, max_elements=2, shuffle=True)
