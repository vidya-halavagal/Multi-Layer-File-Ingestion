import os
import shutil

def ensure_directory(directory_path: str) -> None:
    """Create a folder if it is missing, so later steps never fail on a missing path.

    Args:
        directory_path: Path of the folder to create.

    Returns:
        None. Does nothing if the folder already exists.
    """
    os.makedirs(directory_path, exist_ok=True)


def move_file(file_name: str, source_dir: str, destination_dir: str) -> None:
    """Move a file from one folder to another.

    Args:
        file_name: Name of the file to move.
        source_dir: Folder the file is in now.
        destination_dir: Folder to move it into.

    Returns:
        None file ends up in the destination folder.
    """
    # Create the destination folder if it is missing 
    ensure_directory(destination_dir)

    # Build the old and new paths 
    source_path = os.path.join(source_dir, file_name)
    destination_path = os.path.join(destination_dir, file_name)

    # Move the file 
    shutil.move(source_path, destination_path)