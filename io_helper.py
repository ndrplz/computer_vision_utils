import cv2
import numpy as np


def read_image(path, channels_first, color=True, dtype=np.float32, resize_dim=None):
    """
    Reads and returns an image as a numpy array

    :param path: image filename
    :param channels_first: whether to have color channels in first position or not
    :param color: if true, loads color, otherwise greyscale
    :param dtype: data type to return
    :param resize_dim: optional, resize size (interpolation is linear)
    :return:
    """
    i = cv2.imread(path, 1 if color else 0)
    if color:
        i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)

    if resize_dim is not None:
        i = cv2.resize(i, dsize=resize_dim[::-1], interpolation=cv2.INTER_LINEAR)

    if color and channels_first:
        i = np.transpose(i, (2, 0, 1))

    return i.astype(dtype)
