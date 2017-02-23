import cv2
import numpy as np
import os.path as path




def read_image(image_path, channels_first, color=True, color_mode='RGB', dtype=np.float32, resize_dim=None):

    """
    Reads and returns an image as a numpy array

    Parameters
    ----------
    image_path : string
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
    ----------
    Loaded Image as numpy array of type dtype
    """

    if not path.exists(image_path):
        raise ValueError('Provided path "{}" does NOT exist.'.format(image_path))

    image = cv2.imread(image_path, cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE)

    if color and color_mode == 'RGB':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if resize_dim is not None:
        image = cv2.resize(image, dsize=resize_dim[::-1], interpolation=cv2.INTER_LINEAR)

    if color and channels_first:
        image = np.transpose(image, (2, 0, 1))

    return image.astype(dtype)


if __name__ == '__main__':

    img = read_image('img/test1.jpg', False, color=True, color_mode='BGR', dtype=np.uint8)
    cv2.imshow('test image', img)
    cv2.waitKey()
