import cv2
from cvzone.FaceDetectionModule import FaceDetector

cap = cv2.VideoCapture(0)
detector = FaceDetector()

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame, bboxs = detector.findFaces(frame)

    if bboxs:
        center = bboxs[0]["center"]
        score = bboxs[0]["score"]
        print(score)
    cv2.imshow("FACE", frame)

    if cv2.waitKeyEx(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()