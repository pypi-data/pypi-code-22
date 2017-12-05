"""
Copyright 1999 Illinois Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL ILLINOIS INSTITUTE OF TECHNOLOGY BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of Illinois Institute
of Technology shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Software without prior written
authorization from Illinois Institute of Technology.
"""

import os
from os.path import split, exists, join
import fabio

def getFilesAndHdf(dir_path):
    fileList = os.listdir(dir_path)
    imgList = []
    hdfList = []

    for f in fileList:
        full_file_name = fullPath(dir_path, f)
        if isImg(full_file_name):
            imgList.append(f)
            # if calculate_med_img:
            #     tmp_images.append(fabio.open(full_file_name).data)
        else:
            toks = f.split('.')
            if toks[-1] == 'hdf':
                hdfList.append(f)

    return imgList, hdfList

def getBlankImageAndMask(path):
    mask_file = join(join(path, 'settings'),'mask.tif')
    blank_file = join(join(path, 'settings'),'blank.tif')
    mask = None
    blank_img = None
    if exists(mask_file):
        mask = fabio.open(mask_file).data
    if exists(blank_file):
        blank_img = fabio.open(blank_file).data
    return blank_img, mask

def getImgFiles(fullname):
    """
    Get directory, all image file names in the same directory and current file index
    :param fullname: full name of the file including directory i.e. /aaa/bbb/ccc/ddd.tif (str)
    :return: directory (str), list of image file names, and current index i.e /aaa/bbb/ccc, ["ddd.tif","eee.tif"], 0
    """

    dir_path, filename = split(str(fullname)) # split directory and file name from full file name
    dir_path = str(dir_path)
    filename = str(filename)
    _, ext = os.path.splitext(str(filename))
    current = 0
    failedcases = []

    if ext == ".txt":
        for line in open(fullname, "r"):
            failedcases.append(line.rstrip('\n'))
    else:
        failedcases = None

    fileList = os.listdir(dir_path)
    imgList = []

    for f in fileList:
        if failedcases is not None and f not in failedcases:
            continue
        full_file_name = fullPath(dir_path, f)
        if isImg(full_file_name) and f != "calibration.tif":
            imgList.append(f)

    imgList.sort()

    if failedcases is None:
        current = imgList.index(filename)

    return dir_path, imgList, current

def fullPath(filePath, fileName):
    """
    Combile a path and file name to get full file name
    :param filePath: directory (string)
    :param fileName: file name (string)
    :return: filePath/filename (string)
    """
    if filePath[-1] == '/':
        return filePath+fileName
    else:
        return filePath+"/"+fileName

def isImg(fileName):
    """
    Check if a file name is an image file
    :param fileName: (str)
    :return: True or False
    """
    # imgList = ['bmp','jpg','tif','tiff','png','jpeg']
    imgList = ['tif', 'tiff']
    nameList = fileName.split('.')
    if nameList[-1] in imgList:
        return True
    else:
        return False


def createFolder(path):
    """
    Create a folder if it doesn't exist
    :param path: full path of creating directory
    :return:
    """
    if not exists(path):
        os.makedirs(path)

