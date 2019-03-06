# encoding: utf-8
'''
@author: weiyang_tang
@contact: weiyang_tang@126.com
@file: login.py
@time: 2019-03-04 10:07
@desc:
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from passwordManage import APP


class APP_login(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.userNameLabel = QLabel('账号')
        self.userName = QLineEdit()
        self.passwordLabel = QLabel('密码')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.loginButon = QPushButton('登录')
        self.loginButon.clicked.connect(self.login)

        self.userNameLabel.setFont(QFont("Roman times", 15, QFont.Bold))
        self.userName.setFont(QFont("Roman times", 10, QFont.Bold))
        self.passwordLabel.setFont(QFont("Roman times", 15, QFont.Bold))
        self.password.setFont(QFont("Roman times", 10, QFont.Bold))
        self.loginButon.setFont(QFont("Roman times", 15, QFont.Bold))

        hbox = QHBoxLayout()
        hbox.addStretch(1)  # 空白的地方分割比
        hbox.addWidget(self.userNameLabel)
        hbox.addWidget(self.userName)
        hbox.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.passwordLabel)
        hbox2.addWidget(self.password)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.loginButon)
        hbox3.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)

        widGet = QWidget()
        widGet.setLayout(vbox)
        self.set_palette()
        self.setCentralWidget(widGet)

        self.resize(600, 400)
        self.center()
        self.setWindowTitle('密码管理器')
        self.setWindowIcon(QIcon('APP.jpg'))
        self.show()

    def center(self):  # 窗口居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_palette(self):
        # 不设置也可以
        self.setAutoFillBackground(True)
        palette = QPalette()
        # 设置背景颜色
        # palette.setColor(self.backgroundRole(), QColor(192, 253, 123))
        # 设置背景图片
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap('bg.jpg')))
        self.setPalette(palette)

    def login(self):
        # self.app = APP()
        # self.setCentralWidget(self.app)
        self.close()
        self.app = APP()
        self.app.show()
        # userName = self.userName.text()
        # password = self.password.text()
        # print(userName, password)
        # reply = QMessageBox.information(self,  # 使用infomation信息框
        #                                 "密码",
        #                                 password,
        #                                 QMessageBox.Yes | QMessageBox.No)
        # print(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = APP_login()
    ex.show()
    sys.exit(app.exec_())
