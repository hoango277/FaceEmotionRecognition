import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from login_main import LoginWindow
from home import Ui_HomeWindow
from user_info_main import get_token_from_file, get_user_info
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication



class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.cameraWindow = None
        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self)

        self.ui.logoutButton.clicked.connect(self.handle_logout)
        self.ui.editInfoButton.clicked.connect(self.show_user_window)
        self.ui.emotionRecognitionButton.clicked.connect(self.show_camera_window)

    def handle_logout(self):
        try:
            with open("token.json", "w") as token_file:
                json.dump({}, token_file)
        except Exception as e:
            print(f"Không thể xóa token: {str(e)}")

        self.show_login_window()

    def show_login_window(self):
        self.loginWindow = LoginWindow()
        self.loginWindow.show()

        self.hide()

    def show_user_window(self):
        from user_info_main import Ui_UserInfoWindow

        # Lấy token và thông tin người dùng
        token = get_token_from_file()
        if not token:
            print("Không có token để sử dụng!")
            return

        user_info = get_user_info(token)
        if user_info:
            try:
                self.userWindow = Ui_UserInfoWindow()
                self.userWindow.setupUi(user_info=user_info)
                self.userWindow.show()
                self.hide()
            except Exception as e:
                print(e)

    def show_camera_window(self):
        from camera_main import CameraWindow
        self.cameraWindow = CameraWindow()
        self.cameraWindow.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())
