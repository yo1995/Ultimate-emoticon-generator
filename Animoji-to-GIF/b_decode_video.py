import imageio
from PIL import Image


def decode_video_file(filename):
    image_stack = []
    vid = imageio.get_reader(filename, 'ffmpeg')
    for img in enumerate(vid):
        img = Image.fromarray(img[1])
        img = img.convert('RGBA')
        image_stack.append(img)
    return image_stack
