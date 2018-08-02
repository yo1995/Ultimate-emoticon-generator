# -*- coding: utf-8 -*-

import os
import string
from PIL import Image, ImageFont, ImageDraw


def draw_text(img, caption_text, xy):
    # x y position at upper left
    x, y = xy
    font_color = '#A12306'
    font_size = 100
    font_path = 'C:/Windows/Fonts/STZHONGS.TTF'  # C:/Windows/Fonts/YaHeiMonacoHybird.ttf# C:/Windows/Fonts/STZHONGS.TTF
    outline = 2  # stands for px around the text
    outline_color = "#000"  # always pick a darker outline to achieve better view
    outline_antialias_rate = 5  # 8 should be a reasonable biggest number for 4 lines or less.

    # edit things below with caution.
    char_len = 0
    max_len = 0
    lines = 1
    ascii_character_width_rate = 0.4
    text = caption_text

    for line in range(lines):
        temp_len = 0
        line_str = ''
        for asc in line_str:
            if asc in string.ascii_letters:
                temp_len = temp_len + 1
        temp_len = len(line_str) - ascii_character_width_rate * temp_len
        max_len = temp_len if temp_len > max_len else max_len
        text = text + line_str + "\n"

    for char in text:
        if char in string.ascii_letters:
            char_len = char_len + 1

    dr = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join("fonts", font_path), font_size)
    for i in range(outline_antialias_rate):
        for j in range(outline_antialias_rate):
            dr.text((x + outline / (j + 1), y - outline / (i + 1)), text, font=font, fill=outline_color, align='center')
            dr.text((x + outline / (j + 1), y + outline / (i + 1)), text, font=font, fill=outline_color, align='center')
            dr.text((x - outline / (j + 1), y - outline / (i + 1)), text, font=font, fill=outline_color, align='center')
            dr.text((x - outline / (j + 1), y + outline / (i + 1)), text, font=font, fill=outline_color, align='center')
    dr.text((x, y), text, font=font, fill=font_color, align='center')

    return img
    # input(u'表情已生成，任意键结束！')
