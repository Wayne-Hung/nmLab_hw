import time
import cv2

pipeline = (
    "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)1920, height=(int)1080, "
        "format=(string)NV12, framerate=(fraction)30/1 ! "
    "queue ! "
    "nvvidconv ! "
        "video/x-raw, "
        "width=(int)1920, height=(int)1080, "
        "format=(string)BGRx, framerate=(fraction)30/1 ! "
    "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
    "appsink"
)

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        print(time.strftime('%X'), frame.shape)
except KeyboardInterrupt as e:
    cap.release()
