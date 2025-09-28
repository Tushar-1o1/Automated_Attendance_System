import database 
import datetime as dt,time
import os
import csv


flag,mycur,mydb,str_year=database.connect()

#get todaysdate
def tdate():
    date=dt.datetime.now().date()
    return date


#get current year
def year_newyear():
    year=dt.datetime.now().year
    return year


#file path of csv file
import os

def file_path_csv():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    attendance_path = os.path.join(script_dir, "attendance.csv")
    return attendance_path


#this is to add new colum every year on 31st march
def alter_Table(mydb,mycur):
    today = dt.date.today()
    if today.day == 31 and today.month == 3:
        try:
            year=year_newyear()
            new_year=year+1
            str_year = f"Year_{year}_{new_year}"
            str_year_next = f"Year_{year+1}_{new_year+1}"
            mycur.execute(f"ALTER TABLE YEARLY_ATTENDANCE DROP COLUMN `{str_year}`")
            mycur.execute(f"ALTER TABLE YEARLY_ATTENDANCE ADD COLUMN `{str_year_next}` INT DEFAULT 0")
            mydb.commit()
        except Exception as err:
            print(err)
    else:
        print("")


#add information to yearly attendance
def yearly_attendance(mycur, mydb, enrollment_number):
    try:
        year = year_newyear()
        new_year = year + 1
        str_year = f"Year_{year}_{new_year}"
        mycur.execute("SELECT Enrollment_No FROM STUDENT WHERE Enrollment_No = %s", (enrollment_number,))
        student_exists = mycur.fetchone()
        if not student_exists:
            print(f"Enrollment number {enrollment_number} does not exist in STUDENT table.")
            return
        mycur.execute(f"SELECT `{str_year}` FROM YEARLY_ATTENDANCE WHERE Enrollment_No = %s", (enrollment_number,))
        result = mycur.fetchone()
        if result is None:
            mycur.execute(
                f"INSERT INTO YEARLY_ATTENDANCE (Enrollment_No, `{str_year}`) VALUES (%s, %s)",
                (enrollment_number, 1)
            )
            print(f"Inserted new attendance record for {enrollment_number} with {str_year} = 1")
        else:
            current_count = result[0] if result[0] is not None else 0
            mycur.execute(
                f"UPDATE YEARLY_ATTENDANCE SET `{str_year}` = %s WHERE Enrollment_No = %s",
                (current_count + 1, enrollment_number)
            )
            print(f"Updated attendance for {enrollment_number}: {str_year} = {current_count + 1}")
        mydb.commit()
    except Exception as e:
        print(f"Error updating yearly attendance: {e}")



#this is to mark attendance
def mark_attendance(enrollment_number):
    try:
        alter_Table(mydb, mycur)  # If you want to keep yearly column update
        date = tdate()
        status = 'present'
        mycur.execute(
            "INSERT INTO ATTENDANCE (Enrollment_No, Date, Status) VALUES (%s, %s, %s)",
            (enrollment_number, date, status)
        )
        mydb.commit()
        yearly_attendance(mycur,mydb,enrollment_number)
        return True
    except Exception as e:
        print(f"Error marking attendance: {e}")
        return False


#to read csv file data and feed it to mark_attendance function
def import_attendance_csv(csv_file="E:/Automated_Attendance_System/attendance.csv"):
    try:
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                enrollment_no = row['Enrollment_No']
                # Prevent duplication in DB
                mycur.execute("SELECT * FROM ATTENDANCE WHERE Enrollment_No = %s",(enrollment_no,))
                result = mycur.fetchone()

                if result:
                    print(f"⚠️ Already marked attendance for {enrollment_no} for today")
                    continue

                if mark_attendance(enrollment_no):
                    print(f"✅ Marked attendance for {enrollment_no}")
                else:
                    print(f"❌ Failed to mark attendance for {enrollment_no}")
    except Exception as e:
        print(f"Error: {e}")


#delete record after 7am and 8am
def delete_after_78am():
    now = dt.datetime.now()
    file_path = file_path_csv()
    if 7 <= now.hour <= 8:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print("✅ attendance.csv deleted after 6 AM")
            except Exception as e:
                print(f"❌ Error deleting file: {e}")
        else:
            print("ℹ️ File not found, nothing to delete.")
    else:
        print("⏳ It's not time yet (before 6 AM)")

yearly_attendance(mycur,mydb,'12345')