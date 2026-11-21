from src.file_scanner import fetch_target_files
from src.file_validator import split_files

def get_valid_files(target_dir: str, file_pattern: str = r"[a-zA-Z]+_[a-zA-Z]+_\d{8}\.txt") -> list[str]:
    """Return only the file names in a folder that match the name pattern.

    Args:
        path: Folder to scan.
        file_pattern: Regex pattern a valid file name must match.

    Returns:
        list of valid file.
    """
    files = fetch_target_files(target_dir)
    valid, invalid = split_files(files, file_pattern)

    return valid
    

def process_file(file_name: str) -> None:
    """Process a single file.

    Args:
        file_name: Name of the file to process.
    """
    print(f"Processing: {file_name}")

