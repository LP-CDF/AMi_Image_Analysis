import os

def ensure_directory(file_path):
    """Checks the given file path for a directory, and creates one if not already present.

    Args:
        file_path: a string representing a valid URL
    """

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
