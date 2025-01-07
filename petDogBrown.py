from PyQt5 import QtWidgets
import os
from pet4gif import Pet  # 导入 Pet 类
import sys
from PyQt5.QtCore import QTimer  # 从 PyQt5 导入 QTimer
from PyQt5.QtGui import QMovie


class DogBrown(Pet):
    def __init__(self):
        super().__init__(
            "petDogBrown"
        )  # 继承自 Pet 类，初始化时指定宠物名称为 DogBrown

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
        # 动态添加“开始运动”和“停止运动”按钮
        if self.isWalking:  # 判断当前是否正在运动
            menu.addAction("停止运动", self.stopMotion)
        else:
            menu.addAction("开始运动", self.startMotion)

        menu.addAction("随机", self.randomAction)  # 散步选项

        menu.addAction("散步", self.startWalk)  # 散步选项
        menu.addAction("停止", self.startIdle)  # 停止选项啊？
        menu.addAction("聊天", self.AIchat)  # AI聊天选项
        # 添加新菜单项
        menu.addSeparator()  # 添加分隔线

        menu.addAction("交互", self.startCo)
        menu.addAction("吃饭", self.startEat)
        menu.addAction("高兴", self.startMeet)
        menu.addAction("跳舞", self.startDance)
        menu.addAction("生气", self.startMad)
        menu.addAction("睡觉", self.startSleep)
        menu.addAction("爱心", self.startLove)
        menu.addAction("冰淇淋", self.startIce)
        menu.addSeparator()  # 分隔线
        menu.addAction("退出", self.close)  # 退出选项
        menu.addAction("更换宠物", self.changePet)  # 更换宠物选项
        # 显示菜单
        menu.exec_(self.mapToGlobal(position))

    def startMotion(self):
        self.isWalking = True
        self.randomwalk()

    def stopMotion(self):
        self.isWalking = False
        self.stopRandomMotion()

    def AIchat(self):
        os.system(f"{sys.executable} ./AIchat.py")

    def startEat(self):
        self.gif_path = os.path.join(self.pet_name, "eat.gif")
        self.loadGif(self.gif_path)

    def randomAction(self):
        path = "./petDogBrown"

        # 定时器每30秒调用一次updateGif
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.updateGif(path))  # 使用 lambda 传递参数
        self.timer.start(5000)  # 每5秒触发

        # 初次调用立即加载一个GIF
        self.updateGif(path)

    def startMeet(self):
        self.gif_path = os.path.join(self.pet_name, "meet.gif")
        self.loadGif(self.gif_path)

    def startDance(self):
        self.gif_path = os.path.join(self.pet_name, "Music.gif")
        self.loadGif(self.gif_path)

    def startLove(self):
        self.gif_path = os.path.join(self.pet_name, "love.gif")
        self.loadGif(self.gif_path)

    def startMad(self):
        self.gif_path = os.path.join(self.pet_name, "mad.gif")
        self.loadGif(self.gif_path)

    def startSleep(self):
        self.gif_path = os.path.join(self.pet_name, "sleep.gif")
        self.loadGif(self.gif_path)

    def startIce(self):
        self.gif_path = os.path.join(self.pet_name, "ice.gif")
        self.loadGif(self.gif_path)

    def startCo(self):
        self.gif_path = os.path.join(self.pet_name, "co.gif")
        self.loadGif(self.gif_path)
