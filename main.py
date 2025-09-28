import database 
import datetime as dt,time
import os


flag,mycur,mydb=database.connect()

#get todaysdate
def tdate():
    date=dt.datetime.now().date()
    return date


#get current year
def year_newyear():
    year=dt.datetime.now().year
    return year


#This is to get all files name
def get_all_files():
    current_dir = os.getcwd()
    all_items = os.listdir(current_dir)
    files = [f for f in all_items if os.path.isfile(os.path.join(current_dir, f))]
    return files


#this is to get current working directory and change directories
def dir_file():
    cwd = os.getcwd()
    all_items = os.listdir(cwd)
    folder_name='known_faces'
    if folder_name in all_items and os.path.isdir(os.path.join(cwd, folder_name)):
        os.chdir('known_faces')
        return get_all_files()
    else:
        return None
 

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
        print("Today is not March 31.")


def mark_attendance(enrollment_number):
    try:
        files=dir_file()
        file_names_without_ext = [os.path.splitext(f)[0] for f in files]
        if enrollment_number in file_names_without_ext:
            date=tdate()
            status='present'
            mycur.execute("INSERT INTO ATTENDANCE (Enrollment_No, Date, Status) VALUES (%s, %s, %s)",(enrollment_number, date, status))
            mydb.commit()
        else:
            print(files)
    except Exception as e:
        print(e)

mark_attendance('12345')
#alter_Table(mydb,mycur)