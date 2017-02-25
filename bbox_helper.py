import cv2
import numpy as np


class Rectangle:
    """
    2D Rectangle defined by top-left and bottom-right corners.

    Parameters
    ----------
    x_min : int
        x coordinate of top-left corner.
    y_min : int
        y coordinate of top-left corner.
    x_max : int
        x coordinate of bottom-right corner.
    y_min : int
        y coordinate of bottom-right corner.
    """
    
    def __init__(self, x_min, y_min, x_max, y_max):

        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

        self.x_side = self.x_max - self.x_min
        self.y_side = self.y_max - self.y_min

    def intersect_with(self, rect):
        """
        Compute the intersection between this instance and another Rectangle.
        
        Parameters
        ----------
        rect : Rectangle
            The instance of the second Rectangle.
            
        Returns
        -------
        intersection_area : float
            Area of intersection between the two rectangles expressed in number of pixels.
        """
        if not isinstance(rect, Rectangle):
            raise ValueError('Cannot compute intersection if "rect" is not a Rectangle')

        dx = min(self.x_max, rect.x_max) - max(self.x_min, rect.x_min)
        dy = min(self.y_max, rect.y_max) - max(self.y_min, rect.y_min)

        if dx >= 0 and dy >= 0:
            intersection = dx * dy
        else:
            intersection = 0.

        return intersection

    def resize_sides(self, ratio, bounds=None):
        """
        Resize the sides of rectangle while mantaining the aspect ratio and center position.

        Parameters
        ----------
        ratio : float
            Ratio of the resize in range (0, infinity), where 2 means double the size and 0.5 is half of the size.
        bounds: tuple, optional
            If present, clip the Rectangle to these bounds=(xbmin, ybmin, xbmax, ybmax).

        Returns
        -------
        rectangle : Rectangle
            Reshaped Rectangle.
        """

        # compute offset
        off_x = abs(ratio * self.x_side - self.x_side) / 2
        off_y = abs(ratio * self.y_side - self.y_side) / 2

        # offset changes sign according if the resize is either positive or negative
        sign = np.sign(ratio - 1.)
        off_x = np.int32(off_x * sign)
        off_y = np.int32(off_y * sign)

        # update top-left and bottom-right coords
        new_x_min, new_y_min = self.x_min - off_x, self.y_min - off_y
        new_x_max, new_y_max = self.x_max + off_x, self.y_max + off_y

        # eventually clip the coordinates according to the given bounds
        if bounds:
            b_x_min, b_y_min, b_x_max, b_y_max = bounds
            new_x_min = max(new_x_min, b_x_min)
            new_y_min = max(new_y_min, b_y_min)
            new_x_max = min(new_x_max, b_x_max)
            new_y_max = min(new_y_max, b_y_max)

        return Rectangle(new_x_min, new_y_min, new_x_max, new_y_max)

    def draw(self, frame, color=255, thickness=1):
        """
        Draw Rectangle on a given frame.

        Notice: while this function does not return anything, original image `frame` is modified.

        Parameters
        ----------
        frame : 2D / 3D np.array
            The image on which the rectangle is drawn.
        color : tuple, optional
            Color used to draw the rectangle (default = 255)
        thickness : int, optional
            Line thickness used t draw the rectangle (default = 1)

        Returns
        -------
        None
        """
        cv2.rectangle(frame, (self.x_min, self.y_min), (self.x_max, self.y_max), color, thickness)

    def get_binary_mask(self, mask_shape):
        """
        Get uint8 binary mask of shape `mask_shape` with rectangle in foreground.

        Parameters
        ----------
        mask_shape : (tuple)
            Shape of the mask to return - following convention (h, w)

        Returns
        -------
        mask : np.array
            Binary uint8 mask of shape `mask_shape` with rectangle drawn as foreground.
        """
        if mask_shape[0] < self.y_max or mask_shape[1] < self.x_max:
            raise ValueError('Mask shape is smaller than Rectangle size')
        mask = np.zeros(shape=mask_shape, dtype=np.uint8)
        mask = cv2.rectangle(mask, self.tl_corner, self.br_corner, color=255, thickness=cv2.FILLED)
        return mask

    @property
    def tl_corner(self):
        """
        Coordinates of the top-left corner of rectangle (as int32).

        Returns
        -------
        tl_corner : int32 tuple
        """
        return tuple(map(np.int32, (self.x_min, self.y_min)))

    @property
    def br_corner(self):
        """
        Coordinates of the bottom-right corner of rectangle.
        
        Returns
        -------
        br_corner : int32 tuple
        """
        return tuple(map(np.int32, (self.x_max, self.y_max)))

    @property
    def coords(self):
        """
        Coordinates (x_min, y_min, x_max, y_max) which define the Rectangle. 
        
        Returns
        -------
        coordinates : int32 tuple
        """
        return tuple(map(np.int32, (self.x_min, self.y_min, self.x_max, self.y_max)))

    @property
    def area(self):
        """
        Get the area of Rectangle
        
        Returns
        -------
        area : float32
        """
        return np.float32(self.x_side * self.y_side)