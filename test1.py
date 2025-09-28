import cv2
import face_recognition
import dlib
import numpy as np
import os
from datetime import datetime, date
import threading
import pandas as pd

# ==============================
# Load Models (make sure files exist!)
# ==============================
predictor_path = "models/shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "models/dlib_face_recognition_resnet_model_v1.dat"

if not os.path.exists(predictor_path) or not os.path.exists(face_rec_model_path):
    raise RuntimeError("❌ Missing model files in 'models/' folder. Please download .dat files.")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
encoder = dlib.face_recognition_model_v1(face_rec_model_path)

# ==============================
# Load Known Faces
# ==============================
known_face_encodings = []
known_face_names = []

known_faces_dir = "known_faces"
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)

for filename in os.listdir(known_faces_dir):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(path)
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)
        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])
            print(f"✅ Loaded {filename}")
        else:
            print(f"⚠️ No face found in {filename}")

# ==============================
# Attendance Setup
# ==============================
attendance_file = "attendance.csv"
registered_today = set()   # track names registered today
today_date = date.today().strftime("%Y-%m-%d")

# Load previous attendance to preserve history
if os.path.exists(attendance_file):
    df_existing = pd.read_csv(attendance_file)
    # Ensure today’s already registered names are tracked
    registered_today = set(zip(df_existing["Name"], df_existing["Date"]))
else:
    df_existing = pd.DataFrame(columns=["Name", "Date", "Time"])

# ==============================
# Process Frames Function
# ==============================
def process_frames():
    cap = cv2.VideoCapture(0)
    new_records = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        locations = face_recognition.face_locations(rgb_small)
        encodings = face_recognition.face_encodings(rgb_small, locations)

        for encoding, face_location in zip(encodings, locations):
            matches = face_recognition.compare_faces(known_face_encodings, encoding, tolerance=0.6)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # ✅ Register only once per day
                if (name, today_date) not in registered_today:
                    now = datetime.now().strftime("%H:%M:%S")
                    new_records.append([name, today_date, now])
                    registered_today.add((name, today_date))
                    print(f"📌 {name} registered on {today_date} at {now}")

            # Draw rectangle around face
            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save Attendance to Single CSV
    if new_records:
        df_new = pd.DataFrame(new_records, columns=["Name", "Date", "Time"])
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_csv(attendance_file, index=False)
        print(f"✅ Attendance updated in {attendance_file}")
    else:
        print("ℹ️ No new attendance today.")

# ==============================
# Start Processing in Thread
# ==============================
t = threading.Thread(target=process_frames)
t.start()
