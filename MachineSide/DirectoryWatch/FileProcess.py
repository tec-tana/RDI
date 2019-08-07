"""
File Processing

1. Loop over directory and watch for complete set
2. Validate the set (e.g. filtering empty files)
3. Merge dataframe, and save completed dataframe in different folder (locally).
4. Save file on cloud storage
5. Delete merged files in original folder.
"""
import pandas as pd
# import FileUpload
# import DataDiagnostics


class FileProcess:
    """
    This function process the file then upload.

    :param file_path: raw string literal
    :param action: int literal, 1=> created, 3=>updated
    :return:
    """
    def __init__(self):
        pass

    def add(self, *file_path: str, action: str = "Completed"):
        print(file_path, action)
        pass

    def file_validate(self, file_path: str):
        """
        This function validates file before upload.

        :param file_path: raw string literal
        :return bool: True = eligible for upload
        """
        # DataDiagnostics.__main__()
        return

    def file_merge(self, *file_path):
        """
        This function merge files into pandas dataframe.

        :param file_path:
        :return:
        """
        pass

    def file_upload(self, file_path: str):
        """
        This function upload given files to database / cloud storage.

        :param file_path: raw string literal
        :return:
        """
        # convert pandas dataframe to json file
        # json_dataframe = FileUpload.convert_to_json(file_path)
        # upload json file to Google Cloud Storage
        # FileUpload.upload_to_gcs(json_dataframe)
        return

    def file_update(self, file_path: str):
        """
        This function updates the values in dataframe appropriately

        :param file_path: raw string literal
        """
        return
