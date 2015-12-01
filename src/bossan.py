#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from PySide import QtGui, QtCore
from image_edit import ImageFactory

class DropArea(QtGui.QFrame):
    ''' ('v') drag and drop area '''
    def __init__(self):
        super().__init__()
        # ('-') essentials
        self.setObjectName("DropArea")
        self.setAcceptDrops(True)
        self.setFixedSize(200, 280)
        # ('-') top section
        self.vb_top = QtGui.QVBoxLayout()
        self.vb_top.setAlignment(QtCore.Qt.AlignTop)
        # ('-') middle section
        self.vb_mid = QtGui.QVBoxLayout()
        self.vb_mid.setAlignment(QtCore.Qt.AlignTop)
        # ('-') bottom section
        self.vb_btm = QtGui.QVBoxLayout()
        self.vb_btm.setAlignment(QtCore.Qt.AlignBottom)
        # ('-') setup all sections
        self.vb_area = QtGui.QVBoxLayout()
        self.vb_area.addLayout(self.vb_top)
        self.vb_area.addLayout(self.vb_mid)
        self.vb_area.addLayout(self.vb_btm)
        self.setLayout(self.vb_area)

    def fileGate(self, event):
        # ('o') detects dragged-in files
        if event.mimeData().hasUrls() \
        and not os.path.isdir([url.toLocalFile() for url in event.mimeData().urls()][0]):
            event.accept()
            return True
        else:
            event.ignore()
            return False


class AreaResize(DropArea):
    ''' ('v') resize area, the special section is the bottom '''
    def __init__(self):
        super().__init__()
        self.setObjectName("AreaResize")
        # ('-') top section
        self.lbl_top = QtGui.QLabel()
        self.lbl_top.setPixmap(QtGui.QPixmap("resources/img/label_resize.png"))
        self.lbl_top.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_top.addWidget(self.lbl_top)
        # ('-') middle section
        self.lbl_mid = QtGui.QLabel()
        self.lbl_mid.setPixmap(QtGui.QPixmap("resources/img/img_resize.png"))
        self.lbl_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_mid.addWidget(self.lbl_mid)
        # ('-') bottom section
        self.cb_half = QtGui.QCheckBox()
        self.cb_half.setObjectName("cb_half")
        self.cb_half.setChecked(True)

        self.lbl_width = QtGui.QLabel()
        self.lbl_width.setPixmap(QtGui.QPixmap("resources/img/label_width.png"))
        self.sb_width = QtGui.QSpinBox()
        self.sb_width.setObjectName("sb_width")
        self.sb_width.setMaximum(2000)
        self.sb_width.setSingleStep(10)
        self.sb_width.setValue(500)
        self.sb_width.setFixedSize(85, 30)
        self.sb_width.setAlignment(QtCore.Qt.AlignRight)
        self.sb_width.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.hb_w = QtGui.QHBoxLayout()
        self.hb_w.addWidget(self.lbl_width)
        self.hb_w.addWidget(self.sb_width)
        self.hb_w.setAlignment(QtCore.Qt.AlignCenter)
        self.hb_w.setContentsMargins(-10, -10, -10, -10)

        self.lbl_height = QtGui.QLabel()
        self.lbl_height.setPixmap(QtGui.QPixmap("resources/img/label_height.png"))
        self.sb_height = QtGui.QSpinBox()
        self.sb_height.setObjectName("sb_height")
        self.sb_height.setMaximum(2000)
        self.sb_height.setSingleStep(10)
        self.sb_height.setValue(500)
        self.sb_height.setFixedSize(85, 30)
        self.sb_height.setAlignment(QtCore.Qt.AlignRight)
        self.sb_height.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.hb_h = QtGui.QHBoxLayout()
        self.hb_h.addWidget(self.lbl_height)
        self.hb_h.addWidget(self.sb_height)
        self.hb_h.setAlignment(QtCore.Qt.AlignCenter)

        self.vb_wgt = QtGui.QVBoxLayout()
        self.vb_wgt.addWidget(self.cb_half)
        self.vb_wgt.addLayout(self.hb_w)
        self.vb_wgt.addLayout(self.hb_h)
        self.vb_wgt.setAlignment(QtCore.Qt.AlignCenter)
        # ('-') setup all sections
        self.vb_btm.addLayout(self.vb_wgt)
        self.vb_btm.setAlignment(QtCore.Qt.AlignCenter)

    def dragEnterEvent(self, event):
        # ('o') called when files are dragged-in the area
        if self.fileGate(event):
            print("enter")
            self.setStyleSheet("#AreaResize{background-color: #FAFAFA;}")

    def dragLeaveEvent(self, event):
        # ('o') called when files leave from the area
        print("leave")
        self.setStyleSheet("#AreaResize{background-color: #F2F2F2;}")

    def dropEvent(self, event):
        # ('o') called when files are dropped-into the area
        print("drop")
        width = self.sb_width.value()
        height = self.sb_height.value()
        if self.cb_half.checkState() == 2:
            half = True
        else:
            half = False
        print(width)
        file = [url.toLocalFile() for url in event.mimeData().urls()]
        print(file)
        ImageFactory(file).resize(half, width, height)
        self.setStyleSheet("#AreaResize{background-color: #F2F2F2;}")


