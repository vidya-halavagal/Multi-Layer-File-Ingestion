import os

def is_unprocessed(filename: str, processed_folder: str) -> bool:
    """check whether the file is not already processed."""
    
    # get processed files and check if the filename is not present
    return filename not in os.listdir(processed_folder)
