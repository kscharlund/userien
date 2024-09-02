import contextlib
import fcntl
import os
import shelve
import typing


STORAGE_DIR = os.path.join(os.path.dirname(__file__), "tmp")


# Context manager for file locking shelves from:
# https://stackoverflow.com/questions/486490/python-shelve-module-question
@contextlib.contextmanager
def open_safe_shelve(
    db_path: str,
    flag: typing.Literal["r", "w", "c", "n"] = "c",
    protocol=None,
    writeback=False,
):
    if flag in {"w", "c", "n"}:
        lockfile_lock_mode = fcntl.LOCK_EX
    elif flag == "r":
        lockfile_lock_mode = fcntl.LOCK_SH
    else:
        raise ValueError(f"Invalid mode: {flag}, only 'r', 'w', 'c', 'n' are allowed.")

    with open(f"{db_path}.lock", "w") as lock_file:
        fcntl.flock(lock_file.fileno(), lockfile_lock_mode)
        try:
            yield shelve.open(
                db_path, flag=flag, protocol=protocol, writeback=writeback
            )
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def series_for_event(event_id):
    # TODO: Make more dynamic.
    all_series = [
        ["44027", "45014", "45486", "45015", "46473"],  # 2023
        ["48802", "49288", "48748", "50736", "50708", "50920"],  # 2024
    ]
    for series in all_series:
        if event_id in series:
            return series
    return [event_id]


def save_event_result_list(result_list):
    with open_safe_shelve(os.path.join(STORAGE_DIR, "events")) as db:
        db[result_list["event"]["event_id"]] = result_list


def read_event_result_list(event_id):
    with open_safe_shelve(os.path.join(STORAGE_DIR, "events"), "r") as db:
        return db.get(event_id, None)
