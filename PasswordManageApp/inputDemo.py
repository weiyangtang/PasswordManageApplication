# encoding: utf-8
'''
@author: weiyang_tang
@contact: weiyang_tang@126.com
@file: inputDemo.py
@time: 2019-03-05 12:57
@desc:
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Dialog(QDialog):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        webNameLabel = QLabel('网站')
        self.webName = QLineEdit()
        # self.webName.setText()
        hbox1.addWidget(webNameLabel)
        hbox1.addWidget(self.webName)

        hbox2 = QHBoxLayout()
        userNameLabel = QLabel('账号')
        self.userName = QLineEdit()
        hbox2.addWidget(userNameLabel)
        hbox2.addWidget(self.userName)

        hbox3 = QHBoxLayout()
        pwdLabel = QLabel('密码')
        self.pwd = QLineEdit()
        hbox3.addWidget(pwdLabel)
        hbox3.addWidget(self.pwd)

        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)  # 点击ok，隐士存在该方法
        buttons.rejected.connect(self.reject)  # 点击cancel，该方法默认隐士存在
        vbox.addWidget(buttons)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

        self.resize(400, 200)
        self.center()
        self.setWindowTitle('输入密码')
        self.setWindowIcon(QIcon('APP.jpg'))
        self.show()

    def center(self):  # 窗口居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 设置背景图片
    def set_palette(self):
        # 不设置也可以
        self.setAutoFillBackground(True)
        palette = QPalette()
        # 设置背景颜色
        # palette.setColor(self.backgroundRole(), QColor(192, 253, 123))
        # 设置背景图片
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap('bg.jpg')))
        self.setPalette(palette)

    @staticmethod
    def getResult(self, parent=None):
        dialog = Dialog()
        result = dialog.exec_()
        webNameText = dialog.webName.text()
        userNameText = dialog.userName.text()
        pwdText = dialog.pwd.text()
        userInfo = [webNameText, userNameText, pwdText]
        print(userInfo)
        return (userInfo)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dialog()
    sys.exit(app.exec_())
