from PIL import Image, ImageFont, ImageDraw
import os
import matplotlib.pyplot as plt


def add_text(img, font_size, x_pos, y_pos, text, color):
    draw = ImageDraw.Draw(img)
    # C:/Windows/Fonts/YaHeiMonacoHybird.ttf
    # C:/Windows/Fonts/STZHONGS.TTF
    font = ImageFont.truetype(os.path.join('fonts', 'C:/Windows/Fonts/STZHONGS.TTF'), font_size)
    draw.text((x_pos, y_pos), text, font=font, fill=color)  # color = "#111"
    return img


def save_img_file_as_static_gif_with_alpha(img, transparent_gif_bg_path, save_filename, quantize):
    # width = img.size[0]
    # height = img.size[1]
    # bg = Image.open(transparent_gif_bg_path)
    # transparency = bg.info['transparency']
    # im = Image.new("RGBA", (width, height), (1,1,1))
    # im.paste(img)
    # if quantize > 0:
    #     # seems not working for gif. improve later
    #     im = im.convert('P').quantize(colors=quantize, method=2)
    #     # im = im.convert('P', palette=Image.ADAPTIVE, colors=quantize)
    #     print(len(im.getpalette()))
    transparency = 255
    img.save(save_filename, transparency=transparency, version='GIF89a', optimize=True)


    return


def save_img_file_as_animated_gif_with_alpha(frame0, img, transparent_gif_bg_path, save_filename, version, duration):
    transparency = 255
    frame0.save(save_filename, transparency=transparency, save_all=True, optimize=False, append_images=img, disposal=2, version=version, loop=0, duration=duration)
    return


'''
width = frame0.size[0]
height = frame0.size[1]
# bg = Image.open(transparent_gif_bg_path)
# transparency = bg.info['transparency']
# im = Image.new("RGBA", (width, height), (255,255,255))
# im.paste(frame0)
# im = im.convert('RGB').convert(mode='P', dither=Image.FLOYDSTEINBERG, palette='ADAPTIVE', colors=255)
# im = frame0.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=255)
# mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
# im.paste(0, mask)
# im.save(save_filename, transparency=transparency, version='GIF89a')
'''
