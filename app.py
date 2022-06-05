from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.pyqtwindow import Ui_MainWindow
import sys, os
import time
import AppKit
import pyautogui
from PIL import Image, ImageDraw 


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.initUI()
        

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.GetPixelColorButton.clicked.connect(self.StartGetMonitorPixelColor)

    def StartGetMonitorPixelColor(self):
        self.work = GetMonitorPixelColor()
        self.work.qthread_signal_screenshotpath.connect(self.ShowImage)
        self.work.qthread_signal_colorvalue1.connect(self.ChangeColorTexT)
        self.work.qthread_signal_colorvalue1.connect(self.ChangeColorBlock)
        self.work.qthread_signal_mouseposition.connect(self.ChangeMousePositionTexT)
        self.work.start()

    # 顯示圖
    def ShowImage(self, path):
        im = QPixmap(path)
        self.Image.setPixmap(im)

    def ChangeColorTexT(self, color):
        self.ColorValue.setText("RGBA   : {}".format(color))

    def ChangeMousePositionTexT(self, position):
        self.MousePosition.setText("Position : {}".format(position))

    def ChangeColorBlock(self, color):
        self.ShowColor.setStyleSheet("background-color: rgba{}".format(color))


class GetMonitorPixelColor(QThread):
    qthread_signal_screenshotpath = pyqtSignal(str)
    qthread_signal_colorvalue1 = pyqtSignal(str)
    qthread_signal_mouseposition = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ScreenShotPath = './screenshot/my_screenshot.png'
        self.SmallScreenShotPath = './screenshot/my_smallscreenshot.png'

    def run(self):
        while True:
            x, y = pyautogui.position()
            screenWidth, screenHeight = pyautogui.size()
            im = pyautogui.screenshot(self.ScreenShotPath)
            im = im.resize([screenWidth, screenHeight])
            new_im = im.crop((x - 200, y - 200, x + 200, y + 200))
            new_im.save("./screenshot/my_smallscreenshot.png")
            # new_im.show()
            self.Color = new_im.getpixel((200, 200))
            print("Resolution: {} \nImage Size: {} \nPosition: {} \nColor: {} \n".format([screenWidth, screenHeight], im.size, [x, y], self.Color))
            self.qthread_signal_screenshotpath.emit(str(self.SmallScreenShotPath))
            self.qthread_signal_colorvalue1.emit(str(self.Color))
            self.qthread_signal_mouseposition.emit(str((x , y)))



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        destory()
