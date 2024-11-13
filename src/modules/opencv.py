import cv2

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print('Could not open video')

while True:
    ret, frame = capture.read()

    if not ret:
        print('Could not read the frame')

        break

    cv2.imshow('Webcam', frame)

    gray = cv2.cv2Color(frame, cv2.COLOR_BGR2GRAY)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break