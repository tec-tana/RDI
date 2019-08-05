"""
File Processing

1. Add new file path to watch_set, if it is a complete set, validate the data. Otherwise, pass.
2. Validation includes filter empty files, etc.
3. Generate dataframe based on this initial file set. Record complete set of dataframe.
4. If files are updated, update appropriate dataframe.
"""

import pandas as pd

def file_process(full_filename: str):
    """
    This function process the file then upload.

    :param full_filename: raw string literal
    :return:
    """
    print(full_filename)
    return


def file_upload(full_filename: str):
    """
    This function upload given files to database.

    :param full_filename: raw string literal
    :return:
    """
    return


def file_validate(full_filename: str):
    """
    This function validates file before upload.

    :param full_filename: raw string literal
    :return bool: True = eligible for upload
    """
    return

def file_update(full_filename: str):
    """
    This function updates the values in dataframe appropriately

    :param full_filename: raw string literal
    """
    return
