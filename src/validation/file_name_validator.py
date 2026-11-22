import re

def is_valid_file_name(
    file_name: str,
    pattern: re.Pattern) -> bool:
    """
    Check whether a file name matches the compiled regex pattern.

    Args:
        file_name: Name of the file to validate.
        pattern: Compiled regex pattern used for filename validation.

    Returns:
        True if the entire filename matches the pattern, otherwise False.
    """

    # Match the entire file name against the compiled regex pattern.
    return pattern.fullmatch(file_name) is not None


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
