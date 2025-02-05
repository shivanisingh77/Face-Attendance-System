
import os
import pickle

# Code for running a webcam
import cv2
import cvzone
import face_recognition
import firebase_admin
import numpy as np
from PIL.ImageChops import offset
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-2e0d3-default-rtdb.firebaseio.com/"
})

cap = cv2.VideoCapture(0)               #1 as we gonna use multiple cameras
cap.set(3,640)             #width
cap.set(4,480)             #height

#for importing the background image

imgBackground = cv2.imread('Resources/background.jpg')

# importing the mode images into a list

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

#print(len(imgModeList))

# load the encoding file

print("Loading Encoded File..")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentids = encodeListKnownWithIds
print(studentids)
print("Encoded File Loaded...")


modeType = 3
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)     #reducing the size of the image
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)                              #coverting the bgr into rgb (mandatory)


    faceCurFrame = face_recognition.face_locations((imgS))                    #taking the locations of the faces
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)      # encoding the webcam image


    imgBackground[162:162 + 480, 55:55 + 640] = img              #for combining webcam and background image
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]        #for combining the various modes into interface


    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    #       print("matches", matches)
    #       print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            print("Match Index", matchIndex)

            if matches[matchIndex]:
    #            print("Known Face Detected")
    #            print(studentids[matchIndex])
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1              #bbox(bounding box) information
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)     #rt= rectangle thickness

                id = studentids[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                #get the image
                image_path = f'Images/{id}.jpg'
                if os.path.exists(image_path):
                    imgStudent = cv2.imread(image_path, cv2.IMREAD_COLOR)

                # Update data of attendance

                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondElapsed)
                if secondElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 0
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 0:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['Standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w,h), _=cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414 - w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175: 175+216, 909: 909+216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 3
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 3
        counter = 0

    # cv2.imshow("Webcam", img)                             #for the webcam
    cv2.imshow("Face Attendance", imgBackground)   #for the background
    cv2.waitKey(1)