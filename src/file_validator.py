import re


def is_valid_file_name(file_name: str, pattern: str) -> bool:
    """Check whether a file name matches <name>_<address>_<date>_<time>.txt format.

    Args:
        file_name: Name of the file to check.
        pattern: Regex pattern a valid file name must match.

    Returns:
        True if the whole file name matches the pattern, otherwise False.
    """
    file_pattern = re.compile(pattern)
    return file_pattern.fullmatch(file_name) is not None


def split_files(file_names: list[str], pattern: str) -> tuple[list[str], list[str]]:
    """Split file names into valid and invalid lists based on a regex pattern.

    Args:
        file_names: List of file names to check.
        pattern: Regex pattern a valid file name must match.

    Returns:
        A tuple (valid_files, invalid_files) of two lists of file names.
    """
    valid_files = []
    invalid_files = []

    for file_name in file_names:
        if is_valid_file_name(file_name, pattern):
            valid_files.append(file_name)
        else:
            invalid_files.append(file_name)

    return valid_files, invalid_files


def has_valid_header(header_line: str, expected_columns: list[str]) -> bool:
    """Check whether a header line has the expected columns in the expected order.

    Args:
        header_line: First line of a file, e.g. "id,name,address,amount".
        expected_columns: Column names the header must match, in order.

    Returns:
        True if the header matches exactly, otherwise False.
    """
    columns = header_line.strip().split(",")
    return columns == expected_columns
