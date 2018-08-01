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
    zihao = 100
    char_len = 0
    max_len = 0
    lines = int(input(u'请输入行数：\n'))
    ascii_character_width_rate = 0.4
    text = ''
    current_dir = sys.path[0]
    img = Image.open(current_dir + '/1.gif')
    transparency = img.info['transparency']
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
        im = Image.new("RGBA", (zihao*int(len(text) - ascii_character_width_rate * char_len), zihao + 30), (0, 0, 0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", "C:/Windows/Fonts/STZHONGS.TTF"), zihao)  # C:/Windows/Fonts/YaHeiMonacoHybird.ttf  # C:/Windows/Fonts/STZHONGS.TTF
        dr.text((1, 1), text, font=font, fill="#111", align='center')
        filename = text
    else:
        im = Image.new("RGBA", (int(zihao * max_len), lines * (zihao + 20) + 30), (0, 0, 0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(os.path.join("fonts", "C:/Windows/Fonts/STZHONGS.TTF"), zihao)
        dr.multiline_text((1, 1), text, font=font, fill="#111", spacing=20, align='center')
        filename = text if len(text) < 6 else text[:6]

    im.save(current_dir + '/' + validate_title(filename) + ".gif", transparency=transparency)
    # input(u'表情已生成，任意键结束！')
