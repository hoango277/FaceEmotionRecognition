from PyQt5 import QtCore, QtGui, QtWidgets

class ForgotPasswordDialog(object):
    def setupUi(self, ForgotPasswordDialog):
        ForgotPasswordDialog.setObjectName("ForgotPasswordDialog")
        ForgotPasswordDialog.resize(400, 300)  # Điều chỉnh kích thước của dialog

        self.centralwidget = QtWidgets.QWidget(ForgotPasswordDialog)
        self.centralwidget.setObjectName("centralwidget")

        # Tạo QLabel cho tiêu đề
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(50, 30, 300, 50))
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("font-size: 25px; font-weight: bold;")

        # Trường nhập email
        self.emailInput = QtWidgets.QLineEdit(self.centralwidget)
        self.emailInput.setGeometry(QtCore.QRect(50, 100, 300, 45))
        self.emailInput.setObjectName("emailInput")
        self.emailInput.setStyleSheet("border: 1px solid gray; padding: 5px; border-radius: 5px;")

        # Nút "Tiếp tục"
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(50, 160, 300, 45))
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setStyleSheet("""
            background-color: #1E3A8A;  /* Màu xanh đậm */
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
        """)
        
        # Thêm QLabel cho dòng chữ "Quay lại" (chuyển lại từ QLabel)
        self.backLabel = QtWidgets.QLabel(self.centralwidget)  # Dùng QLabel thay vì QPushButton
        self.backLabel.setGeometry(QtCore.QRect(50, 210, 300, 30))  # Vị trí dưới nút "Tiếp tục"
        self.backLabel.setAlignment(QtCore.Qt.AlignCenter)  # Căn giữa
        self.backLabel.setObjectName("backLabel")
        self.backLabel.setStyleSheet("font-size: 14px; color: #007BFF; font-weight: bold; text-decoration: underline;")
        self.backLabel.setText("Quay lại")

        # Đặt layout cho dialog
        ForgotPasswordDialog.setCentralWidget(self.centralwidget)
        self.retranslateUi(ForgotPasswordDialog)
        QtCore.QMetaObject.connectSlotsByName(ForgotPasswordDialog)

    def retranslateUi(self, ForgotPasswordDialog):
        _translate = QtCore.QCoreApplication.translate
        ForgotPasswordDialog.setWindowTitle(_translate("ForgotPasswordDialog", "Quên mật khẩu"))
        self.titleLabel.setText(_translate("ForgotPasswordDialog", "Quên mật khẩu"))
        self.emailInput.setPlaceholderText(_translate("ForgotPasswordDialog", "Email"))
        self.confirmButton.setText(_translate("ForgotPasswordDialog", "Tiếp tục"))

