# -*- coding: utf-8 -*-
# !/usr/bin/python3
# author: Gavin Xue
# last edit: 20190201

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from sensors import SensorsProject, EventDesign
from PyQt5.QtWidgets import QApplication
import sys
import os


class Login(QtWidgets.QMainWindow):
    login_success = QtCore.pyqtSignal(SensorsProject)

    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.location_on_the_screen()
        self.sa = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(665, 228)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 20, 67, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.verticalLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(30, 0, 150, 150))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("{}/icons/running_man.png".
                                                format(os.path.dirname(os.path.realpath(sys.argv[0])))))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(300, 20, 301, 116))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(200, 20, 20, 110))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.url = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.url.setClearButtonEnabled(True)
        self.url.setObjectName("url")
        self.gridLayout_2.addWidget(self.url, 1, 0, 1, 1)

        self.project = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.project.setClearButtonEnabled(True)
        self.project.setObjectName("project")
        self.gridLayout_2.addWidget(self.project, 2, 0, 1, 1)

        self.user_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.user_name.setClearButtonEnabled(True)
        self.user_name.setObjectName("user_name")
        self.gridLayout_2.addWidget(self.user_name, 3, 0, 1, 1)

        self.password = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout_2.addWidget(self.password, 4, 0, 1, 1)

        self.url.raise_()
        self.project.raise_()
        self.user_name.raise_()
        self.password.raise_()

        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(250, 150, 141, 32))
        self.login_btn.setObjectName("login_btn")
        self.sa = self.login_btn.clicked.connect(self.login_access)

        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.setGeometry(QtCore.QRect(430, 150, 141, 32))
        self.exit_btn.setObjectName("exit_btn")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 665, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.exit_btn.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SA工具箱"))
        self.label.setText(_translate("MainWindow", "SA 网址："))
        self.label_3.setText(_translate("MainWindow", "用户名："))
        self.label_2.setText(_translate("MainWindow", "密码："))
        self.label_4.setText(_translate("MainWindow", "项目名称："))
        self.login_btn.setText(_translate("MainWindow", "登录"))
        self.exit_btn.setText(_translate("MainWindow", "退出"))
        self.statusbar.setStatusTip("Developed by Gavin Xue")

    def location_on_the_screen(self):
        sg = QtWidgets.QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = sg.width() - widget.width()
        y = sg.height() - widget.height()
        self.move(x / 2, y / 2)

    def login_access(self):
        try:
            sa_url = self.url.text()
            sa_project = self.project.text()
            sa_user = self.user_name.text()
            sa_pw = self.password.text()
            sa = SensorsProject(sa_url, sa_project, sa_user, sa_pw)
            if sa.error:
                QMessageBox.warning(self,
                                    "error",
                                    sa.error,
                                    QMessageBox.Yes)
            if sa.token:
                self.login_success.emit(sa)

        except Exception as e:
            QMessageBox.warning(self,
                                "error",
                                str(e),
                                QMessageBox.Yes)


