import os 
import main
import open_camera

attendance_path =main.file_path_csv()

print(attendance_path)

main.import_attendance_csv(attendance_path)
main.delete_after_78am()