def getStyleSheet():
    """
    Get style sheet from stylesheet.txt
    :return: styesheet (str) or empty string if it's not available
    """
    return "QToolTip{     border: 1px solid black;     background-color: #ffa02f;     padding: 1px;     border-radius: 3px;     opacity: 100;} " \
           "QWidget {    color: #cecece;    background-color: #323232; }" \
           "QWidget:item:selected{    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}" \
           "QMenuBar::item{    background: transparent;}" \
           "QMenuBar::item:selected{    background: transparent;    border: 1px solid #ffaa00;}" \
           "QMenuBar::item:pressed{    background: #6d6d6d;    border: 1px solid #000;    background-color: QLinearGradient(        x1:0, y1:0,        x2:0, y2:1,        stop:1 #212121,        stop:0.4 #343434/*,        stop:0.2 #343434,        stop:0.1 #ffaa00*/    );    margin-bottom:-1px;    padding-bottom:1px;}" \
           "QMenu{    border: 1px solid #000;}" \
           "QMenu::item{    padding: 2px 20px 2px 20px;}" \
           "QMenu::item:selected{    color: #000000;}" \
           "QWidget:disabled{    color: #777676;    background-color: #323232;}" \
           "QAbstractItemView{    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);}" \
           "QLineEdit{    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);    padding: 1px;    border-style: solid;    border: 1px solid #1e1e1e;    border-radius: 5;}" \
           "QPushButton{    color: #cecece;    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);    border-width: 1px;    border-color: #1e1e1e;    border-style: solid;    border-radius: 6;    padding: 3px;    font-size: 12px;    padding-left: 5px;    padding-right: 5px; height: 15px;}" \
           "QPushButton:pressed{    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);}" \
           "QPushButton:checked{    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);}" \
           "QComboBox{    selection-background-color: #ffaa00;    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);    border-style: solid;    border: 1px solid #1e1e1e;    border-radius: 5;}" \
           "QComboBox:hover,QPushButton:hover{    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #51300a);}" \
           "QComboBox:on{    padding-top: 3px;    padding-left: 4px;    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);    selection-background-color: #ffaa00;}" \
           "QComboBox QAbstractItemView{    border: 2px solid darkgray;    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}" \
           "QComboBox::drop-down{     subcontrol-origin: padding;     subcontrol-position: top right;     width: 15px;     border-left-width: 0px;     border-left-color: darkgray;     border-left-style: solid; /* just a single line */     border-top-right-radius: 2px; /* same radius as the QComboBox */     border-bottom-right-radius: 2px; }" \
           "QGroupBox { border: 1px solid gray; border-radius: 2px; margin-top: 1ex; }" \
           "QGroupBox::indicator{    color: #cecece;    background-color: #323232;    border: 1px solid #cecece;    width: 9px;    height: 9px;}" \
           "QGroupBox::indicator:disabled, QRadioButton::indicator:disabled{    border: 1px solid #6d6d6d;}" \
           "QGroupBox::indicator:checked{    background-color: #f77213;}" \
           "QGroupBox::title { background-color: #323232 ; subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; }" \
           "QTextEdit:focus{    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}" \
           "QScrollBar:horizontal {     border: 1px solid #222222;     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);     height: 7px;     margin: 0px 16px 0 16px;}" \
           "QScrollBar::handle:horizontal{      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);      min-height: 20px;      border-radius: 2px;}" \
           "QScrollBar::add-line:horizontal {      border: 1px solid #1b1b19;      border-radius: 2px;      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);      width: 14px;      subcontrol-position: right;      subcontrol-origin: margin;}" \
           "QScrollBar::sub-line:horizontal {      border: 1px solid #1b1b19;      border-radius: 2px;      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);      width: 14px;     subcontrol-position: left;     subcontrol-origin: margin;}" \
           "QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal{      border: 1px solid black;      width: 1px;      height: 1px;      background: white;}" \
           "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{      background: none;}" \
           "QScrollBar:vertical{      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);      width: 7px;      margin: 16px 0 16px 0;      border: 1px solid #222222;}" \
           "QScrollBar::handle:vertical{      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);      min-height: 20px;      border-radius: 2px;}" \
           "QScrollBar::add-line:vertical{      border: 1px solid #1b1b19;      border-radius: 2px;      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);      height: 14px;      subcontrol-position: bottom;      subcontrol-origin: margin;}" \
           "QScrollBar::sub-line:vertical{      border: 1px solid #1b1b19;      border-radius: 2px;      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);      height: 14px;      subcontrol-position: top;      subcontrol-origin: margin;}" \
           "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{      border: 1px solid black;      width: 1px;      height: 1px;      background: white;}" \
           "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{      background: none;}" \
           "QTextEdit{    background-color: #242424;}" \
           "QPlainTextEdit{    background-color: #242424;}" \
           "QHeaderView::section{    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);    color: white;    padding-left: 4px;    border: 1px solid #6c6c6c;}" \
           "QCheckBox:disabled{ color: #414141;}" \
           "QDockWidget::title{    text-align: center;    spacing: 3px; /* spacing between items in the tool bar */    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);}" \
           "QDockWidget::close-button, QDockWidget::float-button{    text-align: center;    spacing: 1px; /* spacing between items in the tool bar */    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);}" \
           "QDockWidget::close-button:hover, QDockWidget::float-button:hover{    background: #242424;}" \
           "QDockWidget::close-button:pressed, QDockWidget::float-button:pressed{    padding: 1px -1px -1px 1px;}" \
           "QMainWindow::separator{    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);    color: white;    padding-left: 4px;    border: 1px solid #4c4c4c;    spacing: 3px; /* spacing between items in the tool bar */}" \
           "QMainWindow::separator:hover{    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);    color: white;    padding-left: 4px;    border: 1px solid #6c6c6c;    spacing: 3px; /* spacing between items in the tool bar */}" \
           "QMenu::separator{    height: 2px;    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);    color: white;    padding-left: 4px;    margin-left: 10px;    margin-right: 5px;}" \
           "QProgressBar{    border: 2px solid grey;    border-radius: 5px;    text-align: center;}" \
           "QProgressBar::chunk{    background-color: #d7801a;    width: 2.15px;    margin: 0.5px;}" \
           "QTabBar::tab {    color: #cecece;    border: 1px solid #6d6d6d;    border-bottom-style: none;    background-color: #323232;    padding-left: 10px;    padding-right: 10px;    padding-top: 3px;    padding-bottom: 2px;    margin-right: -1px;}" \
           "QTabWidget::pane {    border: 1px solid #6d6d6d;    top: 1px;}" \
           "QTabBar::tab:last{    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */    border-top-right-radius: 3px;}" \
           "QTabBar::tab:first:!selected{ margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */    border-top-left-radius: 3px;}" \
           "QTabBar::tab:!selected{    color: #cecece;    border-bottom-style: solid;    margin-top: 3px;    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);}" \
           "QTabBar::tab:selected{    border-top-left-radius: 3px;    border-top-right-radius: 3px;    margin-bottom: 0px;}" \
           "QTabBar::tab:!selected:hover{    /*border-top: 2px solid #ffaa00;    padding-bottom: 3px;*/    border-top-left-radius: 3px;    border-top-right-radius: 3px;    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);}" \
           "QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{    color: #cecece;    background-color: #323232;    border: 1px solid #cecece;    border-radius: 6px;}" \
           "QRadioButton::indicator:checked{    background-color: qradialgradient(        cx: 0.5, cy: 0.5,        fx: 0.5, fy: 0.5,        radius: 1.0,        stop: 0.25 #ffaa00,        stop: 0.3 #323232    );}" \
           "QRadioButton::indicator{border-radius: 6px;}" \
           "QRadioButton::indicator:hover, QCheckBox::indicator:hover{    border: 1px solid #ffaa00;}" \
           "QCheckBox::indicator{    color: #cecece;    background-color: #323232;    border: 1px solid #cecece;    width: 9px;    height: 9px;}" \
           "QCheckBox{ width: 20px; }" \
           "QCheckBox::indicator:disabled, QRadioButton::indicator:disabled{    border: 1px solid #6d6d6d;}" \
           "QCheckBox::indicator:checked{    background-color: #f77213;}"