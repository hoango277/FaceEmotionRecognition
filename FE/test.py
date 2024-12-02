import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class VideoStreamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Khởi tạo giao diện
        self.init_ui()

        # URL FastAPI Streaming video
        self.stream_url = 'http://127.0.0.1:8000/api/stream'  # URL của bạn

        # Tải trang web với video stream
        self.webview.setUrl(QUrl(self.stream_url))

    def init_ui(self):
        self.setWindowTitle('Video Stream with QWebEngine')

        # Khởi tạo QWebEngineView
        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)

        # Điều chỉnh kích thước cửa sổ
        self.setGeometry(100, 100, 800, 600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoStreamApp()
    sys.exit(app.exec_())
