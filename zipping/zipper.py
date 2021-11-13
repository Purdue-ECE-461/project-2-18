from zipfile import ZipFile

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = "PA3.zip"
    with ZipFile(file, 'r') as zipper:
        zipper.extractall()
