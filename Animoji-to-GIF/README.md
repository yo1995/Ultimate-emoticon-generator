↓ Logo@3.8MB 

![logo](./logo.gif)

## PyQt 安装与配置

1. 打开PyCharm，设置，解释器，添加新的依赖库

	pip install pyqt5
	pip install pyqt5-tools

其中第一个是PyQt的总库，[第二个](https://github.com/altendky/pyqt5-tools)包含了对QtDesigner的配置。

2. 在PyCharm中配置external tools以实现界面编辑，程序路径为

	Program: C:\Program Files\Python36\Lib\site-packages\pyqt5-tools\designer.exe
	Working Directory: $ProjectFileDir$

3. 设置Qt .ui界面文件转换为.py文件的命令 PyUICon

	Program: C:\Program Files\Python36\python.exe
	Parameters: -m PyQt5.uic.pyuic $ProjectFileDir$\$FileName$ -o $ProjectFileDir$\$FileNameWithoutExtension$.py

	注：我的习惯是把文件全扔在项目文件夹的根目录下。可根据个人喜好自行定制上面的命令。

每次绘制界面并保存为.ui文件后手动执行PyUICon即可，并在.py文件中import对应界面

## tqdm

一个轻量化的命令行进度条，可以插入运行较慢的程序

## grayconnected/floodfill

```python
def color_diff(rgba1, rgba2):
    if len(rgba1) == 3 and len(rgba2) == 3:
        return abs(rgba1[0] - rgba2[0]) + abs(rgba1[1] - rgba2[1]) + abs(rgba1[2] - rgba2[2])
    try:
        euc_length = abs(rgba1[0]-rgba2[0]) + abs(rgba1[1]-rgba2[1]) + abs(rgba1[2]-rgba2[2]) + abs(rgba1[3]-rgba2[3])
    except IndexError:
        return
    else:
        return euc_length

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
```


## what's in a GIF 

http://www.matthewflickinger.com/lab/whatsinagif/bits_and_bytes.asp

### 目前仅支持256色

如果需要缩减颜色，则需要提供关于透明度下标的设置。

http://www.pythonclub.org/modules/pil/convert-png-gif

optimize transparency

use single palette


## Features

### Animoji to GIF

### 文字表情包生成器


## Windows复制路径小贴士

1. 按住 SHIFT + 鼠标右键，可以看到多了一项 “复制到路径” 选项。

2. 只要点击 “复制到路径”，路径就复制到剪贴板中了, 然后就可以粘贴了。


色彩数不到256的动态图

Issues about PIL GIF dither RGB RGBA P and convert

每一帧用local palette，如果转为通用的palette，那么有的index原来对应有颜色，现在变成没有颜色了

三步走：

视频

palette相同的GIF

palette变化的GIF

人脸三维建模的难点

人脸识别：CLM

三维建模：Unity和特征点的映射

三维的缺失：噘嘴

输出成流媒体