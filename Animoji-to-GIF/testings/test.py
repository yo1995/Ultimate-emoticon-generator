import sys
import os
import e_optimization_with_gifsicle as step5
import time


# 应该在读取写入文件名前检查是否合规，最后整合时再添加
cwd = sys.path[0]
os.environ['IMAGEIO_FFMPEG_EXE'] = r'C:\Users\yo-ch\Documents\ShareX\Tools\ffmpeg.exe'  # to set your ffmpeg path
now_time = time.strftime('%H%M%S', time.localtime(time.time()))
tol = 15  # 15 for video
quantize = 16  # quantize to colors. just let user to decide. 0 or neg to ignore
further_optimize = True
ms_for_video = 33  # in milisecond format.
total_frames_limitation = 240
additional_args = '--colors 128 --resize-width 320'  # additional arguments for optimization


input_file_dir = r'C:\Users\yo-ch\Desktop\表情包制作器想法\MJIQ2782.mp4'  # pig.mp4
save_filename = 'C:/Users/yo-ch/Desktop/表情包制作器想法/173550-result.gif'
save_filename_optimized = 'C:/Users/yo-ch/Desktop/表情包制作器想法/' + now_time + '-result-optimized.gif'
transparent_gif_bg_path = r'C:\Users\yo-ch\Desktop\表情包制作器想法\emoticon_py\bg.gif'

step5.gif_general_optimization(cwd, save_filename, save_filename_optimized, additional_args, 3)
