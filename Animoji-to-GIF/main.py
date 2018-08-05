# -*- coding:utf-8 -*-

__author__ = 'cht'
'''
主模块

thoughts: 
- 需要添加打开关闭检测
- # 应该在读取写入文件名前检查是否合规，最后整合时再添加
credits:
- 
'''

# system modules
import sys
import re
import os
import multiprocessing
import time
import configparser
# import emoticon_main
# from PyQt5.QtWidgets import QApplication, QMainWindow

# submodules
import a_read_data_from_media_file as step1
import b_decode_image as step21
import b_decode_video as step22
import c_chroma_key_rip_background as step3
import d_save_image_file as step4
import e_optimization_with_gifsicle as step5



'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = emoticon_main.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
'''


cwd = sys.path[0]
now_time = time.strftime('%H%M%S', time.localtime(time.time()))

conf = configparser.ConfigParser()
conf.read(cwd + '/emoticon_settings.conf', encoding='utf-8')
# v1 = conf.getint('config', 'v1')
# v3 = conf.getboolean('config', 'v3')
# v4 = conf.getfloat('config', 'v4')

# obsolete
transparent_gif_bg_path = cwd + conf.get('path', 'transparent_gif_bg_path')
quantize                = conf.getint('variables', 'quantize')  # quantize to colors. just let user to decide. 0 or neg to ignore


output_dir              = conf.get('path', 'output_dir')
external_tools_dir      = conf.get('path', 'external_tools_dir')
input_file_dir          = conf.get('path', 'input_dir')
save_filename           = cwd + output_dir + now_time + conf.get('path', 'save_filename')
save_filename_optimized = cwd + output_dir + now_time + conf.get('path', 'save_filename_optimized')

monster_path            = cwd + conf.get('path', 'monster_path')
gifsicle_path           = cwd + external_tools_dir + 'gifsicle-1.89-win64/gifsicle.exe'

tol                     = conf.getint('variables', 'tolerance')  # 15 for video, 10 for photos

ms_for_video            = conf.getint('variables', 'ms_for_video')  # in milisecond format.
further_optimize        = conf.getboolean('booleans', 'further_optimize')
crop                    = conf.getboolean('booleans', 'crop')

total_frames_limitation = conf.getint('variables', 'total_frames_limitation')  # take the first # frames from the whole clip
additional_args         = conf.get('additional', 'additional_args')  # additional arguments for optimization
caption_text            = conf.get('additional', 'caption_text')

os.environ['IMAGEIO_FFMPEG_EXE'] = conf.get('path', 'ffmpeg_dir')
crop_box = (0,150,720,950)


def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title


if __name__ == '__main__':
    # step1
    input_file_dir = str(input(u'请输入文件路径（支持直接拖拽到命令行窗口，不填写默认为读取配置文件）：\n'))
    if input_file_dir is None:
        # read conf file
        print('read conf file!')
        input_file_dir = conf.get('path', 'input_dir')
        if input_file_dir is None:
            # read from stdin
            print('read sys argv!')
            input_file_dir = sys.argv[1]
            # im angry!
            if input_file_dir is None:
                print('some file path must exist!')
                input_file_dir = monster_path
    file_type = step1.judge_file_extension(cwd + input_file_dir)

    # step234
    if file_type == 1:  # image file jpg or png
        img = step21.decode_static_image_file(input_file_dir)
        img_out = step3.rip_bg_with_chroma_key(img, tol, caption_text=caption_text)
        step4.save_img_file_as_static_gif_with_alpha(img_out, transparent_gif_bg_path, save_filename, quantize)

    if file_type == 2:  # video file
        # more to add in the future
        pool1 = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # use up all the cores.
        version = 'GIF89a'
        duration = 33

        img_stack = step22.decode_video_file(input_file_dir, crop, crop_box)
        frame0, pixel, coord, prev_colors = step3.rip_bg_with_chroma_key_frame0(img_stack[0], tol, caption_text=caption_text)
        img_stack.pop(0)
        # stacked_frames = []
        # for img in img_stack:
        #     current_frame = step3.rip_bg_with_chroma_key_auto(img, tol, pixel, coord, caption_text=caption_text)
        #
        #     stacked_frames.append(current_frame)
        frames_to_process = min(len(img_stack), total_frames_limitation)
        stacked_frames = [None] * frames_to_process
        for i in range(frames_to_process):  # to limit the max frames
            print('put in pool frame: ' + str(i + 1))
            stacked_frames[i] = pool1.apply_async(step3.rip_bg_with_chroma_key_auto, args=(img_stack[i], tol, coord, caption_text, None)).get()

        pool1.close()
        pool1.join()
        step4.save_img_file_as_animated_gif_with_alpha(frame0, stacked_frames, transparent_gif_bg_path, save_filename,
                                                       version, duration)

    if file_type == 3:  # animated/static gif
        (img, multi_frame) = step21.decode_gif_file(input_file_dir)
        if multi_frame == 1:  # is a single frame GIF
            img_out = step3.rip_bg_with_chroma_key(img, tol, caption_text=caption_text)
            step4.save_img_file_as_static_gif_with_alpha(img_out, transparent_gif_bg_path, save_filename, quantize)
        else:  # is a animated GIF
            current_index = 0
            current_frame = img
            version = img.info.get('version')
            duration = img.info.get('duration')
            stacked_frames = []
            # frame0 = step3.rip_bg_with_chroma_key(current_frame, tol, caption_text=caption_text)
            frame0, pixel, coord, prev_colors = step3.rip_bg_with_chroma_key_frame0(current_frame, tol, caption_text=caption_text)
            # loop over all the frames
            try:
                while 1:
                    current_index = img.tell() + 1
                    print('current frame is:' + str(current_index))
                    img.seek(current_index)
                    # current_frame = step3.rip_bg_with_chroma_key(img, tol, caption_text=caption_text)
                    current_frame = step3.rip_bg_with_chroma_key_auto(img, tol, coord, caption_text=caption_text, prev_colors=None)
                    stacked_frames.append(current_frame)
            except EOFError:
                pass  # end of sequence
                print('already reached the end of frames. output now.')
                step4.save_img_file_as_animated_gif_with_alpha(frame0, stacked_frames, transparent_gif_bg_path, save_filename, version, duration)

    step5.gif_general_optimization(cwd, save_filename, save_filename_optimized, additional_args, 3, gifsicle_path)


