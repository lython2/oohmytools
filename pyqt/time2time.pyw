#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from bson.objectid import ObjectId
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def time_convert_str2int(date_string: str):
    """字符串时间转数字"""
    date_time = datetime.fromisoformat(date_string)
    timestamp = int(date_time.timestamp())
    return timestamp


def time_convert_int2str(timestamp: int, style: str = "%Y-%m-%d %H:%M:%S") -> str:
    """数字时间转字符串"""
    date_time = datetime.fromtimestamp(timestamp)
    date_string = date_time.strftime(style)
    return date_string


def friend_time(line):
    if ":" in line or "/" in line or "-" in line:
        ret = time_convert_str2int(line)
        return str(ret)
    try:
        digit = float(line)
    except Exception as e:
        print(e)
        return None
    if digit > 1000000000000:
        digit = digit / 1000
    digit = int(digit)
    ret = time_convert_int2str(digit)
    return ret


class Time2TimeWindow(QFrame):

    def __init__(self):
        super(Time2TimeWindow, self).__init__()

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.setWindowTitle("T2T")
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.SP_DesktopIcon)))

        self.desktop = QApplication.desktop()
        self.screen_width = self.desktop.width() // 3
        self.screen_height = self.desktop.height() // 3
        self.resize(self.screen_width, self.screen_height)

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        self.text_time = QLineEdit(self)
        self.text_time.setClearButtonEnabled(True)

        self.btn_now = QPushButton("此刻", self)
        self.btn_now.clicked.connect(self.btn_now_click)
        
        self.btn_calc = QPushButton("计算", self)
        self.btn_calc.clicked.connect(self.btn_calc_click)

        self.btn_convert = QPushButton("转换", self)
        self.btn_convert.clicked.connect(self.btn_convert_click)

        layout = QGridLayout()
        layout.addWidget(self.text_time, 0, 0)
        layout.addWidget(self.btn_now, 0, 1)
        layout.addWidget(self.btn_calc, 0, 2)
        layout.addWidget(self.btn_convert, 0, 3)
        layout.addWidget(self.text, 1, 0, 1, 4)

        self.setLayout(layout)

    def btn_calc_click(self):
        line = str(self.text_time.text())
        try:
            txt = friend_time(line)
        except Exception as e:
            txt = e
        self.text.setText(str(txt))

    def btn_now_click(self):
        self.text_time.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.text.setText(str(time.time()))

    def btn_zero_click(self):
        now = datetime.now()
        today = datetime(now.year, now.month, now.day)
        self.text_time.setText(today.strftime("%Y-%m-%d %H:%M:%S"))
        self.text.setText(str(today.timestamp()))

    def btn_convert_click(self):
        text = str(self.text_time.text())
        value = ""
        if "-" in text:
            try:
                digital = time_convert_str2int(text)
            except Exception as e:
                value = str(e)
            else:
                value = ObjectId().from_datetime(datetime.fromtimestamp(digital))
        elif len(text) == 24:
            try:
                obj = ObjectId(text)
                value = obj.generation_time
            except Exception as e:
                value = str(e)
        self.text.setText(str(value))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    frm = Time2TimeWindow()
    frm.show()
    sys.exit(app.exec_())
