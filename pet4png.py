# pet4png.py
import os
import random
from PyQt5 import QtWidgets, QtGui, QtCore

# 定义宠物的父类
class Pet(QtWidgets.QLabel):
    def __init__(self, pet_name):
        super().__init__()
        self.initUI()  # 初始化界面
        self.pet_name = pet_name  # 保存宠物的名字
        self.isDragging = False  # 标记是否在拖动
        self.drag_position = QtCore.QPoint(0, 0)  # 存储拖动位置
        self.prevAction = None  # 用于保存之前的动作
        self.currentAction = self.startIdle  # 当前动作是待机
        self.timer = QtCore.QTimer(self)  # 创建一个定时器，用来刷新动画
        self.timer.timeout.connect(self.updateAnimation)  # 定时器超时时更新动画
        self.changeDirectionTimer = QtCore.QTimer(self)  # 方向变化的定时器
        self.changeDirectionTimer.timeout.connect(self.changeDirection)  # 定时器超时时改变方向
        self.startIdle()  # 初始化时设置为待机状态
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 自定义右键菜单
        self.customContextMenuRequested.connect(self.showMenu)  # 连接右键菜单的信号
        self.setMouseTracking(True)  # 启用鼠标追踪
        self.dragging = False  # 拖动标志初始化为 False

    # 初始化UI，设置窗口相关的属性
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # 无边框并且置顶
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明
        self.setGeometry(500, 500, 130, 130)  # 默认宠物窗口位置
        self.setFixedSize(130, 130)  # 设置宠物窗口固定大小

    # 加载指定路径下的所有 PNG 图片
    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    # 待机状态方法
    def startIdle(self):
        self.images = self.loadImages(f"{self.pet_name}/idle")  # 根据宠物名字加载待机图片
        self.currentImage = 0  # 当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画
        self.moveSpeed = 0  # 待机时没有移动
        self.movingDirection = 0  # 待机时没有方向
        self.changeDirectionTimer.stop()  # 停止方向改变的定时器

    # 散步状态方法
    def startWalk(self):
        self.images = self.loadImages(f"{self.pet_name}/sanbu/you")  # 加载散步的图片
        self.currentImage = 0  # 当前图片索引
        self.movingDirection = 1  # 设置初始移动方向为右
        self.moveSpeed = 10  # 设置移动速度
        self.timer.start(100)  # 每 100ms 更新一次动画
        self.changeDirectionTimer.start(3000)  # 每 3000ms 改变一次方向

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
                    self.images = self.loadImages(f"{self.pet_name}/sanbu/zuo")
                else:  # 向右移动
                    self.images = self.loadImages(f"{self.pet_name}/sanbu/you")

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
                    self.images = self.loadImages(f"{self.pet_name}/sanbu/zuo")
                else:  # 向右移动
                    self.images = self.loadImages(f"{self.pet_name}/sanbu/you")

                self.currentImage = 0
                self.timer.start(100)
        self.deskpet_rect = self.geometry()
        self.move(new_x, self.y())

    # 根据宠物当前的方向来移动宠物
    def movePet(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()  # 获取屏幕的几何信息
        new_x = self.x() + self.movingDirection * self.moveSpeed  # 根据方向和速度计算新的 X 坐标

        # 如果到达屏幕的左边界，则改变方向
        if new_x < 10:
            new_x = 10
            self.movingDirection *= -1  # 方向反转
            self.updateDirectionImages()  # 更新方向对应的图片

        # 如果到达屏幕的右边界，则改变方向
        elif new_x > screen.width() - self.width() - 10:
            new_x = screen.width() - self.width() - 10
            self.movingDirection *= -1  # 方向反转
            self.updateDirectionImages()  # 更新方向对应的图片

        # 移动宠物
        self.move(new_x, self.y())

    # 更新方向时调用的函数，更新移动方向对应的图片
    def updateDirectionImages(self):
        if self.movingDirection == 1:  # 如果方向是右
            self.images = self.loadImages(f"{self.pet_name}/sanbu/you")  # 加载向右的图片
        else:  # 如果方向是左
            self.images = self.loadImages(f"{self.pet_name}/sanbu/zuo")  # 加载向左的图片
        self.currentImage = 0  # 重置当前图片索引
        self.timer.start(100)  # 每 100ms 更新一次动画

    # 每个定时器触发时调用的函数，更新宠物的动画
    def updateAnimation(self):
        self.setPixmap(self.images[self.currentImage])  # 设置当前的图片
        self.currentImage = (self.currentImage + 1) % len(self.images)  # 更新图片索引
        self.movePet()  # 移动宠物

    # 处理方向变化的函数
    def changeDirection(self):
        if random.random() < 0.5:  # 随机决定是否改变方向
            self.movingDirection *= -1  # 改变方向
            self.updateDirectionImages()  # 更新方向对应的图片

    # 显示右键菜单
    def showMenu(self, position):
        menu = QtWidgets.QMenu()
        menu.addAction("散步", self.startWalk)  # 散步选项
        menu.addAction("停止", self.startIdle)  # 停止选项
        menu.addSeparator()  # 分隔线
        menu.addAction("退出", self.close)  # 退出选项
        menu.addAction("更换宠物", self.changePet)  # 处理更换宠物的函数
        menu.exec_(self.mapToGlobal(position))  # 显示菜单

    def changePet(self):
        from ui import PetSelector  # 延迟导入 PetSelector
        self.close()  # 关闭当前宠物窗口
        self.selector = PetSelector()  # 创建宠物选择器界面
        self.selector.show()  # 显示宠物选择界面

    # 左键按下时触发的事件，开始拖动宠物
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True  # 标记正在拖动
            self.drag_position = event.globalPos() - self.pos()  # 记录拖动的初始位置
            self.prevAction = self.currentAction  # 记录当前的动作
            event.accept()

    # 鼠标移动时触发的事件，拖动宠物
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)  # 更新宠物的位置
            event.accept()

    # 左键释放时触发的事件，停止拖动
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False  # 停止拖动
            self.prevAction()  # 恢复之前的动作
            event.accept()
