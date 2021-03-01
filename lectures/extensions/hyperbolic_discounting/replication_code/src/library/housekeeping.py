"""Functions that may be shared across modules, mostly useful for housekeeping."""
import contextlib
import os
import pickle
import shutil
from pathlib import Path
from time import time


@contextlib.contextmanager
def _temporary_working_directory(snippet):
    """Changes working directory and returns to previous on exit.
    The name of the temporary directory is 'temp_process-id_timestamp_snippet'
    The directory is deleted upon exit.

    Args:
        snippet (string): Suffix that identifies the temporary directory.
            Useful whenever parallelization is required.

    """
    folder_name = f"temp_{os.getpid()}_{str(time()).replace('.', '')}_{snippet}"
    path = Path(".").resolve() / folder_name
    path.mkdir()
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
        shutil.rmtree(path)


def _load_pickle(input_file):
    """Load object from pickle."""
    with open(input_file, "rb") as input_file:
        object = pickle.load(input_file)

    return object


def _save_to_pickle(object, output_file):
    """Save object to pickle."""
    with open(output_file, "wb") as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)
