"""
Reads a json files in the form of the POST PackageCreate example,
decodes the base64 string to a zip file in the 'zipped_files' dir using the metadata name,
and extracts that zip file into a named subdirectory in the 'extracted_files' dir
"""
import binascii
import json
from base64 import b64decode
from zipfile import ZipFile


def main():
    with open('example.json', 'r') as json_file:
        data: dict = json.load(json_file)

    try:
        encoded_zip = data['data']['Content']
    except KeyError:
        print("Package doesn't have a content key")
        return
    try:
        name = data['metadata']['Name']
    except KeyError:
        print("Package doesn't have a name")
        return

    try:
        decoded_bytes = b64decode(encoded_zip)
    except binascii.Error as exp:
        print(exp)
        return

    with open(f'./zipped_files/{name}.zip', 'wb') as f:
        f.write(decoded_bytes)

    with ZipFile(f'./zipped_files/{name}.zip', 'r') as zipper:
        zipper.extractall(path=f'./extracted_files/{name}')


if __name__ == '__main__':
    main()
