import cv2
import numpy as np
import os.path as path


def read_image(img_path, channels_first, color=True, color_mode='BGR', dtype=np.float32, resize_dim=None):

    """
    Reads and returns an image as a numpy array

    Parameters
    ----------
    img_path : string
        Path of the input image
    channels_first: bool
        If True, channel dimension is moved in first position
    color: bool, optional
        If True, image is loaded in color: grayscale otherwise
    color_mode: "RGB", "BGR", optional
        Whether to load the color image in RGB or BGR format
    dtype: dtype, optional
        Array is casted to this data type before being returned
    resize_dim: tuple, optional
        Resize size following convention (new_h, new_w) - interpolation is linear

    Returns
    -------
    image : np.array
        Loaded Image as numpy array of type dtype
    """

    if not path.exists(img_path):
        raise ValueError('Provided path "{}" does NOT exist.'.format(img_path))

    image = cv2.imread(img_path, cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE)

    if color and color_mode == 'RGB':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if resize_dim is not None:
        image = cv2.resize(image, dsize=resize_dim[::-1], interpolation=cv2.INTER_LINEAR)

    if color and channels_first:
        image = np.transpose(image, (2, 0, 1))

    return image.astype(dtype)


def write_image(img_path, img, channels_first=False, color_mode='BGR', resize_dim=None, to_normalize=False):
    """
    Writes an image (numpy array) on file

    Parameters
    ----------
    img_path : string
        Path where to save image
    img : ndarray
        Image that has to be saved
    channels_first: bool
        Set this True if shape is (c, h, w)
    color_mode: "RGB", "BGR", optional
        Whether the image is in RGB or BGR format
    resize_dim: tuple, optional
        Resize size following convention (new_h, new_w) - interpolation is linear
    to_normalize: bool
        Whether or not to normalize the image between 0 and 255.

    Returns
    ----------
    """

    color = True if img.ndim == 3 else False
    if color and channels_first:
        img = img.transpose(1, 2, 0)

    if color and color_mode == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if resize_dim is not None:
        img = cv2.resize(img, resize_dim[::-1])

    if to_normalize:
        normalize(img)

    cv2.imwrite(img_path, img)


def normalize(img):
    """
    Normalizes an image between 0 and 255 and returns it as uint8.

    Parameters
    ----------
    img : ndarray
        Image that has to be normalized

    Returns
    ----------
    img : ndarray
        The normalized image
    """
    img = img.astype(np.float32)
    img -= img.min()
    img /= img.max()
    img *= 255
    img = img.astype(np.uint8)

    return img

if __name__ == '__main__':

    img = read_image('img/test1.jpg', False, color=False, color_mode='BGR', dtype=np.uint8)
    cv2.imshow('test image', img)
    cv2.waitKey()

    write_image('img/test1_copy.jpg', img, channels_first=False, color_mode='BGR')
