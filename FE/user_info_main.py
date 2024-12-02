import sys
import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication

def get_token_from_file():
    """ Đọc token từ file token.json """
    try:
        with open('token.json', 'r') as f:
            data = json.load(f)
            return data.get('access_token')
    except FileNotFoundError:
        print("File token.json không tồn tại!")
        return None

def get_user_info(token):
    """ Lấy thông tin người dùng từ API với token """
    url = "http://127.0.0.1:8000/api/users"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Gửi yêu cầu GET đến API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

class Ui_UserInfoWindow(QtWidgets.QMainWindow):
    def setupUi(self, user_info):
        self.setObjectName("UserInfoWindow")  # Use self (the current window) for object name
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)  # Use self instead of UserInfoWindow
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #ECF0F1;")

        # QTableWidget setup
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(20, 20, 760, 400))
        self.table.setRowCount(4)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Thông tin", "Nội Dung"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #FFFFFF;
            border: 1px solid #BDC3C7;
            border-radius: 5px;
        """)

        # Set values into table from user_info
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("Username"))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(user_info["username"]))
        self.table.setItem(1, 0, QtWidgets.QTableWidgetItem("Email"))
        self.table.setItem(1, 1, QtWidgets.QTableWidgetItem(user_info["email"]))
        self.table.setItem(2, 0, QtWidgets.QTableWidgetItem("Họ"))
        self.table.setItem(2, 1, QtWidgets.QTableWidgetItem(user_info["first_name"]))
        self.table.setItem(3, 0, QtWidgets.QTableWidgetItem("Tên"))
        self.table.setItem(3, 1, QtWidgets.QTableWidgetItem(user_info["last_name"]))

        for row in range(4):
            for col in range(2):  # Adjust columns as needed
                item = self.table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

        # Buttons setup with modern look and rounded corners, all with same color
        button_color = "#3498DB"  # Blue color for all buttons

        self.change_password_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_password_button.setGeometry(QtCore.QRect(70, 450, 200, 50))
        self.change_password_button.setStyleSheet(f"""
            background-color: {button_color};
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 25px;
            padding: 10px;
        """)
        self.change_password_button.setText("Đổi mật khẩu")

        self.change_info_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_info_button.setGeometry(QtCore.QRect(310, 450, 200, 50))
        self.change_info_button.setStyleSheet(f"""
            background-color: {button_color};
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 25px;
            padding: 10px;
        """)
        self.change_info_button.setText("Thay đổi thông tin")

        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(550, 450, 200, 50))
        self.back_button.setStyleSheet(f"""
            background-color: {button_color};
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 25px;
            padding: 10px;
        """)
        self.back_button.setText("Quay lại trang chủ")

        # Kết nối nút "Đổi mật khẩu" để mở cửa sổ đổi mật khẩu
        self.change_password_button.clicked.connect(self.open_change_password_window)
        self.back_button.clicked.connect(self.open_home_page)
        self.change_info_button.clicked.connect(self.open_change_user_info)

        self.setCentralWidget(self.centralwidget)

    def open_change_password_window(self):
        try:
            from change_password import Ui_ChangePasswordWindow
            self.changePasswordWindow = Ui_ChangePasswordWindow(self)
            self.changePasswordWindow.setupUi()
            self.changePasswordWindow.show()
            self.hide()
        except Exception as e:
            print(e)

    def open_home_page(self):
        try:
            from home_main import HomeWindow
            self.homeWindow = HomeWindow()
            self.homeWindow.show()
            self.hide()
        except Exception as e:
            print(e)

    def open_change_user_info(self):
        try:
            from change_user_info import Ui_EditUserInfoWindow
            self.userInfoWindows = Ui_EditUserInfoWindow(self)
            self.userInfoWindows.setupUi()
            self.userInfoWindows.show()
            self.hide()
        except Exception as e:
            print(e)



def main():
    # Lấy token từ file token.json
    token = get_token_from_file()
    if not token:
        print("Không có token để sử dụng!")
        return

    # Gửi yêu cầu để lấy thông tin người dùng
    user_info = get_user_info(token)
    if user_info:
        # Khởi tạo ứng dụng PyQt và giao diện người dùng
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = Ui_UserInfoWindow()  # Create instance of the window directly
        MainWindow.setupUi(user_info)  # Pass user_info to setupUi
        MainWindow.show()
        sys.exit(app.exec_())
    else:
        print("Không thể lấy thông tin người dùng.")

if __name__ == "__main__":
    main()
