import threading
from queue import Queue
import cv2

video_threads = []
video_queues = []
streaming = False

def video_stream(camera_index=0, queue=None):
    cap = cv2.VideoCapture(camera_index)  # Mở camera
    if not cap.isOpened():
        raise RuntimeError(f"Không thể mở camera tại chỉ mục {camera_index}")

    while streaming:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc khung hình từ camera. Dừng stream.")
            break
        # Mã hóa khung hình thành định dạng JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Đưa dữ liệu vào hàng đợi
        if queue:
            queue.put(frame_bytes)

    cap.release()  # Giải phóng camera

def video_generator(queue):
    while streaming:
        if not queue.empty():
            frame_bytes = queue.get()
            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
def start_threads(camera_index=0, num_streams=1):
    global streaming, video_threads, video_queues
    streaming = True
    for _ in range(num_streams):
        queue = Queue(maxsize=10)
        thread = threading.Thread(target=video_stream, args=(camera_index, queue))
        thread.daemon = True
        video_threads.append(thread)
        video_queues.append(queue)
        thread.start()
def stop_threads():
    global streaming, video_threads, video_queues
    streaming = False
    for thread in video_threads:
        thread.join()
    video_threads.clear()
    video_queues.clear()

def get_video_generator(index=0):
    if index < len(video_queues):
        return video_generator(video_queues[index])
    else:
        raise IndexError(f"Không có stream nào ở chỉ mục {index}.")
