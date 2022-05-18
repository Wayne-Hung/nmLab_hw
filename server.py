import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import fib_pb2
import fib_pb2_grpc

import cv2
import argparse
import multiprocessing as mp


import mediapipe

mp_hands = mediapipe.solutions.hands
mp_drawing_styles = mediapipe.solutions.drawing_styles

mp_face_detection = mediapipe.solutions.face_detection

mp_object_detection = mediapipe.solutions.object_detection

mp_drawing = mediapipe.solutions.drawing_utils


# return or pass by reference?
def face(image):
    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    return results

def drawFace(image, results):
    if results.detections != None:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
    
    # return image

def hand(image):
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    return results

    # return image

def drawHand(image, results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())


def object_detect(image):
    with mp_object_detection.ObjectDetection(
        min_detection_confidence=0.1) as object_detection:

        results = object_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    return results

    # return image

def drawObject(image, results):
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)



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

def gstreamer_rtmpstream(queue, mode):
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
        results = lambda: None
        results.detections = None
        results.multi_hand_landmarks = None
        interval = 7
        t = 0
        while True:
            if not queue.empty():
                # print('consumer')
                f = queue.get()
                if t % interval == 0:
                    if mode.value == 1:
                        results = face(f)
                        results.multi_hand_landmarks = None
                    elif mode.value == 2:
                        results = hand(f)
                        results.detections = None
                    elif mode.value == 3:
                        results = object_detect(f)
                        results.multi_hand_landmarks = None
                t = t + 1

                # if mode.value != 0:
                #     print("mode is", mode.value)

                if mode.value == 1:
                    drawFace(f, results)
                elif mode.value == 2:
                    drawHand(f, results)
                elif mode.value == 3:
                    drawObject(f, results)
                    
                out.write(f)
    except KeyboardInterrupt as e:
        # cap.release()
        pass
   

    # Complete the function body
    
    # You can apply some simple computer vision algorithm here
    pass

class StreamServer(fib_pb2_grpc.FibCalculatorServicer):

    def __init__(self, mode):
        self.mode = mode
        pass

    def Compute(self, request, context):
        value = request.order

        response = fib_pb2.FibResponse()
        response.value = value

        if value in [0, 1, 2, 3]:
            print("Change mode")
            self.mode.value= int(value)

        return response

def gRPCServer(args, mode):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = StreamServer(mode)
    fib_pb2_grpc.add_FibCalculatorServicer_to_server(servicer, server)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8080, type=int)
    args = vars(parser.parse_args())

    queue = mp.Queue(maxsize=5)
    mode = mp.Value('i', 0)

    # for streaming
    p1 = mp.Process(target=gstreamer_camera, args=(queue, ))
    p2 = mp.Process(target=gstreamer_rtmpstream, args=(queue, mode))
    p3 = mp.Process(target=gRPCServer, args=(args, mode))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # for the gRPC server

