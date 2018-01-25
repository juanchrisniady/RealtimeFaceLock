import face_recognition
import cv2
import sys
from PIL import ImageGrab
import pythoncom, pyHook

def disable(event):
    return False

def lockAll(hm,my_face_encoding,video_capture):
    count = 0
    hm.MouseAll = disable
    hm.KeyAll = disable
    hm.HookMouse()
    hm.HookKeyboard()
    while count < 3:
        isMe = False
        ret, frame = video_capture.read()
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = smaller_frame[:, :, ::-1]
        curr_face_locations = face_recognition.face_locations(rgb)
        curr_faces = face_recognition.face_encodings(rgb, curr_face_locations)    
        for face in curr_faces:
            results = face_recognition.compare_faces([my_face_encoding], face, 0.9)
            if results[0] == True:
                isMe = True
        if isMe:
            count+=1
        else:
            count = 0
        pythoncom.PumpWaitingMessages()
    hm.UnhookKeyboard()
    hm.UnhookMouse()
    print("unlock")
hm = pyHook.HookManager()
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
my_picture = face_recognition.load_image_file("faces/juan2.JPG")
my_face_encoding = face_recognition.face_encodings(my_picture)[0]
video_capture = cv2.VideoCapture(0)
count = 0
while True:
    isMe = False
    ret, frame = video_capture.read()
    smaller_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = smaller_frame[:, :, ::-1]
    curr_face_locations = face_recognition.face_locations(rgb)
    curr_faces = face_recognition.face_encodings(rgb, curr_face_locations)
    
    for face in curr_faces:
        results = face_recognition.compare_faces([my_face_encoding], face)
        if results[0] == True:
            isMe = True
    if isMe:
        count = 0
    else:
        count+=1
    if count == 20:
        print("lock")
        lockAll(hm,my_face_encoding,video_capture)
        count = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


