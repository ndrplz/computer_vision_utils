import cv2
import numpy as np


def resize_tensor(tensor, new_size):
    """
    Resizes an input tensor with opencv. Resize is done for each channel indipendently,

    :param tensor: must have size (channels, h, w)
    :param new_size: tuple like (new_h, new_w)
    :return: the resized tensor having size (channels, new_h, new_w)
    """
    channels = tensor.shape[0]
    new_tensor = np.zeros(shape=(channels,)+new_size)
    for i in range(0, channels):
        new_tensor[i] = cv2.resize(tensor[i], dsize=new_size[::-1])

    return new_tensor
