from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap

class Ui_CameraWindow(object):
    def setupUi(self, CameraWindow):
        CameraWindow.setObjectName("CameraWindow")
        CameraWindow.resize(800, 600)
        CameraWindow.setStyleSheet("background-color: white;")

        self.centralwidget = QtWidgets.QWidget(CameraWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.cameraDisplayLabel = QtWidgets.QLabel(self.centralwidget)
        self.cameraDisplayLabel.setGeometry(QtCore.QRect(0, 50, 800, 430))
        self.cameraDisplayLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.cameraDisplayLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.cameraDisplayLabel.setObjectName("cameraDisplayLabel")
        self.cameraDisplayLabel.setStyleSheet("background-color: #D3D3D3;")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(170, 500, 150, 40))
        self.startButton.setObjectName("startButton")
        self.startButton.setStyleSheet("background-color: #5DADE2; color: white;")

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(330, 500, 150, 40))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setStyleSheet("background-color: #FF6347; color: white;")

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(490, 500, 150, 40))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setStyleSheet("background-color: #808080; color: white;")

        CameraWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CameraWindow)
        QtCore.QMetaObject.connectSlotsByName(CameraWindow)

        self.camera = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.startButton.clicked.connect(self.start_camera)
        self.stopButton.clicked.connect(self.stop_camera)
        self.exitButton.clicked.connect(self.exit_camera)

    def retranslateUi(self, CameraWindow):
        _translate = QtCore.QCoreApplication.translate
        CameraWindow.setWindowTitle(_translate("CameraWindow", "Camera"))
        self.startButton.setText(_translate("CameraWindow", "Start Camera"))
        self.stopButton.setText(_translate("CameraWindow", "Stop Camera"))
        self.exitButton.setText(_translate("CameraWindow", "Exit"))

    def start_camera(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("Cannot open camera")
                self.camera = None
            else:
                self.timer.start(30)
        else:
            self.timer.start(30)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stop_camera(self):
        if self.camera is not None:
            self.timer.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def exit_camera(self):
        if self.camera is not None:
            self.timer.stop()
            self.camera.release()
            self.camera = None
        self.cameraDisplayLabel.clear()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.cameraDisplayLabel.setPixmap(QPixmap.fromImage(qt_image))
