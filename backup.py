import sys
import os
import random
from PyQt5 import QtWidgets, QtGui, QtCore

class Xiaoxin(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.childPets = []
        self.isDragging = False
        self.isMoving = False
        self.change = False

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(500, 500, 130, 130)
        self.currentAction = self.startIdle
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.changeDirectionTimer = QtCore.QTimer(self)  # 添加定时器
        self.changeDirectionTimer.timeout.connect(self.changeDirection)  # 定时器触发时调用changeDirection方法
        self.startIdle()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)
        self.setMouseTracking(True)
        self.dragging = False

    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    def startIdle(self):
        self.setFixedSize(130, 130)
        self.currentAction = self.startIdle
        self.images = self.loadImages("Xiaoxin/xianzhi")
        self.currentImage = 0
        self.timer.start(100)
        self.moveSpeed = 0
        self.movingDirection = 0
        if self.changeDirectionTimer.isActive():
            self.changeDirectionTimer.stop()  # 停止方向改变的定时器

    def startWalk(self):
        self.setFixedSize(130, 130)
        if not self.isDragging:
            self.currentAction = self.startWalk
            direction = random.choice(["zuo", "you"])
            self.images = self.loadImages(f"Xiaoxin/sanbu/{direction}")
            self.currentImage = 0
            self.movingDirection = -1 if direction == "zuo" else 1
            self.moveSpeed = 10
            self.timer.start(100)
            self.changeDirectionTimer.start(3000)  # 启动定时器

    def movePet(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        new_x = self.x() + self.movingDirection * self.moveSpeed
        if new_x < 10:
            new_x = 10
            if self.currentAction == self.startWalk:
                self.movingDirection *= -1
                # 停止加载原先的图片
                self.timer.stop()
                self.images = []  # 清空当前图片列表
                if self.movingDirection == -1:  # 向左移动
                    self.images = self.loadImages("Xiaoxin/sanbu/zuo")
                else:  # 向右移动
                    self.images = self.loadImages("Xiaoxin/sanbu/you")

                self.currentImage = 0
                self.timer.start(100)
        elif new_x > screen.width() - self.width() - 10:
            new_x = screen.width() - self.width() - 10
            if self.currentAction == self.startWalk:
                self.movingDirection *= -1
                # 停止加载原先的图片
                self.timer.stop()
                self.images = []  # 清空当前图片列表
                # 根据移动方向加载对应的图片
                if self.movingDirection == -1:  # 向左移动
                    self.images = self.loadImages("Xiaoxin/sanbu/zuo")
                else:  # 向右移动
                    self.images = self.loadImages("Xiaoxin/sanbu/you")

                self.currentImage = 0
                self.timer.start(100)
        self.deskpet_rect = self.geometry()
        self.move(new_x, self.y())

    def startMeet(self):
        self.setFixedSize(150, 150)
        self.currentAction = self.startMeet
        self.images = self.loadImages("petXiaoxin/meet")
        self.currentImage = 0
        self.moveSpeed = 0
        self.movingDirection = 0
        self.timer.start(30)

    def startLift(self):
        self.setFixedSize(160, 160)
        self.currentAction = self.startLift
        self.images = self.loadImages("petXiaoxin/linqi")
        self.currentImage = 0
        self.moveSpeed = 0
        self.movingDirection = 0
        self.timer.start(100)

    def startFall(self):
        self.setFixedSize(150, 150)
        self.currentAction = self.startFall
        self.images = self.loadImages("Xiaoxin/xialuo")
        self.currentImage = 0
        self.movingDirection = 0
        self.moveSpeed = 5
        self.stopOtherActions()
        self.timer.start(30)

    def stopOtherActions(self):
        self.timer.stop()
        if self.currentAction == self.startWalk:
            self.changeDirectionTimer.stop()  # 停止方向判定定时器
            self.startIdle()
        elif self.currentAction == self.startLift:
            self.startIdle()
        elif self.currentAction == self.startFall:
            pass
        else:
            self.startIdle()

    def updateAnimation(self):
        self.setPixmap(self.images[self.currentImage])
        self.currentImage = (self.currentImage + 1) % len(self.images)
        if hasattr(self, 'movingDirection'):
            if self.currentAction == self.startFall:
                self.fallPet()
            else:
                self.movePet()

    def fallPet(self):
        self.setFixedSize(130, 130)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        new_y = self.y() + self.moveSpeed
        if new_y > screen.height() - self.height() - 10:
            new_y = screen.height() - self.height() - 10
            self.timer.stop()
            self.startIdle()
        self.move(self.x(), new_y)

    def showMenu(self, position):
        menu = QtWidgets.QMenu()
        if self.currentAction == self.sleep:
            menu.addAction("唤醒", self.WakeUp)
            menu.addSeparator()
            menu.addAction("隐藏", self.minimizeWindow)
            menu.addAction("退出", self.close)
        else:
            menu.addAction("散步", self.startWalk)
            menu.addAction("下落", self.startFall)
            menu.addAction("运动", self.exercise)
            menu.addAction("吃饭", self.eating)
            menu.addAction("睡觉", self.sleep)
            menu.addAction("测试", self.startMeet)
            menu.addSeparator()
            menu.addAction("停止", self.startIdle)
            menu.addAction("隐藏", self.minimizeWindow)
            menu.addAction("退出", self.close)
        menu.exec_(self.mapToGlobal(position))

    def exercise(self):
        self.setFixedSize(150,180 )
        self.currentAction = self.exercise
        self.images = self.loadImages("Xiaoxin/yundong")
        self.currentImage = 0
        self.timer.start(125)
        self.moveSpeed = 0
        self.movingDirection = 0

    def eating(self):
        self.setFixedSize(160, 90)
        self.currentAction = self.eating
        self.images = self.loadImages("Xiaoxin/eat")
        self.currentImage = 0
        self.timer.start(25)
        self.moveSpeed = 0
        self.movingDirection = 0
        QtCore.QTimer.singleShot(len(self.images) * 30, self.startIdle)

    def sleep(self):
        self.setFixedSize(315, 500)
        self.currentAction = self.sleep
        self.images = self.loadImages("Xiaoxin/sleep")
        self.currentImage = 0
        self.timer.start(155)
        self.moveSpeed = 0
        self.movingDirection = 0

    def showWakeUpMenu(self):
        self.setFixedSize(130, 130)
        self.sleeping = True
        menu = QtWidgets.QMenu()
        menu.addAction("唤醒", self.wakeUp)
        menu.exec_(self.mapToGlobal(self.pos()))

    def WakeUp(self):
        self.setFixedSize(180, 180)
        self.sleeping = False
        self.currentAction = self.WakeUp
        self.images = self.loadImages("Xiaoxin/waken")
        self.currentImage = 0
        self.timer.start(30)
        # 延时，等待所有图片加载完成
        QtCore.QTimer.singleShot(len(self.images) * 30, self.finishWakeUp)

    def finishWakeUp(self):
        self.movingDirection = 0
        self.wakeUpImagesLoaded = True
        self.setFixedSize(180, 180)
        self.timer.stop()
        self.currentAction = self.startIdle
        self.images = self.loadImages("Xiaoxin/xianzhi")
        self.currentImage = 0
        self.timer.start(100)

    def closeEvent(self, event):
        for child in self.childPets:
            child.close()  # 关闭所有子窗口
        super().closeEvent(event)

    def minimizeWindow(self):
        self.showMinimized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.isDragging = True
            self.drag_position = event.globalPos() - self.pos()
            self.prevAction = self.currentAction
            self.startLift()
            event.accept()

    def mouseMoveEvent(self, event):
        if QtCore.Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            self.isDragging = False

            # 根据需要重新启动changeDirectionTimer
            if self.currentAction == self.startWalk:
                self.changeDirectionTimer.start()

            self.prevAction()  # 或者 self.startIdle(), 根据之前的动作恢复状态
            event.accept()

    def changeDirection(self):
        if self.currentAction == self.startFall or self.currentAction == self.eating or self.currentAction == self.sleep or self.currentAction == self.exercise or self.currentAction == self.WakeUp or self.currentAction == self.startIdle or self.startMeet:
            return  # 如果正在执行下落动作，不改变方向

        if random.random() < 0.5:  # 随机选择是否改变方向
            self.movingDirection *= -1
            self.change = True
            if self.change == True:
                # 停止加载原先的图片
                self.timer.stop()
                self.images = []  # 清空当前图片列表
                self.startWalk()
                self.change = False

app = QtWidgets.QApplication(sys.argv)
pet = Xiaoxin()
pet.show()
sys.exit(app.exec_())