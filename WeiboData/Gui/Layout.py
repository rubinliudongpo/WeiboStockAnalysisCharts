# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created: Tue Oct 24 21:55:37 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWebEngineWidgets import QWebEngineView

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, dis_ambig):
        return QtWidgets.QApplication.translate(context, text, dis_ambig, _encoding)
except AttributeError:
    def _translate(context, text, dis_ambig):
        return QtWidgets.QApplication.translate(context, text, dis_ambig)


class Ui_Main_Window(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 1600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.widget.setGeometry(QtCore.QRect(10, 10, 258, 451))
        # self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.gridLayout.setObjectName("gridLayout")
        self.weibo_id_label = QtWidgets.QLabel(self.centralwidget)
        self.weibo_id_label.setObjectName("Weibo ID Label")
        self.gridLayout.addWidget(self.weibo_id_label, 0, 0, 1, 1)
        self.search_edit_text = QtWidgets.QLineEdit(self.centralwidget)
        self.search_edit_text.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.search_edit_text, 1, 0, 1, 2)
        self.start_date_label = QtWidgets.QLabel(self.centralwidget)
        self.start_date_label.setObjectName("Start Date")
        self.gridLayout.addWidget(self.start_date_label, 2, 0, 1, 1)
        self.end_date_label = QtWidgets.QLabel(self.centralwidget)
        self.end_date_label.setObjectName("End Date")
        self.gridLayout.addWidget(self.end_date_label, 2, 1, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.start_date_edit = QtWidgets.QDateEdit(self.splitter_2)
        self.start_date_edit.setObjectName("StartDateEdit")
        self.end_date_edit = QtWidgets.QDateEdit(self.splitter_2)
        self.end_date_edit.setObjectName("EndDateEdit")
        self.gridLayout.addWidget(self.splitter_2, 3, 0, 1, 2)
        self.splitter_1 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_1.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_1.setObjectName("splitter_1")
        self.comboBox = QtWidgets.QComboBox(self.splitter_1)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["D", "W", "M", "5", "15", "30", "60"])
        self.stock_combobox = QtWidgets.QComboBox(self.splitter_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stock_combobox.sizePolicy().hasHeightForWidth())
        self.stock_combobox.setSizePolicy(sizePolicy)
        self.stock_combobox.setObjectName("stock_combobox")
        self.stock_combobox.addItems(["K线", "复权", "分笔数据", "历史分钟", "十大股东"])
        self.search_btn= QtWidgets.QPushButton(self.splitter_1)
        self.search_btn.setObjectName("SearchButton")
        self.gridLayout.addWidget(self.splitter_1, 4, 0, 1, 2)
        self.stocks_tree = QtWidgets.QTreeWidget(self.centralwidget)
        self.stocks_tree.setObjectName("Stocks")
        self.stocks_tree.headerItem().setText(0, "Stocks")
        self.gridLayout.addWidget(self.stocks_tree, 5, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 80, 12))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.webView = QWebEngineView(self.centralwidget)
        self.webView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setMinimumSize(QtCore.QSize(200, 200))
        self.webView.setMaximumSize(QtCore.QSize(800, 16777215))
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 2, 9, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QToolBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 90, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.addToolBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.weibo_id_label.setText(_translate("MainWindow", "Weibo ID"))
        self.start_date_label.setText(_translate("MainWindow", "Start Date"))
        self.end_date_label.setText(_translate("MainWindow", "End Date"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.comboBox.setItemText(0, _translate("MainWindow", "D", "by date"))
        self.comboBox.setItemText(1, _translate("MainWindow", "W", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "M", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "5", None))
        self.comboBox.setItemText(4, _translate("MainWindow", "15", None))
        self.comboBox.setItemText(5, _translate("MainWindow", "30", None))
        self.comboBox.setItemText(6, _translate("MainWindow", "60", None))


