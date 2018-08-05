import os

# image files, support extensions .jpg .png .gif


def judge_file_extension(filename):
    (name, extension) = os.path.splitext(filename)
    extension.lower()
    print(extension)
    if extension == '.png' or extension == '.jpg':
        return 1
    if extension == '.mp4' or extension == '.mov':
        return 2
    if extension == '.gif':
        return 3

