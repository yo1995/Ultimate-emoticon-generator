from PIL import Image


def decode_static_image_file(filename):
    img = Image.open(filename)
    img = img.convert('RGBA')  # just convert to RGBA to ease the process of output
    return img


def decode_gif_file(filename):
    img = Image.open(filename)
    try:
        img.seek(1)
    except EOFError:
        print('Warning: it is a single frame GIF.')
        return img, 1
    return img, 2
