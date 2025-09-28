import mysql.connector
import time

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
                ID INT PRIMARY KEY,
                Enrollment_No varchar(30),
                Date DATE,
                Status VARCHAR(10)
                )
            """)
        mycur.execute("""
                CREATE TABLE IF NOT EXISTS YEARLY_ATTENDANCE(
                Enrollment_No varchar(30) PRIMARY KEY,
                Year_2025_2026 INT
                )
            """)

        mydb.commit()
        return True, mycur, mydb
    except mysql.connector.Error as err:
        print("Invalid Credentials:", err)
        time.sleep(2)
        return False, None, None
connect()
