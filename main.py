# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime, date, timedelta
import requests
import calendar
import re


class Ui_MainWindow(object):

    yesmorrow: int = 0  # 내일이면 +1, 어제면 -1
    weekday_list = [" (월)", " (화)", " (수)", " (목)", " (금)", " (토)", " (일)"]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 599)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 131, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(810, 20, 131, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 130, 291, 421))
        self.groupBox.setObjectName("groupBox")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 271, 381))
        self.listWidget.setObjectName("listWidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(340, 130, 291, 421))
        self.groupBox_2.setObjectName("groupBox_2")
        self.listWidget_2 = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 30, 271, 381))
        self.listWidget_2.setObjectName("listWidget_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(660, 130, 291, 421))
        self.groupBox_3.setObjectName("groupBox_3")
        self.listWidget_3 = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidget_3.setGeometry(QtCore.QRect(10, 30, 271, 381))
        self.listWidget_3.setObjectName("listWidget_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 20, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 970, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.set_day_yesterday)
        self.pushButton_2.clicked.connect(self.set_day_tomorrow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "밥먹자"))
        self.pushButton.setText(_translate("MainWindow", "어제 급식"))
        self.pushButton_2.setText(_translate("MainWindow", "내일 급식"))
        self.groupBox.setTitle(_translate("MainWindow", "조식"))
        self.groupBox_2.setTitle(_translate("MainWindow", "중식"))
        self.groupBox_3.setTitle(_translate("MainWindow", "석식"))
        self.label.setText(_translate("MainWindow", "날짜"))
        self.set_date()
        self.set_meal()

    def set_day_yesterday(self):
        self.yesmorrow -= 1
        self.set_date()
        self.set_meal()

    def set_day_tomorrow(self):
        self.yesmorrow += 1
        self.set_date()
        self.set_meal()

    def get_date(self):
        return str(datetime.now() + timedelta(days=self.yesmorrow))[:10]

    def set_date(self):
        date = self.get_date()
        year, month, day = self.get_ymd(date)
        weekday = self.weekday_list[calendar.weekday(year, month, day)]
        self.label.setText(date + weekday)

    def set_meal(self):
        list_widgets = [self.listWidget, self.listWidget_2, self.listWidget_3]
        date = self.get_date().replace("-", "")
        for i in range(1, 4):
            url = "https://open.neis.go.kr/hub/mealServiceDietInfo?"  # 기본 URL
            url += "ATPT_OFCDC_SC_CODE=F10&"  # 교육청코드
            url += "SD_SCHUL_CODE=7380292&"  # 학교코드
            url += "MMEAL_SC_CODE=" + str(i) + "&"  # 1, 2, 3 : 아침, 점심, 저녁
            url += "MLSV_YMD=" + date  # 날짜

            response = requests.get(url).text
            soup = bs(response, "lxml")

            list_widgets[i - 1].clear()

            if soup.find("code").get_text() == "INFO-000":  # 급식 데이터가 있을 때

                for linebreak in soup.find_all("br"):
                    linebreak.replace_with("\n")
                result = soup.find("ddish_nm").get_text()
                result = re.sub("[/>\]]+", "", result)

                list_widgets[i - 1].addItems(result.split("\n"))

            else:  # 급식 데이터가 없을 때

                list_widgets[i - 1].addItem("데이터 없음")

    def get_ymd(self, date):
        return int(date[:4]), int(date[5:7]), int(date[8:])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
