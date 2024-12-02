from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Ui_CameraWindow(object):
    def setupUi(self, CameraWindow):
        CameraWindow.setObjectName("CameraWindow")
        CameraWindow.resize(800, 600)
        CameraWindow.setStyleSheet("background-color: white;")

        self.centralwidget = QtWidgets.QWidget(CameraWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.webview = QWebEngineView(self.centralwidget)
        self.webview.setGeometry(QtCore.QRect(0, 50, 800, 430))  # Đặt vị trí và kích thước của QWebEngineView
        self.webview.setVisible(False)  # Không hiển thị QWebEngineView khi khởi động


        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(170, 500, 150, 40))
        self.startButton.setObjectName("startButton")
        self.startButton.setStyleSheet("background-color: #5DADE2; color: white;")

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(330, 500, 150, 40))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setStyleSheet("background-color: #5DADE2; color: white;")

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(490, 500, 150, 40))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setStyleSheet("background-color: #5DADE2; color: white;")

        CameraWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CameraWindow)
        QtCore.QMetaObject.connectSlotsByName(CameraWindow)

        self.camera = None
        self.timer = QtCore.QTimer()

        self.startButton.clicked.connect(self.start_camera)
        self.stopButton.clicked.connect(self.stop_camera)
        self.exitButton.clicked.connect(self.exit_camera)

    def retranslateUi(self, CameraWindow):
        _translate = QtCore.QCoreApplication.translate
        CameraWindow.setWindowTitle(_translate("CameraWindow", "Camera"))
        self.startButton.setText(_translate("CameraWindow", "Start Camera"))
        self.stopButton.setText(_translate("CameraWindow", "Stop Camera"))
        self.exitButton.setText(_translate("CameraWindow", "Exit"))



