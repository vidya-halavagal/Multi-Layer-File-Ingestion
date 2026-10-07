
import os

# Create a function to fetch all files from the target directory
def fetch_target_files(target_dir) -> list[str]:
    """Fetch all files from the specified target directory."""
    
    all_files = []

    # Check each item in the target directory
    try:
        for file_name in os.listdir(target_dir):
            full_file_path = os.path.join(target_dir, file_name)

            # Add only files, not folders
            if os.path.isfile(full_file_path):
                all_files.append(file_name)

        return all_files

    # Handle the case when the directory does not exist
    except FileNotFoundError:
        print(f"Directory not found: {target_dir}")
        return []
        
all_files = fetch_target_files(target_dir)
