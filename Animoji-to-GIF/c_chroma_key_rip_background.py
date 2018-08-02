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

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np  # use numpy to vectorize process image
from c_text import draw_text


def color_diff(rgba1, rgba2):
    if len(rgba1) == 3 and len(rgba2) == 3:
        return abs(rgba1[0] - rgba2[0]) + abs(rgba1[1] - rgba2[1]) + abs(rgba1[2] - rgba2[2])
    try:
        euc_length = abs(rgba1[0]-rgba2[0]) + abs(rgba1[1]-rgba2[1]) + abs(rgba1[2]-rgba2[2]) + abs(rgba1[3]-rgba2[3])
    except IndexError:
        return
    else:
        return euc_length


# contiguous filling a region
def flood_fill_plain(image, xy, value, thresh=0):
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
        new_edge = []
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if color_diff(p, background) <= thresh:
                        pixel[s, t] = value
                        new_edge.append((s, t))
        edge = new_edge


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
    edge = {(x, y)}
    full_edge = set()
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (s,t) in full_edge:
                    continue
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if color_diff(p, background) <= thresh:
                        pixel[s, t] = value
                        new_edge.add((s, t))
                        full_edge.add((s, t))
        edge = new_edge


def rip_bg_with_chroma_key(img, tol, caption_text=None):
    plt.figure("Image")
    plt.imshow(img)
    print("Please click a spot to identify the color to remove")
    coordinates = plt.ginput(1)[0]
    x = round(coordinates[0])
    y = round(coordinates[1])
    if img.getpalette() is not None:
        # then the image is based on palette coloring
        print('not none palette.')
        img = img.convert(mode='RGBA')

    flood_fill(img, (x, y), (0, 0, 0, 0), thresh=tol)
    if caption_text is not None:
        img = draw_text(img, caption_text, (x, y))

    alpha = img.split()[3]
    out = img.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    out.paste(255, mask=mask)

    # out = img
    plt.close()
    return out


def rip_bg_with_chroma_key_frame0(img, tol, caption_text=None):

    plt.figure("Image")
    plt.imshow(img)
    print("Please click a spot to identify the color to remove")
    coordinates = plt.ginput(1)[0]
    x = round(coordinates[0])
    y = round(coordinates[1])
    if img.getpalette() is not None:
        # then the image is based on palette coloring
        print('not none palette.')
        img = img.convert(mode='RGBA')
    pixel = np.array(img.getpixel((x, y)))

    # flood_fill(img, (x, y), (0, 0, 0, 0), thresh=tol)
    flood_fill(img, (x, y), (0, 0, 0, 0), thresh=tol)

    if caption_text is not None:
        img = draw_text(img, caption_text, (x, y))

    alpha = img.split()[3]
    out = img.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    out.paste(255, mask=mask)
    prev_colors = len(out.getcolors())
    # plt.clf()
    # plt.imshow(img)
    # plt.ginput(1)
    plt.close()
    return out, pixel, (x, y), prev_colors


def rip_bg_with_chroma_key_auto(img, tol, coordinates, caption_text=None, prev_colors=None):
    if img.getpalette() is not None:
        print('Not none palette')
        print(len(img.getcolors()))
        if len(img.getcolors()) < 255:  # not full palette
            if prev_colors != len(img.getcolors()):  # the most tricky case: different palette
                print('the most tricky case: different palette')
                col = 128
            else:
                col = len(img.getcolors())
        else:
            col = 255
        # then the image is based on palette coloring
        img = img.convert(mode='RGBA')
        flood_fill(img, coordinates, (0, 0, 0, 0), thresh=tol)

        if caption_text is not None:
            img = draw_text(img, caption_text, coordinates)

        alpha = img.split()[3]
        out = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=col)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        out.paste(255, mask=mask)
        co = out.getcolors()
        print(len(co))
        # out = out.convert('RGBA')
        # plt.clf()
        # plt.imshow(out)
        # plt.ginput(1)
        return out

    flood_fill(img, coordinates, (0, 0, 0, 0), thresh=tol)

    if caption_text is not None:
        img = draw_text(img, caption_text, coordinates)

    alpha = img.split()[3]
    out = img.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    out.paste(255, mask=mask)
    # arr = out.getpalette()
    # print(arr[:18])
    # print(arr[-18:])
    # plt.imshow(out)
    # plt.ginput(1)
    # plt.close()
    #
    # arr = np.array(out)

    # print(arr[:])

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


def flood_fill2(image, xy, value, thresh=0):
    arr = np.array(image)
    x1, y1 = xy
    y = int(x1)
    x = int(y1)
    val = np.array(value)
    try:
        background = arr[x, y, :].copy()   # it's a pointer?!
        if color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        arr[x, y, :] = val
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = [(x, y)]
    while edge:
        new_edge = []
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                try:
                    p = arr[s, t, :]
                except IndexError:
                    pass
                else:
                    if color_diff(p.tolist(), background.tolist()) <= thresh:
                        arr[s, t, :] = val
                        new_edge.append((s, t))
        edge = new_edge
    out = Image.fromarray(arr)
    return out
    
    
def rgb_bounding(colors):
    for color in range(len(colors)):
        if colors[color] > 255:
            colors[color] = 255
            continue
        elif colors[color] < 0:
            colors[color] = 0
            continue
    return colors


'''
