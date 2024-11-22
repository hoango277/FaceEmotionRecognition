from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewPasswordDialog(object):
    def setupUi(self, NewPasswordDialog):
        NewPasswordDialog.setObjectName("NewPasswordDialog")
        NewPasswordDialog.resize(400, 300)

        self.centralwidget = QtWidgets.QWidget(NewPasswordDialog)
        self.centralwidget.setObjectName("centralwidget")

        self.newPasswordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.newPasswordInput.setGeometry(QtCore.QRect(50, 50, 300, 40))
        self.newPasswordInput.setObjectName("newPasswordInput")
        self.newPasswordInput.setPlaceholderText("Mật khẩu mới")
        self.newPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPasswordInput.setStyleSheet("border: 1px solid gray; padding: 5px; border-radius: 5px;")

        self.confirmPasswordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.confirmPasswordInput.setGeometry(QtCore.QRect(50, 110, 300, 40))
        self.confirmPasswordInput.setObjectName("confirmPasswordInput")
        self.confirmPasswordInput.setPlaceholderText("Xác nhận mật khẩu")
        self.confirmPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordInput.setStyleSheet("border: 1px solid gray; padding: 5px; border-radius: 5px;")

        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(50, 180, 300, 40))
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setText("Xác nhận")
        self.confirmButton.setStyleSheet("background-color: #5DADE2; color: white; font-size: 16px; font-weight: bold; border-radius: 5px;")

        NewPasswordDialog.setCentralWidget(self.centralwidget)
        self.retranslateUi(NewPasswordDialog)
        QtCore.QMetaObject.connectSlotsByName(NewPasswordDialog)

    def retranslateUi(self, NewPasswordDialog):
        _translate = QtCore.QCoreApplication.translate
        NewPasswordDialog.setWindowTitle(_translate("NewPasswordDialog", "Đặt mật khẩu mới"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewPasswordDialog = QtWidgets.QMainWindow()
    ui = Ui_NewPasswordDialog()
    ui.setupUi(NewPasswordDialog)
    NewPasswordDialog.show()
    sys.exit(app.exec_())
