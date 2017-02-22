# computer_vision_utils

Everything that I code more than twice during my PhD will end up here.

stitching
--- 
- [stitching.py](stitching.py)

    `stitch_together(input_images, layout, resize_dim=None, off_x=None, off_y=None):`
    
    Stitch together N input images into a bigger frame, using a grid layout.
    Input images can be either color or grayscale, but must all have the same size.

containers
--- 

- [list_helper.py](list_helper.py)

    `dump_list(input_list, file_path)`
    
    Dump list to file, either in "txt" or binary ("pickle") mode. Dump mode is chosen accordingly to "file_path" extension.
    
    `load_list(file_path)`
    
   Load list from file, either in "txt" or binary ("pickle") mode. Load mode is chosen accordingly to "file_path" extension.
    
    `split_into_chunks(list_in, max_elements, shuffle=False)`
    
    Split a list a variable number of chunks of at most "max_elements" each.
    
filesystem
---

- [filesystem.py](filesystem.py)

    `get_file_list_recursively(top_directory, allowed_extension=[])`
    
    Get list of full paths of all files found under root directory "top_directory". If a list of allowed file extensions is provided, files are filtered according to this list.

io
---

- [io_helper.py](io_helper.py)
    
    `read_image(path, channels_first, color=True, dtype=np.float32, resize_dim=None)`

    Reads an image from "path" and returns respecting the self explanatory parameters

tensor_manipulation
-------------------

- [tensor_manipulation.py](tensor_manipulation.py)

    `resize_tensor(tensor, new_size)`

    Resizes a numeri tensor having shape (channels, h, w) into the new size (channels, new_h, new_w).
    Each channel is resized indipendently (good for feature maps).

    `crop_tensor(tensor, indexes)`
    Crops a numeric tensor having shape (channels, h, w) according to indexes in the form (h1,h2,w1,w2).





