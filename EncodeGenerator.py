# 3 step -- Encoding Generator

import cv2
import face_recognition
import pickle
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-2e0d3-default-rtdb.firebaseio.com/"
})

#for importing the student images

folderPath = 'Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentids = []
for path in PathList:
    if path.endswith(('.jpg', '.jpeg', '.png')):
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        studentids.append(os.path.splitext(path)[0])

    # print(path)
    # print(os.path.splitext(path)[0])         #for splitting the name of image to consider only the id
print(studentids)


def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

# for recognizing which encoding belongs to which image

print("Encoding started...")
encodeListKnown = findEncoding(imgList)
encodeListKnownWithIds = [encodeListKnown, studentids]
print(encodeListKnownWithIds)
print("Encoding Complete")

#Saving this as a pickle file after extracting all encodings

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File Saved...")