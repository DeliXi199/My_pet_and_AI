# petXiaoxin.py\
from PyQt5 import QtWidgets, QtCore
import os
from pet4png import Pet  # 导入父类 Pet
import sys


class Xiaoxin(Pet):
    def __init__(self):
        super().__init__("petXiaoxin")  # 传入宠物的名字，父类根据名字加载图片

    def showMenu(self, position):
        """扩展父类的右键菜单"""
        menu = QtWidgets.QMenu()

        # 设置菜单样式
        menu.setStyleSheet(
            """
            QMenu {
                background-color: #f4f4f4;  /* 菜单背景颜色 */
                border: 1px solid #8b4513; /* 边框颜色 */
                padding: 5px;  /* 内边距 */
                font-size: 30px;  /* 字体大小 */
                font-family: FangSong;  /* 字体样式 */
            }
            QMenu::item {
                padding: 8px 20px;  /* 菜单项的内边距 */
                background-color: transparent;  /* 默认背景透明 */
                color: #8b4513;  /* 菜单项文字颜色 */
            }
            QMenu::item:selected {
                background-color: #8b4513;  /* 鼠标悬停时的背景颜色 */
                color: #ffffff;  /* 鼠标悬停时的文字颜色 */
            }
            QMenu::separator {
                height: 1px;  /* 分隔线高度 */
                background-color: #8b4513;  /* 分隔线颜色 */
                margin: 4px 0;  /* 分隔线上下间距 */
            }
        """
        )

        # 调用父类的方法来添加默认的菜单项
        # 添加父类的菜单项
        menu.addAction("散步", self.startWalk)  # 散步选项
        menu.addAction("停止", self.startIdle)  # 停止选项
        menu.addAction("聊天", self.AIchat)  # AI聊天选项
        # 添加新菜单项
        menu.addSeparator()  # 添加分隔线
        menu.addAction("吃饭", self.startEat)
        menu.addAction("休息", self.startRest)
        menu.addAction("下落", self.startFall)
        menu.addAction("运动", self.startEx)
        menu.addAction("小白", self.startBai)
        menu.addSeparator()  # 分隔线
        menu.addAction("退出", self.close)  # 退出选项
        menu.addAction("更换宠物", self.changePet)  # 更换宠物选项
        # 显示菜单
        menu.exec_(self.mapToGlobal(position))

    def startEat(self):
        eating_path = os.path.join("petXiaoxin", "eat")
        self.images = self.loadImages(eating_path)
        self.currentImage = 0  # 当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画

    def startRest(self):
        eating_path = os.path.join("petXiaoxin", "waken")
        self.images = self.loadImages(eating_path)
        self.currentImage = 0  # 当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画

    def AIchat(self):
        os.system(f"{sys.executable} ./AIchat.py")

    def startFall(self):
        eating_path = os.path.join("petXiaoxin", "xialuo")
        self.images = self.loadImages(eating_path)
        self.currentImage = 0  # 当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画

    def startEx(self):
        eating_path = os.path.join("petXiaoxin", "yundong")
        self.images = self.loadImages(eating_path)
        self.currentImage = 0  # 当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画

    def startBai(self):
        eating_path = os.path.join("petXiaoxin", "xiaobai")
        self.images = self.loadImages(eating_path)
        self.currentImage = 0  # 当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画
