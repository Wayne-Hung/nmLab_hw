import time
import cv2
import multiprocessing as mp

def producer(queue):
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
            # print('producer')
            ret, frame = cap.read()
            if not ret:
                break
            # if queue.full():
            #     print('loss')
            queue.put(frame)
            # print(time.strftime('%X'), frame.shape)
    except KeyboardInterrupt as e:
        cap.release()
        
def consumer(queue):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (1920, 1080))
    try:
        while True:
            if not queue.empty():
            # print('consumer')
                f = queue.get()
                out.write(f)
    except KeyboardInterrupt as e:
        # cap.release()
        pass

queue = mp.Queue(maxsize=10)

p1 = mp.Process(target=producer, args=(queue, ))
p2 = mp.Process(target=consumer, args=(queue, ))

p1.start()
p2.start()
p1.join()
p2.join()
