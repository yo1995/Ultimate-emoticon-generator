from PIL import Image


def decode_static_image_file(filename):
    img = Image.open(filename)
    img = img.convert('RGBA')  # just convert to RGBA to ease the process of output

    if img.size[0] > 2000 or img.size[1] > 2000:
        print('input dimension too large for GIF! either crop or resize. abort.')
        exit(-1)

    return img


def decode_gif_file(filename):
    img = Image.open(filename)
    try:
        img.seek(1)
    except EOFError:
        print('Warning: it is a single frame GIF.')
        if img.size[0] > 2000 or img.size[1] > 2000:
            print('input dimension too large for GIF! either crop or resize. abort.')
            exit(-1)
        return img, 1
    return img, 2
