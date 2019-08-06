"""
File Processing

1. Add new file path to watch_set, if it is a complete set, validate the data. Otherwise, pass.
2. Validation includes filter empty files, etc.
3. Generate dataframe based on this initial file set. Record complete set of dataframe.
4. If files are updated, update appropriate dataframe.
"""
import pandas as pd
import FileUpload
import DataDiagnostics


def file_process(file_path: str):
    """
    This function process the file then upload.

    :param file_path: raw string literal
    :return:
    """
    print(file_path)
    return


def file_upload(file_path: str):
    """
    This function upload given files to database.

    :param file_path: raw string literal
    :return:
    """
    FileUpload.import_content(file_path)
    return


def file_validate(file_path: str):
    """
    This function validates file before upload.

    :param file_path: raw string literal
    :return bool: True = eligible for upload
    """
    DataDiagnostics.__main__()
    return

def file_update(file_path: str):
    """
    This function updates the values in dataframe appropriately

    :param file_path: raw string literal
    """
    return
