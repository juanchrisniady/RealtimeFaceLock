import face_recognition
import cv2
import sys
from PIL import ImageGrab
import pythoncom, pyHook

def disable(event):
    return False
def getKeyFace():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Get Key Face", frame)
        k = cv2.waitKey(1)
        if k%256 == 32:
            smaller_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb = smaller_frame[:, :, ::-1]
            curr_face_locations = face_recognition.face_locations(rgb)
            my_face_encoding = face_recognition.face_encodings(rgb, curr_face_locations)[0]
            video_capture.release()
            cv2.destroyAllWindows()
            return my_face_encoding
    

def lockAll(hm,my_face_encoding,video_capture):
    hm.MouseAll = disable
    hm.KeyAll = disable
    hm.HookMouse()
    hm.HookKeyboard()
    isMe = False
    while isMe == False:      
        ret, frame = video_capture.read()
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = smaller_frame[:, :, ::-1]
        curr_face_locations = face_recognition.face_locations(rgb)
        curr_faces = face_recognition.face_encodings(rgb, curr_face_locations)    
        for face in curr_faces:
            results = face_recognition.compare_faces([my_face_encoding], face, 0.4)
            if results[0] == True:
                isMe = True
        pythoncom.PumpWaitingMessages()
    hm.UnhookKeyboard()
    hm.UnhookMouse()
    print("unlock")

hm = pyHook.HookManager()
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
my_face_encoding = getKeyFace()
video_capture = cv2.VideoCapture(0)
def main():
    count = 0
    while True:
        isMe = False
        ret, frame = video_capture.read()
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = smaller_frame[:, :, ::-1]
        curr_face_locations = face_recognition.face_locations(rgb)
        curr_faces = face_recognition.face_encodings(rgb, curr_face_locations)
        
        for face in curr_faces:
            results = face_recognition.compare_faces([my_face_encoding], face,0.4)
            #print(face_recognition.face_distance([my_face_encoding], face))
            if results[0] == True:
                isMe = True
        if isMe:
            count = 0
            #print(count)
        else:
            count+=1
            #print(count)
        if count == 10:
            print("lock")
            lockAll(hm,my_face_encoding,video_capture)
            count = 0

    video_capture.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()


