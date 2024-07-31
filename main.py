import threading
import cv2
# То, что будет в следующих комментах будут моими догадками о том, как можно сделать multi-recognizer, а не только одно фото.
# Прошу строго не судить ツ

from deepface import DeepFace
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
counter = 0
face_match = False # массив рамзером sizeof(reference_img) и все они фолсы
reference_img = cv2.imread("reference.jpg") #крч тут как то надо [] и внутри брекетов циклом прочитать каждую пикчу в бдшке

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame,reference_img.copy())['verified']: #а тут циклом от i = 0..n и reference_img[i].copy()
            face_match = True #face_match[i] = true
        else: face_match = False
    except ValueError:
        face_match = False

while True:
    ret,frame = cap.read()
    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face,args =( frame.copy(),)).start()
            except ValueError:
                 pass
        counter +=1
        if face_match == True:
            cv2.putText(frame,"MATCH!",(20,450),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),10)
        else:
            cv2.putText(frame,"NO MATCH!",(20,450),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),10)
        cv2.imshow("test",frame)
    key = cv2.waitKey(1)
    if (key == ord("q")):
        break
cv2.destroyAllWindows()
