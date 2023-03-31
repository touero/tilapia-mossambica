#  导入时间包
import time
#  导入操作mysql包
import pymysql
#  导入操作系统包
import sys
#  导入win10提示窗包
from win10toast import ToastNotifier
#  Pyqt导入包
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
# 导入登录界面UI文件
from sign_in import Ui_Form
# 导入此系统界面UI文件
from newmainui import Ui_MainWindow


# 向数据库提交的两个方法，submit1：返回结果的提交 submit2：影响几行的提交
def submit1(sql):
    conn = pymysql.connect(host='localhost', user='root', password='root', database='librarymanagementsystem',
                           port=3306)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def submit2(sql):
    conn = pymysql.connect(host='localhost', user='root', password='root', database='librarymanagementsystem',
                           port=3306)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# win10提示窗的方法 参数1：标题 参数2：内容
def message(title, content):
    ToastNotifier().show_toast(title, content, icon_path=None, duration=3, threaded=True)


# 登录界面的类继承
class Window1(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(Window1, self).__init__()
        self.setupUi(self)

    def log_in(self):
        sql = "SELECT * FROM login WHERE username='{}' ".format(self.lineEdit.text())
        loginpassword = submit1(sql)
        if loginpassword:
            if self.lineEdit_2.text() == loginpassword[0][1]:
                window1.pushButton.clicked.connect(lambda: {window1.close(), window2.show()})
            else:
                message('错误', '密码错误')
        else:
            message('错误', '找不到用户')


# 主界面的类继承
class Window2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        self.setupUi(self)
        # 三句给stackedWidget按钮切换
        self.listWidget.itemClicked.connect(self.switch_stack)
        self.listWidget.setCurrentRow(0)
        self.switch_stack()

    # 查询读者
    def find_readers(self):
        try:
            if self.lineEdit_54.text():
                if submit1("SELECT * FROM 读者信息 where 姓名='{}'".format(self.lineEdit_54.text())):
                    sql = "SELECT * FROM 读者信息 where 姓名='{}'".format(self.lineEdit_54.text())
                if submit1("SELECT * FROM 读者信息 where 借阅证号='{}'".format(self.lineEdit_54.text())):
                    sql = "SELECT * FROM 读者信息 where 借阅证号='{}'".format(self.lineEdit_54.text())
                if submit1("SELECT * FROM 读者信息 where 性别='{}'".format(self.lineEdit_54.text())):
                    sql = "SELECT * FROM 读者信息 where 性别='{}'".format(self.lineEdit_54.text())
                if submit1("SELECT * FROM 读者信息 where 单位='{}'".format(self.lineEdit_54.text())):
                    sql = "SELECT * FROM 读者信息 where 单位='{}'".format(self.lineEdit_54.text())
            else:
                message('消息', '查询不存在时记录无反应，空白查询显示全部')
                sql = "SELECT * FROM 读者信息"
            date = submit1(sql)
            line = 0
            self.tableWidget.setRowCount(int(len(date)))  # 重新设置行数
            for date1 in date:
                for i in date1:
                    newItem = QTableWidgetItem(i)  # 给tablewight中的位置赋值
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中显示
                    self.tableWidget.setItem(0, line, newItem)  # tablewight的位置
                    line += 1
        except:
            pass

    # 添加读者
    def add_reader(self):
        try:
            sql = "SELECT * FROM 读者信息 WHERE 借阅证号='{}' ".format(self.lineEdit_55.text())
            data = submit1(sql)
            if not data:
                if self.lineEdit_55.text() and self.lineEdit_56.text() and self.lineEdit_57.text():
                    if self.radioButton_25.isChecked():
                        sql = "insert 读者信息(借阅证号,姓名,性别,单位) values('{}','{}','{}','{}')".format(self.lineEdit_55.text(),
                                                                                              self.lineEdit_56.text(),
                                                                                              self.radioButton_25.text(),
                                                                                              self.lineEdit_57.text())
                        submit2(sql)
                        message('消息', '添加成功')
                        time.sleep(1.5)
                    if self.radioButton_26.isChecked():
                        sql = "insert 读者信息(借阅证号,姓名,性别,单位) values('{}','{}','{}','{}')".format(self.lineEdit_55.text(),
                                                                                              self.lineEdit_56.text(),
                                                                                              self.radioButton_26.text(),
                                                                                              self.lineEdit_57.text())
                        submit2(sql)
                        message("消息", "添加成功")
                        time.sleep(1.5)
                    else:
                        message("错误", "未选中性别")
                else:
                    message('错误', '添加数据不能为空')
            else:
                message('错误', '此读者存在或借阅证号重复')
        except:
            pass

    # 修改读者
    def updata_reader(self):
        try:
            if self.lineEdit_61.text() and self.lineEdit_61.text() != self.lineEdit_58.text():
                if self.lineEdit_58.text() and self.lineEdit_59.text() and self.lineEdit_60.text():
                    if submit1("SELECT * FROM 读者信息 where 姓名='{}'".format(self.lineEdit_61.text())):
                        if self.radioButton_27.isChecked():
                            sql = "update 读者信息 set 借阅证号='{}',姓名='{}',性别='{}',单位='{}' where 姓名='{}'".format(
                                self.lineEdit_58.text(), self.lineEdit_59.text(), self.radioButton_27.text(),
                                self.lineEdit_60.text(),
                                self.lineEdit_61.text())
                            submit2(sql)
                            message('消息', '添加成功')
                    if submit1("SELECT * FROM 读者信息 where 借阅证号='{}'".format(self.lineEdit_61.text())):
                        if self.radioButton_28.isChecked():
                            sql = "update 读者信息 set 借阅证号='{}',姓名='{}',性别='{}',单位='{}' where 借阅证号='{}'".format(
                                self.lineEdit_58.text(), self.lineEdit_59.text(), self.radioButton_28.text(),
                                self.lineEdit_60.text(),
                                self.lineEdit_61.text())
                            submit2(sql)
                            message('消息', '修改成功')
            else:
                message('消息', '此纪录不存在，数据不能为空, 或借阅证号重复')
        except:
            pass

    # 删除读者
    def delete_reader(self):
        while self.lineEdit_62.text():
            if submit1("select * FROM 读者信息 where 姓名='{}'".format(self.lineEdit_62.text())):
                sql = "delete FROM 读者信息 where 姓名='{}'".format(self.lineEdit_62.text())
                submit2(sql)
                message('消息', '删除成功')
                break
            if submit1("select * FROM 读者信息 where 借阅证号='{}'".format(self.lineEdit_62.text())):
                sql = "delete FROM 读者信息 where 借阅证号='{}'".format(self.lineEdit_62.text())
                submit2(sql)
                message('消息', '删除成功')
                break
            if submit1("select * FROM 读者信息 where 性别='{}'".format(self.lineEdit_62.text())):
                sql = "delete FROM 读者信息 where 性别='{}'".format(self.lineEdit_62.text())
                submit2(sql)
                message('消息', '删除成功')
                break
            if submit1("select * FROM 读者信息 where 单位='{}'".format(self.lineEdit_62.text())):
                sql = "delete FROM 读者信息 where 单位='{}'".format(self.lineEdit_62.text())
                submit2(sql)
                message('消息', '删除成功')
                break
            else:
                message('消息', '找不到此记录')
                break
        else:
            message('错误', '删除不能为空')

    # 方法 给stackedWidget按钮切换同上一起使用
    def switch_stack(self):
        try:
            i = self.listWidget.currentIndex().row()
            self.stackedWidget.setCurrentIndex(i)

        except Exception:
            pass


app = QtWidgets.QApplication(sys.argv)  # 初始化qt
window1 = Window1()  # 初始化登录界面
window2 = Window2()  # 初始化图书管理系统界面

if __name__ == '__main__':
    window1.show()
    sys.exit(app.exec_())
