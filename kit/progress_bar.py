#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time


def progress_bar(desc: str, index: int, total: int, bar_len: int = 40, light: str = "━", dark: str = "-"):
    """
    :param desc: 进度条的描述文字
    :param index: 数据前进进度
    :param total: 数据长度
    :param bar_len: 进度条的长度, 默认40
    :param light: 表示已完成的字符,如█, ━,💚💗,🟢
    :param dark: 表示未完成的字符,如 ,-,🤍,⚪
    :return:
    """
    rate = index / total
    if rate > 1:
        rate = 1
    forward = int(rate * bar_len)
    tofu = forward * light + int(bar_len - forward) * dark
    msg = f"\r{desc}{tofu} {rate * 100:.2f}% | {index}/{total} "
    print(msg, end="")


if __name__ == '__main__':
    for i in range(1, 201):
        progress_bar("Download: ", i, 200)
        time.sleep(0.01)
    print()

    for i in range(1, 201):
        progress_bar("Download: ", i, 200, light="█", dark=" ")
        time.sleep(0.01)
    print()

    for i in range(1, 201):
        progress_bar("Download: ", i, 200, light="🟢", dark="⚪", bar_len=20)
        time.sleep(0.01)
    print()

    for i in range(1, 201):
        progress_bar("Download: ", i, 200, light="💗", dark="🤍", bar_len=20)
        time.sleep(0.01)
    print()

    for i in range(1, 201):
        progress_bar("Download: ", i, 200, light="😴", dark="🙄", bar_len=20)
        time.sleep(0.01)
    print()
