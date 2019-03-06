# encoding: utf-8
'''
@author: weiyang_tang
@contact: weiyang_tang@126.com
@file: passwordManage.py
@time: 2019-03-04 16:23
@desc:
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from inputDemo import Dialog
from db import DbManager
import xlwt
import os
import json


class DataProcess(QThread):
    sinOut = pyqtSignal(tuple)  # 信号槽

    def __init__(self, option, userInfo=None):  # 初始化
        super().__init__()
        self.option = option
        self.userInfo = userInfo
        self.dbManager = DbManager()

    def run(self):
        if self.option == 1:  # 添加信息
            flag = self.insertInfo()
            if flag > 0:
                print('添加成功')
        elif self.option == 2:
            values = self.findAllUserInfo()
            print(values)
        elif self.option == 3:
            values = self.deleteUserInfo()
            print(values)
        elif self.option == 4:
            values = self.updateUserInfo()
            print(values)
        elif self.option == 5:
            self.outData()
            # print(values)

    def insertInfo(self):  # 添加账号密码

        if len(self.userInfo) >= 3:
            sql = 'INSERT INTO pwdinfo(webName,userName,pwd) VALUES(%(webName)s,%(userName)s,%(pwd)s)'
            params = self.userInfo
            flag = self.dbManager.edit(sql=sql, params=params)
            values = (flag,)
            self.sinOut.emit(values)
            return flag

    def findAllUserInfo(self):
        sql = 'SELECT * FROM pwdinfo'
        values = self.dbManager.fetchall(sql=sql)
        self.sinOut.emit(values)

    def deleteUserInfo(self):

        sql = 'DELETE FROM pwdinfo WHERE id=%(id)s'
        params = self.userInfo
        flag = self.dbManager.edit(sql=sql, params=params)
        values = (flag,)
        self.sinOut.emit(values)
        return flag

    def updateUserInfo(self):

        sql = 'UPDATE pwdinfo SET webName=%(webName)s,userName=%(userName)s,pwd=%(pwd)s WHERE id=%(id)s'
        params = self.userInfo
        flag = self.dbManager.edit(sql=sql, params=params)
        values = (flag,)
        self.sinOut.emit(values)
        return flag

    def outData(self):
        # dirPath = QFileDialog.getExistingDirectory(self, '保存位置', './')
        # dir_choose = QFileDialog.getExistingDirectory("选取文件夹", '.')  # 起始路径

        sql = 'SELECT * FROM pwdinfo'
        values = self.dbManager.fetchall(sql=sql)

        myWorkbook = xlwt.Workbook()
        mySheet = myWorkbook.add_sheet('网站账号信息')

        for i in range(1, len(values)):
            for j in range(1, len(values[i])):
                print(i, j, values[i][j])
                mySheet.write(i, j - 1, str(values[i][j]))

        mySheet.write(0, 0, '网站')
        mySheet.write(0, 1, '账号')
        mySheet.write(0, 2, '密码')
        # filePath = os.path.join(dirPath, 'password.xls')
        myWorkbook.save('password.xls')
        self.sinOut.emit((1,))


class APP(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        # 实现的效果是一样的，四行三列，所以要灵活运用函数，这里只是示范一下如何单独设置行列
        self.tableWidget = QTableWidget(100, 5)

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        self.tableWidget.setHorizontalHeaderLabels(['编号', '网站系统', '账号', '密码', '备注'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # newItem = QTableWidgetItem('1')
        # tableWidget.setItem(0, 0, newItem)
        #
        # newItem = QTableWidgetItem('男')
        # tableWidget.setItem(0, 1, newItem)
        #
        # newItem = QTableWidgetItem('160')
        # tableWidget.setItem(0, 2, newItem)

        # TODO 优化 2 设置水平方向表格为自适应的伸缩模式
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # TODO 优化3 将表格变为禁止编辑
        # tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # TODO 优化 4 设置表格整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # TODO 优化 5 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(self.tableWidget)
        QTableWidget.resizeRowsToContents(self.tableWidget)

        # TOdo 优化7 在单元格内放置控件

        # searchBtn = QPushButton('修改')
        # searchBtn.setDown(True)
        # searchBtn.setStyleSheet('QPushButton{margin:3px}')
        # tableWidget.setCellWidget(0, 2, searchBtn)
        hbox.addWidget(self.tableWidget)
        # tableWidget.currentItem().row()

        vbox = QVBoxLayout()  # 右边

        addBtn = QPushButton('添加密码')
        deleteBtn = QPushButton('删除密码')
        updateBtn = QPushButton('修改密码')
        outBtn = QPushButton('导出excel')

        addBtn.clicked.connect(self.insertUserInfo)
        deleteBtn.clicked.connect(self.deleteData)
        updateBtn.clicked.connect(self.updateData)
        outBtn.clicked.connect(self.outData)

        vbox.addStretch(1)
        vbox.addWidget(addBtn)
        vbox.addStretch(1)
        vbox.addWidget(deleteBtn)
        vbox.addStretch(1)
        vbox.addWidget(updateBtn)
        vbox.addStretch(1)
        vbox.addWidget(outBtn)
        vbox.addStretch(1)

        grid = QGridLayout()  # 整体框架，网格布局
        grid.setSpacing(10)

        grid.addLayout(hbox, 1, 0, 3, 1)
        grid.addLayout(vbox, 1, 1, 1, 1)

        self.setLayout(grid)

        self.resize(1000, 400)
        self.center()
        self.setWindowTitle('密码管理器')
        self.setWindowIcon(QIcon('APP.jpg'))
        self.show()

        self.initData()

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

    def inputDatas(self):
        print()

    # self.app = inputData()
    # self.app.show()

    #  添加数据
    def insertUserInfo(self):
        userInfo = Dialog.getResult(self)
        print('用户信息', userInfo)
        params = {'webName': userInfo[0], 'userName': userInfo[1], 'pwd': userInfo[2]}
        self.thread = DataProcess(option=1, userInfo=params)
        self.thread.sinOut.connect(self.slot_insertUserInfo)
        self.thread.start()

    def slot_insertUserInfo(self, tuple):
        print('结果为', tuple[0])
        self.tableWidget.clearContents()
        self.initData()

    # 数据初始化
    def initData(self):
        self.thread = DataProcess(option=2)
        self.thread.sinOut.connect(self.slot_initData)
        self.thread.start()

    def slot_initData(self, tuple):
        print('信息为', tuple)

        for i in range(len(tuple)):
            for j in range(len(tuple[i])):
                print(i, j, tuple[i][j])
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(tuple[i][j])))  # 只能为字符串
        # self.tableWidget.setItem(0, 0, QTableWidgetItem(0))

    def deleteData(self):

        rowIndex = self.tableWidget.currentRow()  # 获取所选的单元格的行号
        id = self.tableWidget.item(rowIndex, 0).text()
        webName = self.tableWidget.item(rowIndex, 1).text()

        reply = QMessageBox.information(self, '警告', '是否删除' + webName + ",注意该操作无法恢复.", QMessageBox.Ok,
                                        QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            params = {'id': id}
            self.thread = DataProcess(option=3, userInfo=params)
            self.thread.sinOut.connect(self.slot_deleteData)
            self.thread.start()

    def slot_deleteData(self, tuple):
        flag = tuple[0]
        self.tableWidget.clearContents()
        self.initData()
        if flag > 0:
            reply = QMessageBox.information(self, '提示', '删除成功')

    def updateData(self):
        rowIndex = self.tableWidget.currentRow()  # 获取所选的单元格的行号
        id = self.tableWidget.item(rowIndex, 0).text()
        webName = self.tableWidget.item(rowIndex, 1).text()
        userName = self.tableWidget.item(rowIndex, 2).text()
        pwd = self.tableWidget.item(rowIndex, 3).text()
        params = {'id': id, 'webName': webName, 'userName': userName, 'pwd': pwd}
        userInfo = Dialog.getResult(self)
        self.thread = DataProcess(option=4, userInfo=userInfo)
        self.thread.sinOut.connect(self.slot_deleteData)
        self.thread.start()

    def slot_updateData(self, tuple):
        flag = tuple[0]
        self.tableWidget.clearContents()
        self.initData()
        if flag > 0:
            reply = QMessageBox.information(self, '提示', '修改成功')

    def outData(self):
        self.thread = DataProcess(option=5)
        self.thread.sinOut.connect(self.slot_outData)
        self.thread.start()

    def slot_outData(self, tuple):
        flag = tuple[0]
        if flag > 0:
            reply = QMessageBox.information(self, '提示', '账号密码导出成功,导出到当前文件夹下')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = APP()
    sys.exit(app.exec_())
