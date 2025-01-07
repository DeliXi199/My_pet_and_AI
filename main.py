# main.py
import sys
from PyQt5 import QtWidgets
from petXiaoxin import Xiaoxin

def main():
    app = QtWidgets.QApplication(sys.argv)  # 创建应用实例
    pet = Xiaoxin()  # 直接创建 Xiaoxin 宠物实例
    pet.show()  # 显示 Xiaoxin 宠物
    sys.exit(app.exec_())  # 运行应用并退出

if __name__ == '__main__':
    main()