class HomePage(QtWidgets.QMainWindow):
    go_export_design = QtCore.pyqtSignal()
    upload_design_success = QtCore.pyqtSignal(EventDesign)
    go_error_page = QtCore.pyqtSignal(str)
    go_update_cname_page = QtCore.pyqtSignal(SensorsProject, EventDesign)

    def __init__(self, sa=SensorsProject()):
        self.sa = sa
        super(HomePage, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.location_on_the_screen()
        self.upload_design = EventDesign()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 30, 221, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # add a line to split event upload
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(330, 30, 31, 281))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # upload event design description
        self.label_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_desc.setGeometry(QtCore.QRect(380, 30, 221, 16))
        self.label_desc.setFont(font)
        self.label_desc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_desc.setObjectName("label_desc")

        btn_font = QtGui.QFont()
        btn_font.setBold(True)
        btn_font.setWeight(75)

        # upload event design func
        self.upload_design_btn = QtWidgets.QPushButton(self.centralwidget)
        self.upload_design_btn.setGeometry(QtCore.QRect(370, 60, 250, 30))
        self.upload_design_btn.setStatusTip("点击按钮上传事件设计")
        self.upload_design_btn.setFont(btn_font)
        self.upload_design_btn.setObjectName("upload_design_btn")
        self.upload_design_btn.clicked.connect(self.upload_event_design)

        # event design information widget
        self.event_info = QtWidgets.QWidget(self.centralwidget)
        self.event_info.setGeometry(QtCore.QRect(380, 90, 250, 221))
        self.event_info.setObjectName("widget")

        self.event_desc = QtWidgets.QLabel(self.event_info)
        self.event_desc.setObjectName("event_desc")

        self.event_tips = QtWidgets.QLabel(self.event_info)
        self.event_tips.setEnabled(False)
        self.event_tips.setGeometry(QtCore.QRect(0, 190, 251, 31))
        self.event_tips.setObjectName("event_tips")

        self.event_info.hide()

        # export event design of current
        self.export_design = QtWidgets.QPushButton(self.centralwidget)
        self.export_design.setGeometry(QtCore.QRect(70, 60, 251, 30))
        self.export_design.setFont(btn_font)
        self.export_design.setObjectName("export_design")
        self.export_design.clicked.connect(self.export_event_design)

        # check error of argument e_name and c_name
        self.check_coherence_btn = QtWidgets.QPushButton(self.centralwidget)
        self.check_coherence_btn.setGeometry(QtCore.QRect(70, 100, 250, 30))
        self.check_coherence_btn.setFont(btn_font)
        self.check_coherence_btn.setObjectName("check_coherence_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.check_coherence_btn.clicked.connect(self.check_coherence)

        # update cname from event design
        self.update_cname_btn = QtWidgets.QPushButton(self.centralwidget)
        self.update_cname_btn.setGeometry(QtCore.QRect(70, 140, 250, 30))
        self.update_cname_btn.setFont(btn_font)
        self.update_cname_btn.setObjectName("update_cname_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.update_cname_btn.clicked.connect(self.go_update_cname)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SA工具箱"))
        self.export_design.setText(_translate("MainWindow", "导出当前环境事件&属性"))
        self.label.setText(_translate("MainWindow", "欢迎进入工具箱，请需要使用的功能"))
        self.label_desc.setText(_translate("MainWindow", "请点此上传环境事件设计"))
        self.upload_design_btn.setText(_translate("MainWindow", "上传事件设计"))
        self.event_desc.setText(_translate("MainWindow", "事件数量："))
        self.event_tips.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">"
                                        "请检查事件设计描述是否异常！<br/>如有异常请重新上传符合神策标准模板"
                                        "的事件设计！</span></p></body></html>"))
        self.check_coherence_btn.setText(_translate("MainWindow", "事件设计中英文变量一致性校验"))
        self.update_cname_btn.setText(_translate("MainWindow", "批量更新 事件/属性 显示名"))
        self.statusbar.setStatusTip("Developed by Gavin Xue")

    def location_on_the_screen(self):
        sg = QtWidgets.QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = sg.width() - widget.width()
        y = sg.height() - widget.height()
        self.move(x / 2, y / 2)

    def upload_event_design(self):
        filename, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "Select a event design file",
                                                         "./",
                                                         "excel (*.xls, *.xlsx)")
        try:
            if filename:
                self.upload_design.upload_event_design(filename)
                event_desc = "<br>文件名：{}<br>".format(self.upload_design.filename.split('/')[-1]) + \
                             "事件去重数：{}<br>".format(self.upload_design.event_qty) + \
                             "属性去重数：{}<br>".format(self.upload_design.prop_qty)
                self.event_desc.setText(event_desc)
                self.event_info.show()
                self.upload_design_success.emit(self.upload_design)

        except Exception as e:
            # 上传失败时，将原有的上传的事件设计设置为空对象
            self.event_info.hide()
            self.upload_design_success.emit(self.upload_design)
            QMessageBox.warning(self,
                                "error",
                                str(e),
                                QMessageBox.Yes)

    def export_event_design(self):
        """Export event design from SA project

        Returns:
            None
        """
        try:
            self.sa.export_event_design()
            QMessageBox.information(self,
                                    'info',
                                    '导出已完成，请查看当前文件夹下文件 export_event_design.xlsx',
                                    QMessageBox.Yes)
        except Exception as e:
            QMessageBox.warning(self,
                                "error",
                                str(e),
                                QMessageBox.Yes)

    def check_coherence(self):
        try:
            if self.upload_design.event_table.empty:
                raise Exception('请先上传正确的事件设计，再使用此功能！')
            self.upload_design.check_prop_coherence()
            if self.upload_design.prop_coherence_error:
                error_str = '<br>'.join(self.upload_design.prop_coherence_error)
                self.go_error_page.emit(error_str)
            else:
                QMessageBox.warning(self,
                                    "info",
                                    "太棒了！没有任何错误出现！",
                                    QMessageBox.Yes)

        except Exception as e:
            QMessageBox.warning(self,
                                "error",
                                str(e),
                                QMessageBox.Yes)

    def go_update_cname(self):
        try:
            if self.upload_design.event_table.empty:
                raise Exception('请先上传正确的事件设计，再使用此功能！')
            else:
                self.go_update_cname_page.emit(self.sa, self.upload_design)

        except Exception as e:
            QMessageBox.warning(self,
                                "error",
                                str(e),
                                QMessageBox.Yes)


class ErrorDisplay(QtWidgets.QMainWindow):
    back_homepage = QtCore.pyqtSignal(QtWidgets.QMainWindow)

    def __init__(self, errors=None):
        super(ErrorDisplay, self).__init__()
        self.errors = errors
        self.setupUi(self)
        self.retranslateUi(self)
        self.location_on_the_screen()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 50, 621, 281))
        self.textBrowser.setObjectName("textBrowser")
        self.back_homepage_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_homepage_btn.setGeometry(QtCore.QRect(160, 10, 151, 32))
        self.back_homepage_btn.setObjectName("back_homepage_btn")
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.setGeometry(QtCore.QRect(350, 10, 151, 32))
        self.exit_btn.setObjectName("exit_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 处理操作信息
        self.exit_btn.clicked.connect(sys.exit)
        self.back_homepage_btn.clicked.connect(self.back_home)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "错误检查"))
        if self.errors:
            self.textBrowser.setHtml(_translate("MainWindow", "{}".format(self.errors)))
        self.back_homepage_btn.setText(_translate("MainWindow", "返回工具箱主页"))
        self.exit_btn.setText(_translate("MainWindow", "退出工具"))
        self.statusbar.setStatusTip("Developed by Gavin Xue")

    def location_on_the_screen(self):
        sg = QtWidgets.QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = sg.width() - widget.width()
        y = sg.height() - widget.height()
        self.move(x/2, y/2)

    def back_home(self):
        self.back_homepage.emit(self)


