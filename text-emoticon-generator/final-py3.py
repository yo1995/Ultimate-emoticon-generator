# -*- coding: utf-8 -*-

import os
import sys
import re
import string
import math
from PIL import Image, ImageFont, ImageDraw


def validate_title(title):
    rstr = r'[\\/:*?"<>|]'  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title).replace('\n', '')
    return new_title


if __name__ == '__main__':
    # x y position at upper left
    x = 1
    y = 1
    font_color = '#A12306'
    font_size = 100
    font_path = 'C:/Windows/Fonts/STZHONGS.TTF'  # C:/Windows/Fonts/YaHeiMonacoHybird.ttf# C:/Windows/Fonts/STZHONGS.TTF
    outline = 2  # stands for px around the text
    outline_color = "#111"  # always pick a darker outline to achieve better view
    outline_antialias_rate = 8  # 8 should be a reasonable biggest number for 4 lines or less.

    # edit things below with caution.
    char_len = 0
    max_len = 0
    lines = int(input(u'请输入行数：\n'))
    ascii_character_width_rate = 0.4
    text = ''
    current_dir = sys.path[0]

    for line in range(lines):
        temp_len = 0
        line_str = input(u'请输入需要转化的文字第' + str(line + 1) + '行：\n')
        for asc in line_str:
            if asc in string.ascii_letters:
                temp_len = temp_len + 1
        temp_len = len(line_str) - ascii_character_width_rate * temp_len
        max_len = temp_len if temp_len > max_len else max_len
        text = text + line_str + "\n"

    for char in text:
        if char in string.ascii_letters:
            char_len = char_len + 1

    if lines == 1:
        width = font_size * int(len(text) - ascii_character_width_rate * char_len - 0.45)
        height = int(font_size + 0.3 * font_size)
        im = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 0.5 for \n but remain some space
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", font_path), font_size)
        for i in range(outline_antialias_rate):
            for j in range(outline_antialias_rate):
                dr.text((x + outline / (j + 1), y - outline / (i + 1)), text, font=font, fill=outline_color, align='center')
                dr.text((x + outline / (j + 1), y + outline / (i + 1)), text, font=font, fill=outline_color, align='center')
                dr.text((x - outline / (j + 1), y - outline / (i + 1)), text, font=font, fill=outline_color, align='center')
                dr.text((x - outline / (j + 1), y + outline / (i + 1)), text, font=font, fill=outline_color, align='center')
        dr.text((x, y), text, font=font, fill=font_color, align='center')
        filename = text

    else:
        im = Image.new("RGBA", (int(font_size * max_len), int(lines * (1.2 * font_size) + 0.3 * font_size)), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", font_path), font_size)
        for i in range(outline_antialias_rate):
            for j in range(outline_antialias_rate):
                dr.multiline_text((x + outline / (j + 1), y - outline / (i + 1)), text, font=font, spacing=20, fill=outline_color, align='center')
                dr.multiline_text((x + outline / (j + 1), y + outline / (i + 1)), text, font=font, spacing=20, fill=outline_color, align='center')
                dr.multiline_text((x - outline / (j + 1), y - outline / (i + 1)), text, font=font, spacing=20, fill=outline_color, align='center')
                dr.multiline_text((x - outline / (j + 1), y + outline / (i + 1)), text, font=font, spacing=20, fill=outline_color, align='center')

        dr.multiline_text((x, y), text, font=font, fill=font_color, spacing=20, align='center')
        filename = text if len(text) < 6 else text[:6]

    alpha = im.split()[3]
    out = im.convert('RGB').convert('P', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=16)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    out.paste(255, mask=mask)
    transparency = 255
    out.save(current_dir + '/' + validate_title(filename) + ".gif", transparency=transparency)
    # input(u'表情已生成，任意键结束！')
