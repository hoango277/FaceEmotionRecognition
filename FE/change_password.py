import json
import requests  # Đảm bảo rằng requests đã được import

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChangePasswordWindow(QtWidgets.QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.user_info_window = user_info
    def setupUi(self):
        self.setObjectName("ChangePasswordWindow")
        self.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #ECF0F1;")

        # Tạo các trường nhập liệu
        self.old_password_label = QtWidgets.QLabel("Mật khẩu cũ:", self.centralwidget)
        self.old_password_label.setGeometry(QtCore.QRect(50, 40, 120, 30))
        self.old_password_label.setStyleSheet("font-size: 14px; color: #34495E;")

        self.old_password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.old_password_input.setGeometry(QtCore.QRect(180, 40, 200, 30))
        self.old_password_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #BDC3C7;
        """)
        self.old_password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.new_password_label = QtWidgets.QLabel("Mật khẩu mới:", self.centralwidget)
        self.new_password_label.setGeometry(QtCore.QRect(50, 100, 120, 30))
        self.new_password_label.setStyleSheet("font-size: 14px; color: #34495E;")

        self.new_password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.new_password_input.setGeometry(QtCore.QRect(180, 100, 200, 30))
        self.new_password_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #BDC3C7;
        """)
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        # Nút Xác nhận
        self.confirm_button = QtWidgets.QPushButton("Xác nhận", self.centralwidget)
        self.confirm_button.setGeometry(QtCore.QRect(50, 180, 150, 40))
        self.confirm_button.setStyleSheet("""
            background-color: #3498DB;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 20px;
            padding: 10px;
        """)

        # Nút Hủy
        self.cancel_button = QtWidgets.QPushButton("Hủy", self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(230, 180, 150, 40))
        self.cancel_button.setStyleSheet("""
            background-color: #E74C3C;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 20px;
            padding: 10px;
        """)

        # Kết nối các nút với hành động
        self.confirm_button.clicked.connect(self.change_password)
        self.cancel_button.clicked.connect(self.cancel)

        self.setCentralWidget(self.centralwidget)

    def cancel(self):
        """ Hàm khi nhấn nút 'Hủy' quay lại cửa sổ chính """
        try:
            self.user_info_window.show()  # Hiển thị lại cửa sổ UserInfoWindow
            self.close()  # Đóng cửa sổ thay đổi mật khẩu
        except Exception as e:
            print(e)

    def get_token_from_file(self):
        """ Đọc token từ file token.json """
        try:
            with open('token.json', 'r') as f:
                data = json.load(f)
                return data.get('access_token')
        except FileNotFoundError:
            print("File token.json không tồn tại!")
            return None

    def change_password(self):
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()

        # Kiểm tra nếu mật khẩu cũ và mới không trống
        if not old_password or not new_password:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Gửi yêu cầu để đổi mật khẩu qua API
        url = "http://127.0.0.1:8000/api/users/password"
        data = {
            "old_password": old_password,
            "new_password": new_password,
        }
        token = self.get_token_from_file()

        if not token:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Không có token để xác thực!")
            return

        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Gửi yêu cầu PUT đến API
        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            QtWidgets.QMessageBox.information(None, "Thành công", "Đổi mật khẩu thành công!")
            self.user_info_window.show()  # Quay lại cửa sổ UserInfoWindow sau khi đổi mật khẩu thành công
            self.close()  # Đóng cửa sổ thay đổi mật khẩu
        else:
            QtWidgets.QMessageBox.warning(None, "Lỗi", f"Không thể đổi mật khẩu: {response.text}")

    def run(self):
        """ Hàm chạy ứng dụng """
        app = QtWidgets.QApplication([])
        ChangePasswordWindow = QtWidgets.QMainWindow()
        ui = Ui_ChangePasswordWindow(self.user_info_window)  # Truyền đối tượng `UserInfoWindow`
        ui.setupUi(ChangePasswordWindow)
        ChangePasswordWindow.show()
        app.exec_()