class AreaRotate(DropArea):
    ''' ('v') rotate area, has 2 radio buttons '''
    def __init__(self):
        super().__init__()
        self.setObjectName("AreaRotate")
        # ('-') top section
        self.lbl_top = QtGui.QLabel()
        self.lbl_top.setPixmap(QtGui.QPixmap("resources/img/label_rotate.png"))
        self.lbl_top.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_top.addWidget(self.lbl_top)
        # ('-') middle section
        self.lbl_mid = QtGui.QLabel()
        self.lbl_mid.setPixmap(QtGui.QPixmap("resources/img/img_rotate.png"))
        self.lbl_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_mid.addWidget(self.lbl_mid)
        # ('-') bottom section
        self.rb_right = QtGui.QRadioButton()
        self.rb_right.setObjectName("rb_right")
        self.rb_right.setChecked(True)

        self.rb_left = QtGui.QRadioButton()
        self.rb_left.setObjectName("rb_left")
        self.rb_left.setChecked(False)

        self.vb_wgt = QtGui.QVBoxLayout()
        self.vb_wgt.addWidget(self.rb_right)
        self.vb_wgt.addWidget(self.rb_left)
        self.vb_wgt.setAlignment(QtCore.Qt.AlignCenter)
        # ('-') setup all sections
        self.vb_btm.addLayout(self.vb_wgt)
        self.vb_btm.setAlignment(QtCore.Qt.AlignCenter)

    def dragEnterEvent(self, event):
    # ('o') called when files are dragged-in the area
        if self.fileGate(event):
            print("enter")
            self.setStyleSheet("#AreaRotate{background-color: #FAFAFA;}")

    def dragLeaveEvent(self, event):
        # ('o') called when files leave from the area
        print("leave")
        self.setStyleSheet("#AreaRotate{background-color: #F2F2F2;}")

    def dropEvent(self, event):
        # ('o') called when files are dropped-into the area
        print("drop")
        if self.rb_right.isChecked():
            direction = "right"
        elif self.rb_left.isChecked():
            direction = "left"
        else:
            direction = "right"
        file = [url.toLocalFile() for url in event.mimeData().urls()]
        print(file)
        ImageFactory(file).rotate(direction)
        self.setStyleSheet("#AreaRotate{background-color: #F2F2F2;}")


