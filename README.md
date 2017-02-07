# computer_vision_utils

Everything that I code more than twice during my PhD will end up here.

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