import jsonlines
from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import argparse

# arguments for the script defined
parser = argparse.ArgumentParser(description='Import a folder content to MongoDB')
parser.add_argument('folder_name', type=str,
                    help='Folder name containing jsonlines files to parse, prefixed with the language code')

# open mongodb connection and collection
client = MongoClient('localhost', 27017)
db = client['references']
collection = 'all'

def get_files(folder_name):
    """ Get file names from a given folder
    :param folder_name: name of the folder that the jsonlines files are stored
    :return: list of file names
    """
    file_names = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
    return file_names

def load_file_data(folder_name, file_name):
    """ load data from jsonlines file
    Adds language code, assuming the file name is <languagecode>-references.ljson
    :param file_name: filename with data to be loaded into mongodb
    :return: list with data from the file
    """
    file_data = []
    with jsonlines.open(folder_name + '/' + file_name) as reader:
        for obj in reader:
            obj['language'] = file_name.split('-')[0]
            file_data.append(obj)
    return file_data


def insert_into_collection(file_data):
    """ Insert file_data into collection
    :param file_data: file data to be inserted into the collection
    :return:
    """
    collection_english = db[collection]
    # if pymongo < 3.0, use insert()
    #collection_english.insert(file_data)
    # if pymongo >= 3.0 use insert_one() for inserting one document
    #collection_english.insert_one(file_data)
    # if pymongo >= 3.0 use insert_many() for inserting many documents
    collection_english.insert_many(file_data)


if __name__ == '__main__':
    args = parser.parse_args()
    file_names = get_files(args.folder_name)
    for file_name in file_names:
        file_data = load_file_data(args.folder_name, file_name)
        insert_into_collection(file_data)

    client.close()