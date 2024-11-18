# app/services/video_service.py

import threading
from queue import Queue
import cv2
from app.services.camera_thread import CameraThread

video_threads = []
video_queues = []
streaming = False

# Hàm đọc và truyền video
def video_stream(camera_index=0, queue=None):
    """Hàm đọc khung hình từ camera và đẩy vào hàng đợi."""
    cap = CameraThread.open_camera(camera_index)
    while streaming:
        frame = CameraThread.capture_frame(cap)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        if queue:
            queue.put(frame_bytes)
    CameraThread.release_camera(cap)

# Hàm lấy dữ liệu từ queue để phát
def video_generator(queue):
    """Hàm phát video dưới dạng streaming, sử dụng queue."""
    while streaming:
        if not queue.empty():
            frame_bytes = queue.get()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

# Khởi chạy các thread cho video streaming
def start_threads(camera_index=0, num_streams=1):
    """Khởi tạo các thread để chạy song song việc đọc camera."""
    global streaming, video_threads, video_queues
    streaming = True
    for _ in range(num_streams):
        queue = Queue(maxsize=10)  # Hàng đợi lưu trữ các khung hình
        thread = threading.Thread(target=video_stream, args=(camera_index, queue))
        thread.daemon = True  # Đảm bảo thread dừng khi ứng dụng kết thúc
        video_threads.append(thread)
        video_queues.append(queue)
        thread.start()

# Dừng các thread và giải phóng tài nguyên
def stop_threads():
    """Dừng tất cả các thread liên quan đến video streaming."""
    global streaming, video_threads, video_queues
    streaming = False
    for thread in video_threads:
        thread.join()
    video_threads.clear()
    video_queues.clear()

# Lấy generator cho một stream cụ thể
def get_video_generator(index=0):
    """Trả về generator cho một stream từ hàng đợi cụ thể."""
    if index < len(video_queues):
        return video_generator(video_queues[index])
    else:
        raise IndexError(f"Không có stream nào ở chỉ mục {index}.")
