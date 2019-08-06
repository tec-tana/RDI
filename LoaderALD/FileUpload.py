"""
File Upload to MongoDB database

Credit to https://gist.github.com/mprajwala/849b5909f5b881c8ce6a
"""
import os
import pandas as pd
import pymongo
import json


def import_content(file_path: str):
    """
    This function uploads csv file onto MongoDB.

    :param file_path: string literal
    :return:
    """
    mongo_client = pymongo.MongoClient('localhost', 27017)
    mongo_db = mongo_client['mongodb_name']  # Replace mongo db name
    collection_name = 'collection_name'  # Replace mongo db collection name
    db_cm = mongo_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, file_path)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)


if __name__ == "__main__":
    file_path = '/path/to/csv/path'  # pass csv file path
    import_content(file_path)
