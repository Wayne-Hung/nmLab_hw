import cv2
import mediapipe as mp

mp_object_detection = mp.solutions.object_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
image = cv2.imread('object.jpg')

with mp_object_detection.ObjectDetection(
    min_detection_confidence=0.1) as object_detection:

    results = object_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

    cv2.imwrite('mp-object.jpg', image)
