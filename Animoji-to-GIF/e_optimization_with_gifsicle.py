import os


def gif_general_optimization(cwd, in_file, out_file, additional_args, o_level, gifsicle_path):
    if o_level == 1:
        o_level_s = ' -O1 '
    elif o_level == 2:
        o_level_s = ' -O2 '
    elif o_level == 3:
        o_level_s = ' -O3 '
    else:
        o_level_s = ' -O1 '  # default

    if os.path.exists(gifsicle_path):
        os.system(gifsicle_path + o_level_s + additional_args + ' -i ' + in_file + ' -o ' + out_file)
    else:
        print('gifsicle not exists! check your installation.')
