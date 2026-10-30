import time

from src.file_scanner import fetch_target_files

def build_file_queue(leftover_files: list[str], target_dir: str) -> list[str]:
    """combine  leftover files with new unqueued files from the target directory.

    Args:
        leftover_files: List of files left over from the previous round.
        target_dir: Path of the directory containing incoming files.

    Returns:
        Ordered list of files to process leftovers first, followed by new files.
    """
    # scan from the Target dir
    scanned_files = fetch_target_files(target_dir)

    new_files = []
    # fetch only Leftover files which are not in new files
    for file in scanned_files:
        if file not in leftover_files:
            new_files.append(file)
        
    # we get leftovers first, new files next
    return leftover_files + new_files


def run_pipeline_round(
    target_dir: str,
    processed_dir: str,
    rejected_dir: str,
    interval_minutes: float,
    leftover_files: list[str],
) -> None:
    """Run one ingestion cycle within the allotted time budget.

    Args:
        target_dir: Folder containing incoming files.
        processed_dir: Folder to move completed files.
        rejected_dir: Folder to move invalid files.
        interval_minutes: Max time limit for this round.
        leftover_files: Files left over from the previous round.
    """
    round_start_time = time.time()
    end_time = round_start_time + (interval_minutes * 60)
    print(f"Round started! Time budget: {interval_minutes} minutes.")

    queue = build_file_queue(leftover_files, target_dir)
    print(f"Queue ready: {len(queue)} files")