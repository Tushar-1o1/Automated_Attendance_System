import cv2
import face_recognition
import numpy as np
import os
import pandas as pd

# ===== Paths =====
model_path = r"E:\Automated_Attendance_System\models\res10_300x300_ssd_iter_140000_fp16.caffemodel"
config_path = r"E:\Automated_Attendance_System\models\deploy.prototxt"
known_faces_dir = r"E:\Automated_Attendance_System\known_faces"
attendance_file = r"E:\Automated_Attendance_System\attendance.csv"

# ===== Load Face Detector =====
net = cv2.dnn.readNetFromCaffe(config_path, model_path)

# ===== Load Known Encodings =====
known_face_encodings = []
known_face_ids = []

for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            enrollment_id = os.path.splitext(filename)[0]  # remove extension
            known_face_ids.append(enrollment_id)
            print(f"✅ Loaded {enrollment_id}")
        else:
            print(f"⚠️ No face found in {filename}")

# ===== Track already marked attendance =====
if os.path.exists(attendance_file):
    df_existing = pd.read_csv(attendance_file)
    registered_today = set(df_existing["Enrollment_No"].tolist())
else:
    df_existing = pd.DataFrame(columns=["Enrollment_No"])
    registered_today = set()

# ===== Detect faces with OpenCV DNN =====
def detect_faces_dnn(frame):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    boxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            # Clamp coordinates
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            boxes.append((x1, y1, x2, y2))
    return boxes

# ===== Start Camera =====
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

new_records = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = detect_faces_dnn(frame)

    for (x1, y1, x2, y2) in face_locations:
        # Convert bounding box to face_recognition format: (top, right, bottom, left)
        face_location = (y1, x2, y2, x1)

        encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=[face_location])

        enrollment_number = "Unknown"
        if encodings:
            matches = face_recognition.compare_faces(known_face_encodings, encodings[0], tolerance=0.5)
            distances = face_recognition.face_distance(known_face_encodings, encodings[0])

            if True in matches:
                best_match_index = np.argmin(distances)
                enrollment_number = known_face_ids[best_match_index]

                if enrollment_number not in registered_today:
                    print(f"📌 Marked {enrollment_number} present")
                    if [enrollment_number] not in new_records:
                        new_records.append([enrollment_number])
                    registered_today.add(enrollment_number)

            # Draw rectangle and enrollment number
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, enrollment_number, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Recognition Attendance", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ===== Save Attendance =====
if new_records:
    df_new = pd.DataFrame(new_records, columns=["Enrollment_No"])
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.drop_duplicates(subset=["Enrollment_No"], inplace=True)  # Just in case duplicates sneaked in
    df_final.to_csv(attendance_file, index=False)
    print(f"✅ Attendance saved to {attendance_file}")
else:
    print("ℹ️ No new attendance recorded.")
