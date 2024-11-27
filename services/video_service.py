from starlette.responses import StreamingResponse
from ultralytics import YOLO
import cv2 as cv
import threading
import queue
import time
import numpy as np
from tensorflow.keras.models import load_model

from exception import raise_error


class CameraThread(threading.Thread):
    def __init__(self, frame_queue, result_queue, frame_to_stream):
        threading.Thread.__init__(self)
        self.frame_queue = frame_queue
        self.result_queue = result_queue
        self.capture = cv.VideoCapture(0)
        self.running = True
        self.frame_count = 0
        self.current_boxes = []
        self.frame_to_stream = frame_to_stream

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                break
            frame = cv.flip(frame, 1)

            # Mỗi 3 khung hình, gửi khung hình để phát hiện
            if self.frame_count % 3 == 0:
                if self.frame_queue.empty():
                    self.frame_queue.put(frame.copy())

            # Lấy kết quả từ detection thread
            if not self.result_queue.empty():
                self.current_boxes = self.result_queue.get()

            # Vẽ bounding boxes và văn bản
            if self.current_boxes:
                for box in self.current_boxes:
                    x1, y1, x2, y2, conf, emotion_label, emotion_conf = box
                    # Vẽ bounding box
                    cv.rectangle(frame, (int(x1), int(y1)),
                                 (int(x2), int(y2)), (255, 0, 0), 2)

                    # Nhãn cảm xúc
                    emotion_text = f"{emotion_label} {emotion_conf:.2f}"
                    (e_text_width, e_text_height), e_baseline = cv.getTextSize(emotion_text, cv.FONT_HERSHEY_SIMPLEX,
                                                                               0.5, 1)
                    # Tính vị trí văn bản (trên bounding box)
                    text_x = int(x1)
                    text_y = int(y1) - 10
                    # Nếu văn bản ở đâù khung hình thì chuyển xuống dưới
                    if text_y - e_text_height - e_baseline < 0:
                        text_y = int(y2) + e_text_height + e_baseline + 10

                    # Vẽ nhãn cảm xúc
                    cv.rectangle(frame, (text_x, text_y - e_text_height - e_baseline),
                                 (text_x + e_text_width, text_y), (0, 255, 0), -1)
                    cv.putText(frame, emotion_text, (text_x, text_y - e_baseline),
                               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)

            self.frame_count += 1
            if not self.frame_to_stream.empty():
                self.frame_to_stream.get()
            self.frame_to_stream.put(frame)


    def stop(self):
        self.running = False
        if self.capture.isOpened():
            self.capture.release()
        cv.destroyAllWindows()


class DetectionThread(threading.Thread):
    def __init__(self, frame_queue, result_queue):
        threading.Thread.__init__(self)
        self.frame_queue = frame_queue
        self.result_queue = result_queue
        self.model = YOLO('resources/yolov8n-face.pt')
        self.emotion_model = load_model('resources/final_emotion_model.h5')
        self.emotion_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
        self.running = True

    def preprocess_face(self, face_img):
        # Chuyển đổi ảnh sang grayscale và resize về kích thước 48x48
        face_gray = cv.cvtColor(face_img, cv.COLOR_BGR2GRAY)
        face_resized = cv.resize(face_gray, (48, 48))
        face_normalized = face_resized / 255.0
        face_reshaped = np.expand_dims(face_normalized, axis=0)
        face_reshaped = np.expand_dims(face_reshaped, axis=-1)
        return face_reshaped
    def run(self):
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                results = self.model.predict(frame, conf=0.4)

                current_boxes = []
                for result in results:
                    for box in result.boxes:
                        # Lấy tọa độ bounding box
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        # Lấy lớp và độ tin cậy
                        cls_id = int(box.cls[0]) if box.cls is not None else -1
                        conf = box.conf[0].item() if box.conf is not None else 0.0

                        # Cắt khuôn mặt từ khung hình
                        face_img = frame[int(y1):int(y2), int(x1):int(x2)]
                        if face_img.size == 0:
                            continue  # Bỏ qua nếu không cắt được khuôn mặt
                        # Tiền xử lý và nhận diện cảm xúc
                        preprocessed_face = self.preprocess_face(face_img)
                        emotion_prediction = self.emotion_model.predict(preprocessed_face)
                        emotion_label = self.emotion_labels[np.argmax(emotion_prediction)]
                        emotion_conf = np.max(emotion_prediction)

                        # Lưu vào box
                        current_boxes.append((x1, y1, x2, y2, conf, emotion_label, emotion_conf))
                # Cập nhật result_queue
                while not self.result_queue.empty():
                    self.result_queue.get()
                self.result_queue.put(current_boxes)

            time.sleep(0.01)

    def stop(self):
        self.running = False


class VideoService:
    def __init__(self):
        self.frame_queue = queue.Queue(maxsize=1)
        self.result_queue = queue.Queue(maxsize=1)
        self.frame_to_stream = queue.Queue(maxsize=1)
        self.camera_thread = None
        self.detection_thread = None
        self.running = False

    def get_video(self, user):
        if user.get('user_role') != 'user':
            return raise_error(100008)
        self.camera_thread = CameraThread(self.frame_queue, self.result_queue, self.frame_to_stream)
        self.detection_thread = DetectionThread(self.frame_queue, self.result_queue)

        self.camera_thread.start()
        self.detection_thread.start()
        self.running = True

        def generate_video():
            while self.running:
                try:
                    frame = self.frame_to_stream.get(timeout=1)
                    _, buffer = cv.imencode('.png', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except queue.Empty:
                    print()

        return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace; boundary=frame")

    def stop_video(self, user):
        if user.get('user_role') != 'user':
            return raise_error(100008)
        if self.detection_thread:
            self.detection_thread.stop()
            self.detection_thread.join()
            self.detection_thread = None
        if self.running:
            if self.camera_thread:
                self.camera_thread.stop()
                self.camera_thread.join()
                self.camera_thread = None
        self.running = False



