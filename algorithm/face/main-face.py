import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


image = cv2.imread('face.jpg')

with mp_face_detection.FaceDetection(
    min_detection_confidence=0.5) as face_detection:
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    for detection in results.detections:
        mp_drawing.draw_detection(image, detection)

    cv2.imwrite('mp-face.jpg', image)