class AreaConcatenate(DropArea):
    ''' ('v') concatenate area, has 2 radio buttons '''
    def __init__(self):
        super().__init__()
        self.setObjectName("AreaConcatenate")
        # ('-') top section
        self.lbl_top = QtGui.QLabel()
        self.lbl_top.setPixmap(QtGui.QPixmap("resources/img/label_concatenate.png"))
        self.lbl_top.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_top.addWidget(self.lbl_top)
        # ('-') middle section
        self.lbl_mid = QtGui.QLabel()
        self.lbl_mid.setPixmap(QtGui.QPixmap("resources/img/img_concatenate.png"))
        self.lbl_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_mid.addWidget(self.lbl_mid)
        # ('-') bottom section
        self.rb_horizontal = QtGui.QRadioButton()
        self.rb_horizontal.setObjectName("rb_horizontal")
        self.rb_horizontal.setChecked(True)

        self.rb_vertical = QtGui.QRadioButton()
        self.rb_vertical.setObjectName("rb_vertical")
        self.rb_vertical.setChecked(False)

        self.vb_wgt = QtGui.QVBoxLayout()
        self.vb_wgt.addWidget(self.rb_horizontal)
        self.vb_wgt.addWidget(self.rb_vertical)
        self.vb_wgt.setAlignment(QtCore.Qt.AlignCenter)
        # ('-') setup all sections
        self.vb_btm.addLayout(self.vb_wgt)
        self.vb_btm.setAlignment(QtCore.Qt.AlignCenter)

    def dragEnterEvent(self, event):
    # ('o') called when files are dragged-in the area
        if len([url for url in event.mimeData().urls()]) < 2:
            print("'concatenate' requires more than 2 images.")
            event.ignore()
        elif self.fileGate(event):
            print("enter")
            self.setStyleSheet("#AreaConcatenate{background-color: #FAFAFA;}")

    def dragLeaveEvent(self, event):
        # ('o') called when files leave from the area
        print("leave")
        self.setStyleSheet("#AreaConcatenate{background-color: #F2F2F2;}")

    def dropEvent(self, event):
        # ('o') called when files are dropped-into the area
        print("drop")
        if self.rb_horizontal.isChecked():
            direction = "horizontal"
        elif self.rb_vertical.isChecked():
            direction = "vertical"
        else:
            direction = "horizontal"
        file = [url.toLocalFile() for url in event.mimeData().urls()]
        print(file)
        ImageFactory(file).concatenate(direction)
        self.setStyleSheet("#AreaConcatenate{background-color: #F2F2F2;}")


class AreaPngquant(DropArea):
    ''' ('v') Pngquant area, nothing special '''
    def __init__(self):
        super().__init__()
        self.setObjectName("AreaPngquant")
        # ('-') top section
        self.lbl_top = QtGui.QLabel()
        self.lbl_top.setPixmap(QtGui.QPixmap("resources/img/label_pngquant.png"))
        self.lbl_top.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_top.addWidget(self.lbl_top)
        # ('-') middle section
        self.lbl_mid = QtGui.QLabel()
        self.lbl_mid.setPixmap(QtGui.QPixmap("resources/img/img_pngquant.png"))
        self.lbl_mid.setAlignment(QtCore.Qt.AlignCenter)
        self.vb_mid.addWidget(self.lbl_mid)
        # ('-') bottom section
        # ('-') setup all sections

    def dragEnterEvent(self, event):
    # ('o') called when files are dragged-in the area
        if self.fileGate(event):
            print("enter")
            self.setStyleSheet("#AreaPngquant{background-color: #FAFAFA;}")

    def dragLeaveEvent(self, event):
        # ('o') called when files leave from the area
        print("leave")
        self.setStyleSheet("#AreaPngquant{background-color: #F2F2F2;}")

    def dropEvent(self, event):
        # ('o') called when files are dropped-into the area
        print("drop")
        file = [url.toLocalFile() for url in event.mimeData().urls()]
        ImageFactory(file).pngquant()
        self.setStyleSheet("#AreaPngquant{background-color: #F2F2F2;}")


class MainWidget(QtGui.QWidget):
    ''' ('v') main window class, contains all of the widgets '''
    def __init__(self):
        super().__init__()
        # ('-') essentials
        self.setObjectName("MainWidget")
        self.setWindowTitle("Bossan")
        self.setFixedSize(850, 300)
        self.setCSS()
        # ('-') yum yum
        self.main_hb = QtGui.QHBoxLayout()
        self.main_hb.addWidget(AreaResize())
        self.main_hb.addWidget(AreaRotate())
        self.main_hb.addWidget(AreaConcatenate())
        self.main_hb.addWidget(AreaPngquant())
        self.setLayout(self.main_hb)
        self.setContentsMargins(-5, -11, -5, -11)

    def setCSS(self):
        # ('o') set stylesheet from an external file
        with open("stylesheet.css","r") as style:
            self.setStyleSheet("".join(style.readlines()))


def main():
    ''' ('v') main class, run the program '''
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForLocale())
    # ('-') set icon
    app = QtGui.QApplication(sys.argv)
    app_icon = QtGui.QIcon(QtGui.QPixmap("resources/img/icon.png"))
    app.setWindowIcon(app_icon)
    # ('-') show
    win = MainWidget()
    win.show()
    # ('-') execute
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
