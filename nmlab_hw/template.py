import cv2
import multiprocessing as mp

def gstreamer_camera(queue):
    # Use the provided pipeline to construct the video capture in opencv
    pipeline = (
        "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)1920, height=(int)1080, "
            "format=(string)NV12, framerate=(fraction)30/1 ! "
        "queue ! "
        "nvvidconv flip-method=2 ! "
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

    # Complete the function body
    pass


def gstreamer_rtmpstream(queue):
    # Use the provided pipeline to construct the video writer in opencv
    pipeline = (
        "appsrc ! "
            "video/x-raw, format=(string)BGR ! "
        "queue ! "
        "videoconvert ! "
            "video/x-raw, format=RGBA ! "
        "nvvidconv ! "
        "nvv4l2h264enc bitrate=8000000 ! "
        "h264parse ! "
        "flvmux ! "
        'rtmpsink location="rtmp://localhost/rtmp/live live=1"'
    )

    out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 30.0, (1920, 1080))
    try:
        while True:
            if not queue.empty():
                # print('consumer')
                f = queue.get()
                f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                f = cv2.cvtColor(f, cv2.COLOR_GRAY2BGR)
                out.write(f)
    except KeyboardInterrupt as e:
        # cap.release()
        pass
   

    # Complete the function body
    
    # You can apply some simple computer vision algorithm here
    pass


queue = mp.Queue(maxsize=10)

p1 = mp.Process(target=gstreamer_camera, args=(queue, ))
p2 = mp.Process(target=gstreamer_rtmpstream, args=(queue, ))

p1.start()
p2.start()
p1.join()
p2.join()

# Complelte the code
