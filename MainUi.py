#-*- coding:utf-8 -*-
from __future__ import print_function
import os, sys, sip, time
from datetime import datetime,timedelta
from qtpy.QtWidgets import QTreeWidgetItem, QMenu, QApplication, QAction, QMainWindow, QMessageBox
from qtpy import QtGui, QtWidgets
from qtpy.QtCore import Qt, QUrl, QDate
from qtpy.QtGui import QStandardItemModel
from WeiboData.Gui.Graph import stock_render_page
from WeiboData.Gui.Layout import Ui_Main_Window
from WeiboData.Core.Dispatcher import Dispatcher
import pymysql
from Config import DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME, DB_CHARSET, STOCK_SEARCH_BY_WEIBOID
from pandas import DataFrame as df
import pandas as pd
import tushare as ts
import re
try:
    import cPickle
except ImportError:
    import _pickle as cPickle# import json
list1 = []


class MyUi(QMainWindow):
    def __init__(self):
        super(MyUi, self).__init__()
        self.ui = Ui_Main_Window()
        self.connection = None
        self.ui.setup_ui(self)
        self._init_db()
        self.ui.stocks_tree.clear()
        self.ui.search_btn.clicked.connect(lambda: self.search_weibo())
        self.ui.stocks_tree.itemClicked.connect(self.onItemClick)
        current_date = time.strftime("%Y/%m/%d")
        date_obj = datetime.strptime(current_date, "%Y/%m/%d")
        past = date_obj - timedelta(days = 7)
        past_time = datetime.strftime(past, "%Y/%m/%d")
        QPast = QDate.fromString(past_time,"yyyy/MM/dd")
        Qcurdate = QDate.fromString(current_date,"yyyy/MM/dd")
        self.ui.start_date_edit.setDate(QPast)
        self.ui.end_date_edit.setDate(Qcurdate)
        self.ui.start_date_edit.setCalendarPopup(True)
        self.ui.end_date_edit.setCalendarPopup(True)

    def _init_db(self):
        self.connection = pymysql.connect(host=DB_HOST,
        port=DB_PORT, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, charset=DB_CHARSET)

    def search_weibo(self):
        self.ui.stocks_tree.clear()
        weibo_id = self.ui.search_edit_text.text()
        start_date = self.ui.start_date_edit.date()
        start_date = start_date.toPyDate()
        start_date = start_date.strftime("%Y/%m/%d")
        start_date = time.mktime(time.strptime(start_date, "%Y/%m/%d"))
        end_date = self.ui.end_date_edit.date()
        end_date = end_date.toPyDate()
        end_date = end_date.strftime("%Y/%m/%d")
        end_date = time.mktime(time.strptime(end_date, "%Y/%m/%d"))

        if weibo_id:
            dispatcher = Dispatcher(uid=weibo_id, start_date=start_date,
                                    end_date=end_date, filter_flag=True,
                                    update_cookies=False)
            dispatcher.execute()
        else:
            print('please input weibo uid here.')

        self.ui.stocks_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.stocks_tree.customContextMenuRequested.connect(self.openWidgetMenu)

        stock_id_list = list()
        stock_comments_list = list()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(STOCK_SEARCH_BY_WEIBOID, [weibo_id])
                search_results = cursor.fetchall()
                if len(search_results) > 0:

                    for row in search_results:
                        print(row[3], row[4], row[5])
                        stock_id = row[3]
                        stock_comments = row[4] + "" + row[5]
                        stock_id_list.append(stock_id)
                        stock_comments_list.append(stock_comments)
        finally:
            self.connection.close()
        parent = QTreeWidgetItem(self.ui.stocks_tree)
        parent.setText(0, "搜索结果")
        for i in range(len(stock_id_list)):
            child = QTreeWidgetItem(parent)
            child.setText(0, stock_id_list[i] + "-" + stock_comments_list[i])
        self.ui.stocks_tree.expandToDepth(0)


    def onItemClick(self):
        text = self.ui.stocks_tree.currentItem().text(0)
        stock_id_pattern = re.compile("(s[h|z]\d{6})-.*")
        stock_id = stock_id_pattern.search(text)
        QMessageBox.information(self, "股票提示", text)
        width = self.ui.webView.width()
        height = self.ui.webView.height()
        start_date = self.ui.start_date_edit.date()
        start_date = start_date.toPyDate()
        start_date = start_date.strftime("%Y/%m/%d")
        end_date = self.ui.end_date_edit.date()
        end_date = end_date.toPyDate()
        end_date = end_date.strftime("%Y/%m/%d")
        stock_render_page(stock_id.group(1), start_date, end_date, 15, width, height)#labels:复权ork线or分笔 option:hfq, qfq or 15, 30, D, etc
        self.ui.webView.reload()#refreshes webengine
        self.ui.webView.repaint()
        self.ui.webView.update()

    def openWidgetMenu(self,position):
        indexes = self.ui.stocks_tree.selectedIndexes()
        item = self.ui.stocks_tree.itemAt(position)
        if item == None:
            return
        if len(indexes) > 0:
            menu = QMenu()
            menu.addAction(QAction("Delete", menu, checkable = True))
            #menu.triggered.connect(self.eraseItem)
            item = self.ui.stocks_tree.itemAt(position)
            # collec = str(item.text())
            # print(collec)
            menu.triggered.connect(lambda action: self.ListMethodSelected(action, item))
            menu.exec_(self.ui.stocks_tree.viewport().mapToGlobal(position))
            # self.ui.stocks_tree.itemClicked.connect(self.onItemClick(item))

    def ListMethodSelected(self, action, item):
        if action.text() == "Delete":
            self.eraseItem()
        if action.text() == "Combine":
            global CombineKeyword
            collec = str(item.text())
            CombineKeyword.append(collec)#Useless function(maybe?)
            list1 = [self.tr(collec)]
            self.ui.listwidget.addItems(list1)
            self.eraseItem()


    def methodSelected(self, action, collec):
        #print(action.text()) #Choice
        #if (self.ui.treewidget.count() == 5):
         #   self.ui.label.setText("Maximum number of queries")
         #   return
        #self.ui.label.setText("")
        Choice = action.text()
        Stock = collec
        #print(collec)  #Stock Name
        #print(db_origin)  #DataBase name
        #list1 = [self.tr(Stock+"-"+Choice+"-"+db_origin)]
        #self.ui.treewidget.addItems(list1)
        # parent = QTreeWidgetItem(self.ui.treeWidget_2)
        # parent.setText(0, Stock.decode("utf-8")+"-"+Choice)
        # font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        # self.ui.treeWidget_2.setFont(font)

    def eraseItem(self):
        # for x in self.ui.treeWidget_2.selectedItems():#delete with write click menu
        #     #item = self.ui.treewidget.takeItem(self.ui.treewidget.currentRow())
        #     sip.delete(x)
            #item.delete
        pass

    def openMenu(self,position):
        indexes = self.ui.treeWidget.selectedIndexes()
        item = self.ui.treeWidget.itemAt(position)


        db_origin = ""
        #if item.parent():
         #   db_origin = item.parent().text(0)
        collec = str(item.text(0).encode("utf-8"))
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level = level + 1
            menu = QMenu()
            #print((collec, db_origin))
            # if level ==0:
            #     pass
            # else:
            #     keyarray = GetKeys(collec, db_origin)
            #     if "Open" in keyarray:
            #     if self.ui.combobox.currentText()==u"K线":
            #         menu.addAction(QAction("Kline", menu, checkable=True))
            #         menu.addAction(QAction("Open", menu, checkable=True))
            #         menu.addAction(QAction("Close", menu, checkable=True))#open up different menu with different kind of graphs
            #         menu.addAction(QAction("High", menu, checkable=True))
            #         menu.addAction(QAction("Low", menu, checkable=True))
            #         menu.addAction(QAction("Volume", menu, checkable=True))
            #         #menu.addAction(QAction("P_change", menu, checkable=True))
            #         #menu.addAction(QAction("Turnover",menu,checkable=True))
            #     if self.ui.combobox.currentText()==u"复权":
            #         menu.addAction(QAction("Kline", menu, checkable=True))
            #         menu.addAction(QAction("Open", menu, checkable=True))
            #         menu.addAction(QAction("Close", menu, checkable=True))
            #         menu.addAction(QAction("High", menu, checkable=True))
            #         menu.addAction(QAction("Low", menu, checkable=True))
            #         menu.addAction(QAction("Volume", menu, checkable=True))
            #         menu.addAction(QAction("Amount", menu, checkable=True))
            #     if self.ui.combobox.currentText()==u"分笔数据":
            #         menu.addAction(QAction("分笔", menu, checkable=True))
            #     if self.ui.combobox.currentText()==u"历史分钟":
            #         menu.addAction(QAction("Kline", menu, checkable=True))
            #         menu.addAction(QAction("Open", menu, checkable=True))
            #         menu.addAction(QAction("Close", menu, checkable=True))
            #         menu.addAction(QAction("High", menu, checkable=True))
            #         menu.addAction(QAction("Low", menu, checkable=True))
            #         menu.addAction(QAction("Volume", menu, checkable=True))
            #         menu.addAction(QAction("Amount", menu, checkable=True))
            #     if self.ui.combobox.currentText()==u"十大股东":
            #         menu.addAction(QAction("季度饼图", menu, checkable=True))
            #         #menu.addAction(QAction("持股比例", menu, checkable=True))
            #     for g in keyarray:
            #         menu.addAction(QAction(g, menu, checkable=True))
        menu.triggered.connect(lambda action: self.methodSelected(action, collec))
        menu.exec_(self.ui.treeWidget.viewport().mapToGlobal(position))

app = QApplication(sys.argv)
w = MyUi()
w.show()
sys.exit(app.exec_())
