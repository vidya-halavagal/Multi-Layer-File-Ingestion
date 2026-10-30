import hashlib


def compute_file_hash(file_path: str, chunk_size: int = 8192) -> str:
    """Read a file in small chunks and return its SHA-256 fingerprint.

    Args:
        file_path: Path of the file we want to fingerprint.
        chunk_size: Number of bytes to read at a time (default 8192).

    Returns:
        The file's SHA-256 fingerprint as a hex string.
    """
    hasher = hashlib.sha256()
    
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            
            if not chunk:
                break
                
            hasher.update(chunk)
            
    return hasher.hexdigest()