class UpdateCname(QtWidgets.QMainWindow):
    back_homepage = QtCore.pyqtSignal(QtWidgets.QMainWindow)

    def __init__(self, sa=SensorsProject(), upload_design=EventDesign()):
        super(UpdateCname, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.location_on_the_screen()
        self.sa = sa
        self.upload_design = upload_design

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 400)
        font = QtGui.QFont()
        font.setFamily(".PingFang HK")
        MainWindow.setFont(font)
        MainWindow.setStatusTip("")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(270, 10, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")

        self.choose_update_event = QtWidgets.QCheckBox(self.centralwidget)
        self.choose_update_event.setGeometry(QtCore.QRect(260, 70, 200, 30))
        choice_font = QtGui.QFont()
        choice_font.setPointSize(15)
        self.choose_update_event.setFont(choice_font)
        self.choose_update_event.setObjectName("choose_update_event")

        self.choose_update_prop = QtWidgets.QCheckBox(self.centralwidget)
        self.choose_update_prop.setGeometry(QtCore.QRect(260, 110, 200, 30))
        self.choose_update_prop.setFont(choice_font)
        self.choose_update_prop.setObjectName("choose_update_prop")

        self.choose_cover_old = QtWidgets.QCheckBox(self.centralwidget)
        self.choose_cover_old.setGeometry(QtCore.QRect(260, 150, 200, 30))
        self.choose_cover_old.setFont(choice_font)
        self.choose_cover_old.setObjectName("choose_cover_old")

        self.comment_label = QtWidgets.QLabel(self.centralwidget)
        self.comment_label.setGeometry(QtCore.QRect(40, 300, 461, 31))
        self.comment_label.setObjectName("comment_label")

        self.submit_update_btn = QtWidgets.QPushButton(self.centralwidget)
        self.submit_update_btn.setGeometry(QtCore.QRect(180, 210, 151, 32))
        self.submit_update_btn.setObjectName("submit_update_btn")

        self.back_homepage_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_homepage_btn.setGeometry(QtCore.QRect(380, 210, 151, 32))
        self.back_homepage_btn.setObjectName("back_homepage_btn")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.back_homepage_btn.clicked.connect(self.back_home)
        self.submit_update_btn.clicked.connect(self.update_submit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SA工具箱-更新中文名"))
        self.title_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#7f7f7f;\">批量更新中文显示名</span></p></body></html>"))
        self.choose_update_event.setText(_translate("MainWindow", " 选择更新事件中文显示名"))
        self.choose_update_prop.setText(_translate("MainWindow", " 选择更新属性中文显示名"))
        self.choose_cover_old.setText(_translate("MainWindow", " 选择覆盖环境已有显示名"))
        self.comment_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; color:#b3b3b3;\">注释1：批量更新中文显示名，是依据上传的事件设计中的内容，进行对应的更新，请先上传事件设计<br/>注释2：选择覆盖更新后，将根据事件设计中的中文名，将环境中对应的全部更新，请慎用</span></p></body></html>"))
        self.submit_update_btn.setText(_translate("MainWindow", "确认更新"))
        self.back_homepage_btn.setText(_translate("MainWindow", "返回工具箱首页"))
        self.statusbar.setStatusTip("Developed by Gavin Xue")

    def location_on_the_screen(self):
        sg = QtWidgets.QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = sg.width() - widget.width()
        y = sg.height() - widget.height()
        self.move(x/2, y/2)

    def back_home(self):
        self.back_homepage.emit(self)

    def update_submit(self):
        if not self.choose_update_event.isChecked() and not self.choose_update_prop.isChecked():
            QMessageBox.warning(self,
                                "error",
                                "请至少选择更新事件或属性显示名中的一项或多项！",
                                QMessageBox.Yes)
        else:
            try:
                result = self.sa.update_cname(self.upload_design, self.choose_update_event.isChecked(),
                                              self.choose_update_prop.isChecked(), self.choose_cover_old.isChecked())
                QMessageBox.warning(self,
                                    "info",
                                    result,
                                    QMessageBox.Yes)
            except Exception as e:
                QMessageBox.warning(self,
                                    "error",
                                    str(e),
                                    QMessageBox.Yes)


if __name__ == '__main__':
    # import sys
    app = QApplication(sys.argv)
    tmp_window = UpdateCname(SensorsProject(), EventDesign())
    tmp_window.show()
    sys.exit(app.exec_())