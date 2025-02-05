# For adding the students data to firebase real time database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-2e0d3-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {
    "12354":
        {
            "name": "Elon Musk",
            "major": "Robotics",
            "starting_year": 2020,
            "total_attendance": 10,
            "Standing": "G",
            "Year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "12433":
        {
            "name": "Shivani Singh",
            "major": "Computer Sc.",
            "starting_year": 2021,
            "total_attendance": 50,
            "Standing": "G",
            "Year": 4,
            "last_attendance_time": "2024-12-11 00:54:34"
        },
    "12435":
        {
            "name": "Rashmika Mandanna",
            "major": "Robotics",
            "starting_year": 2000,
            "total_attendance": 10,
            "Standing": "G",
            "Year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "21345":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2018,
            "total_attendance": 12,
            "Standing": "B",
            "Year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "12400":
        {
            "name": "Ritik ",
            "major": "AIML",
            "starting_year": 2021,
            "total_attendance": 15,
            "Standing": "B",
            "Year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "12401":
        {
            "name": "Sania",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 20,
            "Standing": "M",
            "Year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "12402":
        {
            "name": "Sidharth",
            "major": "Civil",
            "starting_year": 2020,
            "total_attendance": 30,
            "Standing": "M",
            "Year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "12403":
        {
            "name": "Tom",
            "major": "Electrical",
            "starting_year": 2022,
            "total_attendance": 18,
            "Standing": "G",
            "Year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "12404":
        {
            "name": "Alice",
            "major": "Robotics",
            "starting_year": 2023,
            "total_attendance": 12,
            "Standing": "B",
            "Year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

}

for key,value in data.items():
    ref.child(key).set(value)