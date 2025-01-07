from PyQt5 import QtWidgets, QtGui, QtCore
from petCat import Cat
from petDogBrown import DogBrown
from petDogWhite import DogWhite
from petRabbit import Rabbit
from petXiaoxin import Xiaoxin


class PetSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 去掉默认的标题栏
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.resize(1200, 800)

        # # 设置窗口标题和尺寸
        # self.setWindowTitle("宠物选择器")
        # self.setGeometry(300, 300, 800, 600)  # 增大窗口尺寸

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 外边距

        # 设置背景颜色和整体风格
        self.setStyleSheet(
            "background-color: #FAF3E0;"  # 淡米色背景
            "font-family: 'FangSong';"  # 修改字体为仿宋
            "font-size: 40px;"  # 增大字体
        )

        # 创建圆角区块
        self.mainBlock = QtWidgets.QWidget(self)
        self.mainBlock.setGeometry(50, 70, 700, 500)
        self.mainBlock.setStyleSheet(
            "background-color: #FFF8DC;"  # 浅米黄色背景
            "border-radius: 20px;"  # 圆角效果
            "border: 2px solid #DEB887;"  # 边框
        )

        # 创建标题标签
        self.titleLabel = QtWidgets.QLabel("请选择一个宠物：", self.mainBlock)
        self.titleLabel.setFont(QtGui.QFont("FangSong", 40))  # 修改标题字体为仿宋
        self.titleLabel.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;  /* 设置字体颜色为白色 */
                background-color: #8B4513;  /* 设置背景颜色为深棕色 */
                border-radius: 10px;  /* 可选，设置圆角效果 */
                padding: 10px;  /* 可选，设置内部填充 */
            }
            """
        )
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setGeometry(100, 20, 500, 80)  # 调整标题位置和尺寸

        # 创建按钮：小猫
        self.Cat_button = QtWidgets.QPushButton("小猫", self.mainBlock)
        self.Cat_button.clicked.connect(self.startCat)
        self.Cat_button.setGeometry(50, 120, 250, 80)  # 调整按钮位置
        self.styleButton(self.Cat_button)

        # 创建按钮：棕色线条小狗
        self.DogBrown_button = QtWidgets.QPushButton("棕色线条小狗", self.mainBlock)
        self.DogBrown_button.clicked.connect(self.startDogBrown)
        self.DogBrown_button.setGeometry(400, 120, 250, 80)  # 调整按钮位置
        self.styleButton(self.DogBrown_button)

        # 创建按钮：白色线条小狗
        self.DogWhite_button = QtWidgets.QPushButton("白色线条小狗", self.mainBlock)
        self.DogWhite_button.clicked.connect(self.startDogWhite)
        self.DogWhite_button.setGeometry(50, 240, 250, 80)  # 调整按钮位置
        self.styleButton(self.DogWhite_button)

        # 创建按钮：小兔子
        self.Rabbit_button = QtWidgets.QPushButton("小兔子", self.mainBlock)
        self.Rabbit_button.clicked.connect(self.startRabbit)
        self.Rabbit_button.setGeometry(400, 240, 250, 80)  # 调整按钮位置
        self.styleButton(self.Rabbit_button)

        # 创建按钮：蜡笔小新
        self.Xiaoxin_button = QtWidgets.QPushButton("蜡笔小新", self.mainBlock)
        self.Xiaoxin_button.clicked.connect(self.startXiaoxin)
        self.Xiaoxin_button.setGeometry(225, 360, 250, 80)  # 居中按钮
        self.styleButton(self.Xiaoxin_button)

    def styleButton(self, button):
        button.setStyleSheet(
            "background-color: #FFF8DC;"  # 浅米黄色背景
            "color: #8B4513;"  # 深棕色字体
            "border: 2px solid #DEB887;"  # 浅棕边框
            "border-radius: 15px;"  # 圆角效果
            "padding: 5px;"
        )

    def startCat(self):
        self.pet = Cat()
        self.pet.startIdle()
        self.pet.show()
        self.hide()

    def startDogBrown(self):
        self.pet = DogBrown()
        self.pet.startIdle()
        self.pet.show()
        self.hide()

    def startDogWhite(self):
        self.pet = DogWhite()
        self.pet.startIdle()
        self.pet.show()
        self.hide()

    def startRabbit(self):
        self.pet = Rabbit()
        self.pet.startIdle()
        self.pet.show()
        self.hide()

    def startXiaoxin(self):
        self.pet = Xiaoxin()
        self.pet.show()
        self.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    selector = PetSelector()
    selector.show()
    sys.exit(app.exec_())
