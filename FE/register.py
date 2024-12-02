from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RegisterDialog(object):
    def setupUi(self, RegisterDialog):
        RegisterDialog.setObjectName("RegisterDialog")
        RegisterDialog.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(RegisterDialog)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.centralwidget.setStyleSheet("background-color: white;")
        self.centralwidget.setObjectName("centralwidget")

        self.rightPanel = QtWidgets.QWidget(self.centralwidget)
        self.rightPanel.setGeometry(QtCore.QRect(200, 50, 400, 520))
        self.rightPanel.setStyleSheet("background-color: white;")
        self.rightPanel.setObjectName("rightPanel")

        self.titleLabel = QtWidgets.QLabel(self.rightPanel)
        self.titleLabel.setGeometry(QtCore.QRect(50, 10, 300, 50))
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 25px; font-weight: bold; color: #333333;")
        self.titleLabel.setText("Đăng ký tài khoản mới")
        self.titleLabel.setObjectName("titleLabel")

        # Trường First Name (Họ)
        self.firstNameLabel = QtWidgets.QLabel(self.rightPanel)
        self.firstNameLabel.setGeometry(QtCore.QRect(50, 70, 140, 20))
        self.firstNameLabel.setText("Họ")
        self.firstNameLabel.setStyleSheet("font-size: 14px; color: #333333;")

        self.firstNameInput = QtWidgets.QLineEdit(self.rightPanel)
        self.firstNameInput.setGeometry(QtCore.QRect(50, 90, 140, 35))
        self.firstNameInput.setStyleSheet("background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.firstNameInput.setObjectName("firstNameInput")

        # Trường Last Name (Tên)
        self.lastNameLabel = QtWidgets.QLabel(self.rightPanel)
        self.lastNameLabel.setGeometry(QtCore.QRect(210, 70, 140, 20))
        self.lastNameLabel.setText("Tên")
        self.lastNameLabel.setStyleSheet("font-size: 14px; color: #333333;")

        self.lastNameInput = QtWidgets.QLineEdit(self.rightPanel)
        self.lastNameInput.setGeometry(QtCore.QRect(210, 90, 140, 35))
        self.lastNameInput.setStyleSheet("background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.lastNameInput.setObjectName("lastNameInput")

        # Trường Username (Tên người dùng)
        self.usernameLabel = QtWidgets.QLabel(self.rightPanel)
        self.usernameLabel.setGeometry(QtCore.QRect(50, 130, 300, 20))
        self.usernameLabel.setText("Tên người dùng")
        self.usernameLabel.setStyleSheet("font-size: 14px; color: #333333;")

        self.registerUsernameInput = QtWidgets.QLineEdit(self.rightPanel)
        self.registerUsernameInput.setGeometry(QtCore.QRect(50, 150, 300, 35))
        self.registerUsernameInput.setStyleSheet(
            "background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.registerUsernameInput.setObjectName("registerUsernameInput")

        # Trường Email
        self.emailLabel = QtWidgets.QLabel(self.rightPanel)
        self.emailLabel.setGeometry(QtCore.QRect(50, 190, 300, 20))
        self.emailLabel.setText("Email")
        self.emailLabel.setStyleSheet("font-size: 14px; color: #333333;")

        self.emailInput = QtWidgets.QLineEdit(self.rightPanel)
        self.emailInput.setGeometry(QtCore.QRect(50, 210, 300, 35))
        self.emailInput.setStyleSheet("background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.emailInput.setObjectName("emailInput")

        # Trường Password
        self.passwordLabel = QtWidgets.QLabel(self.rightPanel)
        self.passwordLabel.setGeometry(QtCore.QRect(50, 250, 300, 20))
        self.passwordLabel.setText("Mật khẩu")
        self.passwordLabel.setStyleSheet("font-size: 14px; color: #333333;")

        self.registerPasswordInput = QtWidgets.QLineEdit(self.rightPanel)
        self.registerPasswordInput.setGeometry(QtCore.QRect(50, 270, 300, 35))
        self.registerPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registerPasswordInput.setStyleSheet(
            "background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.registerPasswordInput.setObjectName("registerPasswordInput")

        # Trường Confirm Password
        self.confirmPasswordLabel = QtWidgets.QLabel(self.rightPanel)
        self.confirmPasswordLabel.setGeometry(QtCore.QRect(50, 310, 300, 20))
        self.confirmPasswordLabel.setText("Xác nhận mật khẩu")
        self.confirmPasswordLabel.setStyleSheet("font-size: 14px; color: #333333;")

        self.confirmPasswordInput = QtWidgets.QLineEdit(self.rightPanel)
        self.confirmPasswordInput.setGeometry(QtCore.QRect(50, 330, 300, 35))
        self.confirmPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordInput.setStyleSheet(
            "background-color: #F5F5F5; border: 2px solid #B0B0B0; border-radius: 5px;")
        self.confirmPasswordInput.setObjectName("confirmPasswordInput")

        # Nút Đăng ký
        self.registerConfirmButton = QtWidgets.QPushButton(self.rightPanel)
        self.registerConfirmButton.setGeometry(QtCore.QRect(50, 390, 300, 45))
        self.registerConfirmButton.setStyleSheet(
            "background-color: #5DADE2; color: white; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px;")
        self.registerConfirmButton.setText("Đăng ký")
        self.registerConfirmButton.setObjectName("registerConfirmButton")

        # Liên kết đăng nhập
        self.alreadyHaveAccountLabel = QtWidgets.QLabel(self.rightPanel)
        self.alreadyHaveAccountLabel.setGeometry(QtCore.QRect(50, 450, 300, 25))
        self.alreadyHaveAccountLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.alreadyHaveAccountLabel.setText(
            '<html><head/><body><p><span style="font-size:14px; color:#000000;">Bạn đã có tài khoản? </span><a href="#"><span style="font-size:14px; color:#007BFF; text-decoration: underline;">Đăng nhập</span></a></p></body></html>')
        self.alreadyHaveAccountLabel.setObjectName("alreadyHaveAccountLabel")

        self.retranslateUi(RegisterDialog)
        QtCore.QMetaObject.connectSlotsByName(RegisterDialog)

    def retranslateUi(self, RegisterDialog):
        _translate = QtCore.QCoreApplication.translate
        RegisterDialog.setWindowTitle(_translate("RegisterDialog", "Đăng ký tài khoản"))
