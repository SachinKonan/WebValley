import cv2

url = 'http://192.168.205.226:8080/stream.mjpg'

cap = cv2.VideoCapture(url)

while True:
    ret, img = cap.read()
    cv2.imshow('Frame', img)
    if cv2.waitKey(1) and ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
