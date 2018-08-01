# -*- coding:utf-8 -*-

__author__ = 'cht'
'''
色度键读取子模块

thoughts: 
- 或许命令行工具可以直接借助matplotlib来实现色度读取，免去绘制GUI的麻烦
- 不考虑用pyqt读图了，估计很繁琐也没意义
credits:
- 
'''

from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np  # use numpy to vectorize process image


def rgb_bounding(colors):
    for color in range(len(colors)):
        if colors[color] > 255:
            colors[color] = 255
            continue
        elif colors[color] < 0:
            colors[color] = 0
            continue
    return colors


def color_diff(rgba1, rgba2):
    return abs(rgba1[0]-rgba2[0]) + abs(rgba1[1]-rgba2[1]) + abs(rgba1[2]-rgba2[2]) + abs(rgba1[3]-rgba2[3])


# contiguous filling a region
def flood_fill(image, xy, value, thresh=0):
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = [(x, y)]
    while edge:
        newedge = []
        for (x, y) in edge:
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if color_diff(p, background) <= thresh:
                        pixel[s, t] = value
                        newedge.append((s, t))
        edge = newedge


def rip_bg_with_chroma_key(img, tol):
    plt.figure("Image")
    plt.imshow(img)
    print("Please click a spot to identify the color to remove")
    coordinates = plt.ginput(1)[0]
    x = round(coordinates[0])
    y = round(coordinates[1])
    if img.getpalette() is not None:
        # then the image is based on palette coloring
        print('not none palette.')
        img = img.convert(mode=None)
    flood_fill(img, (x, y), (255, 255, 255, 255), thresh=tol)
    out = img
    plt.close()
    return out


def rip_bg_with_chroma_key_frame0(img, tol):

    plt.figure("Image")
    plt.imshow(img)
    print("Please click a spot to identify the color to remove")
    coordinates = plt.ginput(1)[0]
    x = round(coordinates[0])
    y = round(coordinates[1])
    if img.getpalette() is not None:
        # then the image is based on palette coloring
        print('not none palette.')
        img = img.convert(mode=None)
    pixel = np.array(img.getpixel((x, y)))

    flood_fill(img, (x, y), (0, 0, 0, 0), thresh=tol)
    alpha = img.split()[3]
    out = img.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    out.paste(255, mask=mask)

    # plt.clf()
    # plt.imshow(img)
    # plt.ginput(1)
    plt.close()
    return out, pixel, (x, y)


def rip_bg_with_chroma_key_auto(img, tol, coordinates):
    if img.getpalette() is not None:
        print('Not none palette')
        # then the image is based on palette coloring
        img = img.convert(mode=None)

    flood_fill(img, coordinates, (0, 0, 0, 0), thresh=tol)
    alpha = img.split()[3]
    out = img.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    out.paste(255, mask)
    # plt.imshow(out)
    # plt.ginput(1)
    # plt.close()
    #
    # arr = np.array(out)
    # out.putpalette([])  # try to nullify the palette of following frames.
    return out


'''
    # width = img.size[0]
    #height = img.size[1]

    # len_pixel = len(pixel)
    # print('the color RGB is ' + str(pixel))

    # arr = np.array(img)
    # arr_pixel = np.full((height, width, len_pixel), pixel)

    # g = arr[:, :, 0:len_pixel]
    # zeros = np.full((height, width, len_pixel), (255,255,255,pixel[len_pixel-1]))  # fill transparency to #FFF for output
    # if tol == 0:
    #     cond = g == arr_pixel
    #     arr[:, :, :] = cond * zeros + (~cond) * g  # do not know if its faster than floodfill
    #     out = Image.fromarray(arr)
    # else:
    #     ImageDraw.floodfill(img, (x, y), (255,255,255,1), border=None, thresh=tol)
    #     out = img

'''
