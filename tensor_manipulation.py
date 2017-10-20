import cv2
import numpy as np


def resize_tensor(tensor, new_shape):
    """
    Resize a numeric input 3D tensor with opencv. Each channel is resized independently from the others.
    
    Parameters
    ----------
    tensor: ndarray
        Numeric 3D tensor of shape (channels, h, w)
    new_shape: tuple
        Tuple (new_h, new_w)

    Returns
    -------
    new_tensor: ndarray
        Resized tensor having size (channels, new_h, new_w)
    """
    channels = tensor.shape[0]
    new_tensor = np.zeros(shape=(channels,) + new_shape)
    for i in range(0, channels):
        new_tensor[i] = cv2.resize(tensor[i], dsize=new_shape[::-1])

    return new_tensor


def crop_tensor(tensor, indexes):
    """
    Crop a numeric 3D input tensor.
    
    Parameters
    ----------
    tensor: ndarray
        Numeric 3D tensor of shape (channels, h, w)
    indexes: tuple
        Crop indexes following convention (h1, h2, w1, w2)

    Returns
    -------
    new_tensor: ndarray
        Cropped tensor having size (channels, h2-h1, w2-w1)
    """
    h1, h2, w1, w2 = indexes
    new_tensor = tensor[:, h1:h2, w1:w2].copy()

    return new_tensor
