import cv2
import glob
import numpy as np


def stitch_together(input_images, layout, resize_dim=None, off_x=None, off_y=None):
    """
    Stitch together N input images into a bigger frame, using a grid layout.
    Input images can be either color or grayscale, but must all have the same size.

    Parameters
    ----------
    input_images : list(ndarray)
        List of input images
    layout : tuple
        Grid layout expressed (rows, cols) of the stitch
    resize_dim : tuple, optional
        If present, stitch is resized to this size following convention resize_dim=(new_h, new_w)
    off_x : int, optional
        Offset between stitched images along x axis
    off_y : int, optional
        Offset between stitched images along y axis

    Returns
    -------
    stitch : ndarray
        Stitch of the input images.
    """

    if len(set([img.shape for img in input_images])) > 1:
        raise ValueError('All images must have the same shape')

    # determine if input images are color (3 channels) or grayscale (single channel)
    if len(input_images[0].shape) == 2:
        mode = 'grayscale'
        img_h, img_w = input_images[0].shape
    elif len(input_images[0].shape) == 3:
        mode = 'color'
        img_h, img_w, img_c = input_images[0].shape
    else:
        raise ValueError('Unknown shape for input images')

    # if no offset is provided, set to 10% of image size
    if off_x is None:
        off_x = img_w // 10
    if off_y is None:
        off_y = img_h // 10

    # create stitch mask
    rows, cols = layout
    stitch_h = rows * img_h + (rows + 1) * off_y
    stitch_w = cols * img_w + (cols + 1) * off_x
    if mode == 'color':
        stitch = np.zeros(shape=(stitch_h, stitch_w, img_c), dtype=np.uint8)
    elif mode == 'grayscale':
        stitch = np.zeros(shape=(stitch_h, stitch_w), dtype=np.uint8)

    for r in range(0, rows):
        for c in range(0, cols):

            list_idx =  r * cols + c

            if list_idx < len(input_images):
                if mode == 'color':
                    stitch[ r * (off_y + img_h) + off_y: r*(off_y+img_h) + off_y + img_h,
                            c * (off_x + img_w) + off_x: c * (off_x + img_w) + off_x + img_w,
                            :] = input_images[list_idx]
                elif mode == 'grayscale':
                    stitch[ r * (off_y + img_h) + off_y: r*(off_y+img_h) + off_y + img_h,
                            c * (off_x + img_w) + off_x: c * (off_x + img_w) + off_x + img_w]\
                        = input_images[list_idx]

    if resize_dim:
        stitch = cv2.resize(stitch, dsize=(resize_dim[::-1]))

    return stitch


if __name__ == '__main__':

    img_list = glob.glob('img/*.jpg')

    images = [cv2.imread(f, cv2.IMREAD_COLOR) for f in img_list]

    s = stitch_together(images, layout=(5, 5), resize_dim=(1000, 1000))

    cv2.imshow('s', s)
    cv2.waitKey()



