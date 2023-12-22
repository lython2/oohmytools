#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QGuiApplication, QIcon, QFont
from PyQt5.QtCore import QTimer, Qt


class Clipboard2(QMainWindow):

    def __init__(self):
        super(Clipboard2, self).__init__()

        self.setWindowTitle("Clipboard2")
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.SP_DesktopIcon)))
        self.desktop = QApplication.desktop()

        self.screen_width = self.desktop.width() // 4
        self.screen_height = self.desktop.height() // 2
        self.resize(self.screen_width, self.screen_height)

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.text = QTextEdit(self)
        self.label_info = QLabel(self)

        self.btn_show = QAction(QIcon(self.style().standardIcon(QStyle.SP_DesktopIcon)), "显示", self)
        self.btn_show.triggered.connect(self.showNormal)

        self.btn_start = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogYesButton)), "运行中", self)
        self.btn_start.setCheckable(True)
        self.btn_start.setChecked(True)
        self.btn_start.triggered.connect(self.btn_start_click)

        self.btn_top = QAction(QIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton)), "置顶", self)
        self.btn_top.setCheckable(True)
        self.btn_top.triggered.connect(self.btn_top_click)

        self.btn_sort = QAction(QIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView)), "排序", self)
        self.btn_sort.triggered.connect(self.btn_sort_click)

        self.btn_clear = QAction(QIcon(self.style().standardIcon(QStyle.SP_TrashIcon)), "清空", self)
        self.btn_clear.triggered.connect(self.btn_clear_click)

        self.btn_save = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)), "保存", self)
        self.btn_save.triggered.connect(self.btn_save_click)

        self.btn_close = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton)), "关闭", self)
        self.btn_close.triggered.connect(sys.exit)

        toolbar_top = QToolBar("工具栏", self)
        toolbar_top.setMovable(False)
        toolbar_top.addAction(self.btn_start)
        toolbar_top.addAction(self.btn_top)
        toolbar_top.addAction(self.btn_sort)
        toolbar_top.addAction(self.btn_save)
        toolbar_top.addSeparator()
        toolbar_top.addAction(self.btn_clear)
        toolbar_top.addAction(self.btn_close)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("ClipboardMe2: 运行中")
        self.tray_icon.activated.connect(self.tray_icon_click)
        self.tray_icon.setContextMenu(self.menu_context_menu())
        self.tray_icon.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogYesButton)))
        self.tray_icon.show()

        self.addToolBar(Qt.RightToolBarArea, toolbar_top)
        self.setCentralWidget(self.text)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(100)

        self.buffer = [""]

    def menu_context_menu(self):
        # 主菜单
        menu = QMenu(self)
        menu.addAction(self.btn_show)
        menu.addSeparator()
        menu.addAction(self.btn_start)
        menu.addSeparator()
        menu.addAction(self.btn_top)
        menu.addSeparator()
        menu.addAction(self.btn_save)
        menu.addAction(self.btn_clear)
        menu.addSeparator()
        menu.addAction(self.btn_close)
        return menu

    def timer_event(self):
        clipboard = QGuiApplication.clipboard()
        content = clipboard.text()
        if content == self.buffer[-1]:
            return
        if not content:
            return
        self.text.append(content)
        self.buffer.append(content)

    def btn_start_click(self):
        if self.btn_start.isChecked():
            self.timer.start()
            self.btn_start.setText("运行中")
            self.tray_icon.setToolTip("ClipboardMe2: 运行中")
            self.btn_start.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogYesButton)))
            self.tray_icon.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogYesButton)))
        else:
            self.timer.stop()
            self.btn_start.setText("已停止")
            self.tray_icon.setToolTip("ClipboardMe2: 已停止")
            self.btn_start.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogNoButton)))
            self.tray_icon.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogNoButton)))

    def btn_top_click(self):
        if self.btn_top.isChecked():
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.move(self.desktop.width() - self.size().width(), self.pos().y())
        else:
            self.setWindowFlags(Qt.Widget)
        self.showNormal()

    def btn_save_click(self):
        now = datetime.datetime.now().strftime("%Y%m%dT%H%M")
        text = self.text.toPlainText()
        if text:
            file_path, file_type = QFileDialog.getSaveFileName(self, "另存为 ...",
                                                               f"clipboard-{now}.txt",
                                                               "Txt(*.txt);;Json(*.json)")
            if file_path:
                with open(file_path, "wb") as f:
                    f.write(text.encode())

    def btn_sort_click(self):
        text = self.text.toPlainText()
        if text:
            rows = text.splitlines()
            lines = {_.strip() for _ in rows if _.strip()}
            self.text.setText("\n".join(sorted(lines)))

    def btn_clear_click(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.clear()
        self.text.clear()
        self.buffer = [""]

    def tray_icon_click(self, reason):
        if reason == 2:
            self.showNormal()

    # def closeEvent(self, e) -> None:
    #     self.hide()
    #     e.ignore()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    frm = Clipboard2()
    frm.show()
    sys.exit(app.exec_())
