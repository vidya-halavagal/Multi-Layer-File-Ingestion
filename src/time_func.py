import time
from typing import Callable, List


def set_timer(
    scan_func: Callable[[str], List[str]],
    target_dir: str,
    interval_minutes: float,
    sleep_time: int = 2,
) -> None:
    """Run a scan_func on a folder repeatedly until the time is up.

    Args:
        scan_func: Function to run, called as scan_func(target_dir).
        target_dir: Folder to give to the scan_func.
        interval_minutes: How many minutes to keep running.
        sleep_time: Seconds to wait between scans.
    """
    # Work out when to stop: now + minutes converted to seconds
    end_time = time.time() + (interval_minutes * 60)

    # Keep going while the current time is before the end time
    while time.time() < end_time:
        print(f"seconds left: {round(end_time - time.time(), 1)}")

        # Run the scan_func to check for files
        scan_func(target_dir)

        # Wait before the next scan
        time.sleep(sleep_time)
        

def has_time_left(end_time: float) -> bool:
    """Return True while the round's time budget is not used up.

    Args:
        end_time: Unix timestamp marking the deadline for the round.

    Returns:
        True if current time is before end_time, False otherwise.
    """
    return time.time() < end_time