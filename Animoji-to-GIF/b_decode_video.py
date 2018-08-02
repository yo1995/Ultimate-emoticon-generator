import imageio
from PIL import Image


def decode_video_file(filename, crop=False, crop_box=None):
    image_stack = []
    i = 0
    vid = imageio.get_reader(filename, 'ffmpeg')
    for img in enumerate(vid):
        i = i + 1
        img = Image.fromarray(img[1])
        img = img.convert('RGBA')
        if crop:
            img = img.crop(crop_box)
        image_stack.append(img)

    if i > 120:
        info_str = 'total frames is: ' + str(i) + ', you might want to change max_frames setting.'
    else:
        info_str = 'total frames is: ' + str(i)
    print(info_str)

    if image_stack[0].size[0] > 2000 or image_stack[0].size[1] > 2000:
        print('input dimension too large for GIF! either crop or resize. abort.')
        exit(-1)

    return image_stack
