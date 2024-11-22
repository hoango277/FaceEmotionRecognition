import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from register import Ui_RegisterDialog
from login import Ui_MainWindow
from camera import Ui_CameraWindow
import requests
import cv2
import numpy as np
from keras.models import load_model
from PyQt5.QtGui import QImage, QPixmap

# Sử dụng CPU thay vì GPU để tránh các lỗi liên quan đến GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class RegisterApp(QtWidgets.QDialog, Ui_RegisterDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.registerConfirmButton.clicked.connect(self.register_user)

        # Kết nối nút "Đăng nhập" với hàm mở giao diện đăng nhập
        self.alreadyHaveAccountButton.clicked.connect(self.open_login_window)

    def register_user(self):
        url = 'http://127.0.0.1:8000/register'
        data = {
            "username": self.registerUsernameInput.text(),
            "password": self.registerPasswordInput.text(),
            "email": self.emailInput.text()
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                message = response.json().get('message', 'Đăng ký thành công!')
                self.show_popup("Thông báo", message)
                self.open_login_window()  # Mở giao diện đăng nhập sau khi đăng ký thành công
            else:
                self.show_popup("Thông báo", "Đăng ký thất bại, vui lòng thử lại.")
        except requests.exceptions.RequestException as e:
            self.show_popup("Thông báo", f"Đã xảy ra lỗi: {e}")

    def show_popup(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def open_login_window(self):
        # Tạo một cửa sổ mới cho Đăng nhập
        self.login_window = LoginApp()
        self.login_window.show()
        # Ẩn cửa sổ đăng ký
        self.close()


class LoginApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login_user)

    def login_user(self):
        url = 'http://127.0.0.1:8000/login'
        data = {
            "username": self.usernameInput.text(),
            "password": self.passwordInput.text()
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                message = response.json().get("message")
                if message == "Login successful":
                    #self.show_popup("Thông báo", "Đăng nhập thành công!")
                    self.open_camera_window()  # Mở giao diện camera sau khi đăng nhập thành công
                else:
                    self.show_popup("Thông báo", "Đăng nhập thất bại: " + message)
            else:
                self.show_popup("Thông báo", "Có lỗi xảy ra!")
        except requests.exceptions.RequestException as e:
            self.show_popup("Thông báo", f"Đã xảy ra lỗi: {e}")

    def show_popup(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def open_camera_window(self):
        # Tạo một cửa sổ mới cho Camera
        self.camera_window = QMainWindow()
        self.ui = Ui_CameraWindow()
        self.ui.setupUi(self.camera_window)
        self.camera_window.show()
        # Ẩn cửa sổ đăng nhập
        self.hide()

        # Khởi động camera và nhận diện cảm xúc
        self.ui.startButton.clicked.connect(self.start_emotion_detection)
        self.ui.stopButton.clicked.connect(self.ui.stop_camera)
        self.ui.exitButton.clicked.connect(self.exit_camera_window)

    def start_emotion_detection(self):
        try:
            # Load model và các thành phần cần thiết
            model = load_model('final_emotion_model.h5')
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

            self.ui.camera = cv2.VideoCapture(0)
            if not self.ui.camera.isOpened():
                print("Cannot open camera")
                return

            self.ui.timer = QtCore.QTimer()
            self.ui.timer.timeout.connect(lambda: self.update_emotion_frame(model, face_cascade, emotion_labels))
            self.ui.timer.start(30)
            self.ui.startButton.setEnabled(False)
            self.ui.stopButton.setEnabled(True)

        except Exception as e:
            self.show_popup("Thông báo", f"Đã xảy ra lỗi khi khởi động nhận diện cảm xúc: {e}")

    def update_emotion_frame(self, model, face_cascade, emotion_labels):
        try:
            ret, frame = self.ui.camera.read()
            if not ret:
                return

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                roi_gray = roi_gray.astype('float32') / 255
                roi_gray = np.expand_dims(roi_gray, axis=0)
                roi_gray = np.expand_dims(roi_gray, axis=-1)

                predictions = model.predict(roi_gray)
                max_index = int(np.argmax(predictions))
                emotion = emotion_labels[max_index]

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.ui.cameraDisplayLabel.setPixmap(QPixmap.fromImage(qt_image))

        except Exception as e:
            self.show_popup("Thông báo", f"Đã xảy ra lỗi khi xử lý khung hình: {e}")

    def exit_camera_window(self):
        # Đóng cửa sổ camera và quay lại cửa sổ đăng nhập
        if self.ui.camera is not None:
            self.ui.timer.stop()
            self.ui.camera.release()
            self.ui.camera = None
        self.camera_window.close()
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    register_dialog = RegisterApp()
    register_dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
