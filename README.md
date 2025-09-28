# Automated_Attendance_System

An attendance management system using face recognition with OpenCV and Python.  
This system detects faces using a deep learning model and marks attendance automatically.

---

## Features

- Real-time face detection using OpenCV's DNN face detector.
- Face recognition with `face_recognition` library.
- Attendance recorded and saved in a CSV file.
- Supports multiple students with known face encodings.
- Yearly attendance tracking in MySQL database.
- Easily extensible with new faces/models.

---

## Folder Structure
Automated_Attendance_System/
│
├── models/ # Contains face detection model files
│ ├── res10_300x300_ssd_iter_140000_fp16.caffemodel
│ └── deploy.prototxt
│
├── known_faces/ # Images of students for recognition
│
├── attendance.csv # CSV file storing attendance logs
│
├── app.py # Main application script
├── daily_core_job.py # Scheduled attendance job
├── README.md # This file


---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/Automated_Attendance_System.git
   cd Automated_Attendance_System
2. Requirements
   pip install opencv-pytho
   pip install face_recognition
   pip install numpy
   pip install pandas
   pip install mysql-connector-python
   pip install https://github.com/omwaman1/dlib_wheel_for_python/releases/download/dlib-python3.13.5/dlib-20.0.0-cp313-cp313-win_amd64.whl
