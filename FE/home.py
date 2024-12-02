from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HomeWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Trang chủ")
        MainWindow.resize(724, 602)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-image: url('images/background.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        self.logoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.logoutButton.setGeometry(QtCore.QRect(632, 550, 91, 31))
        self.logoutButton.setObjectName("logoutButton")
        self.logoutButton.setStyleSheet("background-color: #1E90FF; color: white; font-weight: bold;")

        self.editInfoButton = QtWidgets.QPushButton(self.centralwidget)
        self.editInfoButton.setGeometry(QtCore.QRect(180, 250, 351, 50))
        self.editInfoButton.setObjectName("editInfoButton")
        self.editInfoButton.setStyleSheet("background-color: #1E90FF; color: white; font-weight: bold;")

        self.emotionRecognitionButton = QtWidgets.QPushButton(self.centralwidget)
        self.emotionRecognitionButton.setGeometry(QtCore.QRect(180, 340, 351, 50))
        self.emotionRecognitionButton.setObjectName("emotionRecognitionButton")
        self.emotionRecognitionButton.setStyleSheet("background-color: #1E90FF; color: white; font-weight: bold;")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 80, 381, 50))
        self.label.setObjectName("label")
        self.label.setStyleSheet("font-size: 24pt; font-weight: bold; color: white;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trang chủ"))

        # Cập nhật lại tên nút
        self.logoutButton.setText(_translate("MainWindow", "Đăng xuất"))
        self.editInfoButton.setText(_translate("MainWindow", "Thông tin tài khoản"))
        self.emotionRecognitionButton.setText(_translate("MainWindow", "Nhận diện cảm xúc"))
        self.label.setText(_translate("MainWindow", "Trang chủ"))


class MainWindow(QtWidgets.QMainWindow, Ui_HomeWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
