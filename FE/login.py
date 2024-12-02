from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Các thành phần giao diện
        self.leftPanel = QtWidgets.QLabel(self.centralwidget)
        self.leftPanel.setGeometry(QtCore.QRect(0, 0, 320, 600))
        self.leftPanel.setStyleSheet("background-color: white;")
        self.leftPanel.setObjectName("leftPanel")

        self.aiImage = QtWidgets.QLabel(self.leftPanel)
        self.aiImage.setGeometry(QtCore.QRect(10, 50, 300, 500))
        self.aiImage.setStyleSheet("""
            background-image: url('images/AI.png');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
        """)
        self.aiImage.setObjectName("aiImage")

        self.rightPanel = QtWidgets.QWidget(self.centralwidget)
        self.rightPanel.setGeometry(QtCore.QRect(320, 0, 480, 600))
        self.rightPanel.setStyleSheet("background-color: white;")
        self.rightPanel.setObjectName("rightPanel")

        self.logoPanel = QtWidgets.QLabel(self.rightPanel)
        self.logoPanel.setGeometry(QtCore.QRect(0, 0, 480, 180))
        self.logoPanel.setStyleSheet("background-color: white;")
        self.logoPanel.setObjectName("logoPanel")

        self.logoImage = QtWidgets.QLabel(self.logoPanel)
        self.logoImage.setGeometry(QtCore.QRect(90, 10, 300, 150))
        self.logoImage.setStyleSheet("""
            background-image: url('images/logo.png');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
        """)
        self.logoImage.setObjectName("logoImage")

        self.buttonPanel = QtWidgets.QWidget(self.rightPanel)
        self.buttonPanel.setGeometry(QtCore.QRect(0, 180, 480, 420))
        self.buttonPanel.setObjectName("buttonPanel")

        self.usernameInput = QtWidgets.QLineEdit(self.buttonPanel)
        self.usernameInput.setGeometry(QtCore.QRect(60, 20, 360, 40))
        self.usernameInput.setStyleSheet("background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.usernameInput.setObjectName("usernameInput")

        self.passwordInput = QtWidgets.QLineEdit(self.buttonPanel)
        self.passwordInput.setGeometry(QtCore.QRect(60, 80, 360, 40))
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setStyleSheet("background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.passwordInput.setObjectName("passwordInput")

        self.loginButton = QtWidgets.QPushButton(self.buttonPanel)
        self.loginButton.setGeometry(QtCore.QRect(60, 140, 360, 45))
        self.loginButton.setStyleSheet("background-color: #5DADE2; color: white; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px;")
        self.loginButton.setObjectName("loginButton")
        self.loginButton.setText("Đăng nhập")

        self.forgotPasswordLabel = QtWidgets.QLabel(self.buttonPanel)
        self.forgotPasswordLabel.setGeometry(QtCore.QRect(60, 200, 360, 20))
        self.forgotPasswordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.forgotPasswordLabel.setText("Quên mật khẩu?")
        self.forgotPasswordLabel.setStyleSheet("font-size: 14px; color: #007BFF; font-weight: bold;")
        self.forgotPasswordLabel.setObjectName("forgotPasswordLabel")

        self.registerButton = QtWidgets.QPushButton(self.buttonPanel)
        self.registerButton.setGeometry(QtCore.QRect(60, 230, 360, 45))
        self.registerButton.setStyleSheet("background-color: #A9A9A9; color: black; font-size: 16px; border: 2px solid #696969; border-radius: 5px;")
        self.registerButton.setObjectName("registerButton")
        self.registerButton.setText("Đăng ký tài khoản mới")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Đăng nhập"))
        self.usernameInput.setPlaceholderText(_translate("MainWindow", "Tên người dùng"))
        self.passwordInput.setPlaceholderText(_translate("MainWindow", "Mật khẩu"))
        self.loginButton.setText(_translate("MainWindow", "Đăng nhập"))
        self.forgotPasswordLabel.setText(_translate("MainWindow", "Quên mật khẩu?"))
        self.registerButton.setText(_translate("MainWindow", "Đăng ký tài khoản mới"))
