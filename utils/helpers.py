import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def file_extension(filename):
    return filename.split(".")[-1].lower()