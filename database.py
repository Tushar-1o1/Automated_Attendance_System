import mysql.connector
import datetime as dt, time

def year_newyear():
    year=dt.datetime.now().year
    return year

def connect():
    try:
        paswd=input("Enter Login Password = ")
        mydb=mysql.connector.connect(host="localhost",
                                     user="root",
                                     password=paswd,
                                     database="ATTENDANCE_LIST")
        
        mycur=mydb.cursor()
        print(51*"*","login successfully",51*"*")

        mycur.execute("""
                CREATE TABLE IF NOT EXISTS STUDENT(
                Enrollment_No varchar(30) PRIMARY KEY,
                Name varchar(30),
                Class_Name varchar(10),
                Is_Active int
                )
            """)

        mycur.execute("""
                CREATE TABLE IF NOT EXISTS ATTENDANCE(
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Enrollment_No varchar(30),
                Date DATE,
                Status VARCHAR(10)
                )
            """)
        year=year_newyear()
        new_year=year+1
        str_year = f"Year_{year}_{new_year}"
        mycur.execute(f"""
                CREATE TABLE IF NOT EXISTS YEARLY_ATTENDANCE(
                Enrollment_No varchar(30) PRIMARY KEY,
                {str_year} INT DEFAULT 0
                )
            """)

        mydb.commit()
        return True, mycur, mydb
    except mysql.connector.Error as err:
        print("Invalid Credentials:", err)
        time.sleep(5)
        return False, None, None

if __name__ == "__main__":
    connect()