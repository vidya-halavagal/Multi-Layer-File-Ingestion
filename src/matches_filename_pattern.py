import re

def matches_filename_pattern(filename:str,pattern:str) -> bool:  
    """validate whether a filename matches <name>_<address>_<date>_<time>.txt format"""
    file_pattern = re.compile(pattern)

    if not file_pattern.match(filename):
        return False
    return True 
