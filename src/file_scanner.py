import os


def fetch_target_files(target_dir: str) -> list[str]:
    """Fetch all files from the specified target directory.

    Args:
        target_dir: Path of the directory to scan.

    Returns:
        List of file names (folders are skipped). Empty list if the
        directory does not exist.
    """
    all_files = []

    try:
        for file_name in os.listdir(target_dir):
            full_file_path = os.path.join(target_dir, file_name)

            # Add only files, not folders
            if os.path.isfile(full_file_path):
                all_files.append(file_name)

        return all_files

    except FileNotFoundError:
        print(f"Directory not found: {target_dir}")
        return []


def ensure_directory(directory_path: str) -> None:
    """Create a folder if it is missing, so later steps never fail on a missing path.

    Args:
        directory_path: Path of the folder to create.

    Returns:
        None. Does nothing if the folder already exists.
    """
    os.makedirs(directory_path, exist_ok=True)


def is_unprocessed(file_name: str, processed_folder: str) -> bool:
    """Check whether a file has not already been processed.

    Args:
        file_name: Name of the file to check.
        processed_folder: Path to the processed directory.

    Returns:
        bool: True if the file_name is not in the processed folder, otherwise False.
    """

    # List processed files and check whether this file is absent
    return file_name not in os.listdir(processed_folder)


def read_header_line(file_path: str) -> str:
    """Read the first line (header) of a file.

    Args:
        file_path: Full path of the file to open.

    Returns:
        The first line of the file as a string.
    """
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        header_line = file.readline().strip()
        return header_line
