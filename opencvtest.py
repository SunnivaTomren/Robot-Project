import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Klarte ikke å åpne kamera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Klarte ikke å lese fra kamera.")
        break

    cv2.imshow("Kamerafeed", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows() 
