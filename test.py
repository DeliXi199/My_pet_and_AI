from PyQt5 import QtWidgets, QtCore, QtGui
import SparkApi


class AIChatApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 去掉默认的标题栏
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.resize(1200, 800)

        # 主布局（外层背景）
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 外边距
        main_layout.setSpacing(0)

        # 主容器（圆角背景）
        main_container = QtWidgets.QWidget(self)
        main_container.setStyleSheet(
            """
            QWidget {
                background-color: #fff8dc;
                border: 3px solid #8b5a2b;
                border-radius: 20px;
            }
        """
        )
        container_layout = QtWidgets.QVBoxLayout(main_container)
        container_layout.setContentsMargins(10, 10, 10, 10)  # 内边距
        container_layout.setSpacing(10)

        # 添加阴影效果
        shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setOffset(5, 5)
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 100))  # 半透明的黑色阴影
        main_container.setGraphicsEffect(shadow_effect)

        # 自定义标题栏
        self.titleBar = QtWidgets.QWidget(main_container)
        self.titleBar.setFixedHeight(50)
        self.titleBar.setStyleSheet(
            """
            QWidget {
                background-color: #8b5a2b;
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            }
        """
        )
        title_layout = QtWidgets.QHBoxLayout(self.titleBar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        self.titleLabel = QtWidgets.QLabel("聊天界面", self.titleBar)
        self.titleLabel.setStyleSheet(
            """
            QLabel {
                font-family: 'FangSong';
                font-size: 35px;
                color: #ffffff;
            }
        """
        )
        title_layout.addWidget(self.titleLabel)

        self.minimizeButton = QtWidgets.QPushButton("-", self.titleBar)
        self.minimizeButton.setFixedSize(30, 30)
        self.minimizeButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffdead;
                border: 2px solid #8b5a2b;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ffd700;
            }
        """
        )
        self.minimizeButton.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.minimizeButton)

        self.closeButton = QtWidgets.QPushButton("×", self.titleBar)
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ff6347;
                color: white;
                border: 2px solid #8b5a2b;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """
        )
        self.closeButton.clicked.connect(self.close)
        title_layout.addWidget(self.closeButton)

        container_layout.addWidget(self.titleBar)

        # 聊天记录显示区域
        self.chatDisplay = QtWidgets.QTextBrowser(main_container)
        self.chatDisplay.setPlaceholderText("我们开始聊天吧...")
        self.chatDisplay.setStyleSheet(
            """
            QTextBrowser {
                font-family: 'FangSong';
                font-size: 40px;
                color: #333;
                background-color: #fdf5e6;
                border: 2px solid #8b5a2b;
                border-radius: 10px;
                padding: 10px;
            }
        """
        )
        container_layout.addWidget(self.chatDisplay)

        # 输入框和按钮区域
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setSpacing(10)

        self.inputField = QtWidgets.QLineEdit(main_container)
        self.inputField.setPlaceholderText("请输入聊天内容...")
        self.inputField.setStyleSheet(
            """
            QLineEdit {
                font-family: 'FangSong';
                font-size: 40px;
                border: 2px solid #8b5a2b;
                border-radius: 10px;
                padding: 8px;
                background-color: #fffaf0;
            }
        """
        )
        self.inputField.returnPressed.connect(self.processInput)
        input_layout.addWidget(self.inputField)

        self.sendButton = QtWidgets.QPushButton("发送", main_container)
        self.sendButton.setStyleSheet(
            """
            QPushButton {
                font-family: 'FangSong';
                font-size: 40px;
                background-color: #ffdead;
                color: #8b4513;
                border: 2px solid #8b5a2b;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #ffe4b5;
            }
            QPushButton:pressed {
                background-color: #ffc125;
            }
        """
        )
        self.sendButton.clicked.connect(self.processInput)
        input_layout.addWidget(self.sendButton)

        container_layout.addLayout(input_layout)
        main_layout.addWidget(main_container)

        # 初始化对话上下文
        self.text = []

        # 用于窗口拖动的属性
        self.isDragging = False
        self.dragPosition = QtCore.QPoint()

    def processInput(self):
        user_input = self.inputField.text().strip()
        if not user_input:
            self.chatDisplay.append(
                "<span style='color: gray;'>你: [请输入内容]</span>"
            )
            return

        # 显示用户输入
        self.chatDisplay.append(f"<b>你:</b> {user_input}")

        # 添加到对话上下文
        self.text = self.getText("user", user_input)

        # 清空输入框
        self.inputField.clear()

        # 调用 AI 接口
        self.chatDisplay.append(
            "<span style='color: blue;'><b>宠物:</b> [正在思考...]</span>"
        )
        QtCore.QCoreApplication.processEvents()  # 刷新界面显示“正在思考...”

        # 调用 Spark API 获取回答
        try:
            SparkApi.answer = ""
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, self.text)
            ai_response = SparkApi.answer.strip()
            if not ai_response:
                ai_response = "抱歉，我不知道该如何回答。"
        except Exception as e:
            ai_response = f"出现错误: {e}"

        # 显示 AI 的回答
        self.chatDisplay.append(
            f"<span style='color: green;'><b>宠物:</b> {ai_response}</span>"
        )
        self.getText("assistant", ai_response)

    def getText(self, role, content):
        jsoncon = {"role": role, "content": content}
        self.text.append(jsoncon)
        return self.checklen(self.text)

    def getlength(self, text):
        return sum(len(content["content"]) for content in text)

    def checklen(self, text):
        while self.getlength(text) > 8000:
            del text[0]
        return text


# Spark API 配置
appid = "a6ce1da9"  # 填写控制台中获取的 APPID 信息
api_secret = "NTlhMjMzM2ExOTI5MmRhZTc3Njk3NGZl"  # 填写控制台中获取的 APISecret 信息
api_key = "4e046fe5728dc6fdba7f80d11ac4f075"  # 填写控制台中获取的 APIKey 信息
domain = "4.0Ultra"  # 模型版本
Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # 服务地址

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    chat_app = AIChatApp()
    chat_app.show()
    app.exec_()
