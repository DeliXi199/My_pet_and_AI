import os
from PyQt5 import QtWidgets, QtGui, QtCore
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtCore import QPoint, QTimer, QRect


class Pet(QtWidgets.QLabel):
    def __init__(self, pet_name):
        super().__init__()
        self.initUI()
        self.pet_name = pet_name
        self.dragging = False  # 用于标识是否正在拖动
        self.prevAction = None  # 用于保存之前的动作
        self.currentAction = self.startIdle  # 当前动作是待机
        self.startIdle()  # 初始化时设置为待机状态
        self.isWalking = False  # 是否正在运动
        self.isWalked = False  # 是否已经运动过

    def initUI(self):
        """初始化宠物界面"""
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)  # 启用鼠标跟踪

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)

        # 右键菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)  # 连接右键菜单

        self.movie = None  # 用来存储当前的QMovie对象
        self.default_gif = None  # 默认GIF动画（比如静止或走路）

    def loadGif(self, path, size=(150, 150)):
        """加载GIF动画，并将其缩放到固定的大小"""
        self.movie = QtGui.QMovie(path)

        # 确保GIF动画正确显示
        self.setMovie(self.movie)  # 设置当前 QLabel 显示的 GIF

        # 设置GIF的缩放大小（保持宽高比）
        self.movie.setScaledSize(QtCore.QSize(size[0], size[1]))

        # 启动GIF动画
        self.movie.start()

        # 设置标签的固定大小以匹配GIF大小
        self.setFixedSize(size[0], size[1])

    def startIdle(self):
        """设置宠物为静止状态"""
        self.gif_path = os.path.join(
            self.pet_name, "idle.gif"
        )  # 假设路径是 "petName/idle.gif"
        self.default_gif = self.gif_path  # 记录默认的GIF路径
        self.loadGif(self.gif_path)  # 加载并播放静止状态的 GIF

    def startWalk(self):
        """设置宠物为走路状态"""
        self.gif_path = os.path.join(
            self.pet_name, "walk.gif"
        )  # 假设路径为 "petName/walk.gif"
        self.default_gif = self.gif_path  # 记录默认的GIF路径
        self.loadGif(self.gif_path)  # 加载并播放走路状态的 GIF

    def startDragging(self):
        """设置宠物为拖动状态"""
        self.gif_path = os.path.join(
            self.pet_name, "walk.gif"
        )  # 假设路径为 "petName/walk.gif"
        self.loadGif(self.gif_path)  # 加载并播放拖动状态的 GIF

    def updateAnimation(self):
        """更新动画"""
        pass  # 这个方法可以用来做额外的动画更新逻辑，比如根据帧数来做其他事情

    def closeEvent(self, event):
        """关闭宠物窗口"""
        if self.movie:
            self.movie.stop()  # 停止 GIF 播放
        super().closeEvent(event)

    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if self.isWalking:
            self.stopRandomMotion()  # 停止随机运动
            self.isWalking = False  # 停止散步
            self.isWalked = True  # 标记已经散步过
        else:
            self.isWalked = False  # 重置散步标记

        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True  # 标记为正在拖动
            self.drag_position = event.globalPos() - self.pos()  # 记录鼠标点击时的偏移
            self.prevAction = self.currentAction  # 记录当前的动作
            self.startDragging()  # 在开始拖动时播放拖动GIF
            event.accept()  # 接受事件，表示事件被处理

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件，进行拖动"""
        if QtCore.Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)  # 更新窗口位置
            event.accept()  # 接受事件，表示事件被处理

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件，停止拖动"""
        if self.isWalked:
            self.randomwalk()  # 开始随机运动
            self.isWalking = True  # 标记为正在散步
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False  # 标记为不再拖动
            self.prevAction()  # 恢复之前的动作
            event.accept()  # 接受事件，表示事件被处理

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

    def randomwalk(self):
        """加载 GIF 并开始随机运动"""

        # 检查并加载 GIF 文件
        if not os.path.exists(self.gif_path):
            print(f"Error: GIF file not found at {self.gif_path}")
            return

        self.loadGif(self.gif_path)

        gif_size = self.movie.scaledSize()
        self.resize(gif_size.width(), gif_size.height())
        self.movie.frameChanged.connect(self.update)  # 在每帧刷新
        self.movie.start()

        self.show()
        self.startRandomMotion()

    def startRandomMotion(self):
        """让窗口在整个屏幕上随机运动"""

        current_pos = self.pos()

        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 确定目标位置
        target_x = random.randint(0, screen_width - self.width())
        target_y = random.randint(0, screen_height - self.height())

        # 使用 QTimer 模拟动画
        self.start_x = current_pos.x()
        self.start_y = current_pos.y()
        self.target_x = target_x
        self.target_y = target_y

        self.step_count = 300  # 增加步数，减小每步距离
        self.current_step = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animateStep)
        self.timer.start(30)  # 每帧持续 40 毫秒，减缓帧率

    def stopRandomMotion(self):
        """停止随机运动但保留 GIF 动画播放"""
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()  # 停止定时器，结束运动

    def animateStep(self):
        """每一帧的动画更新"""
        if self.current_step >= self.step_count:
            self.timer.stop()
            self.startRandomMotion()  # 动画结束后继续随机移动
            return

        # 线性插值计算新位置
        t = self.current_step / self.step_count
        new_x = self.start_x + (self.target_x - self.start_x) * t
        new_y = self.start_y + (self.target_y - self.start_y) * t
        self.move(int(new_x), int(new_y))
        self.current_step += 1

    def paintEvent(self, event):
        """在窗口上绘制 GIF 的当前帧"""
        if self.movie is not None:
            painter = QPainter(self)
            rect = QRect(0, 0, self.width(), self.height())
            current_frame = self.movie.currentPixmap()
            painter.drawPixmap(rect, current_frame)

    def updateGif(self, folder_path):
        # 获取文件夹中的所有GIF文件
        gif_files = [f for f in os.listdir(folder_path) if f.endswith(".gif")]
        if not gif_files:
            print("No GIF files found in the folder.")
            return

        # 随机选择一个GIF文件
        gif_path = os.path.join(folder_path, random.choice(gif_files))
        self.loadGif(gif_path)
