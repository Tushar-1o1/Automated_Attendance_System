import mysql.connector
import datetime as dt
import time

def year_newyear():
    return dt.datetime.now().year

def connect():
    try:
        paswd = "123456"
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=paswd,
            database="ATTENDANCE_LIST"
        )
        mycur = mydb.cursor()
        print(51 * "*", "login successfully", 51 * "*")

        # Create STUDENT table
        mycur.execute("""
            CREATE TABLE IF NOT EXISTS STUDENT(
                Enrollment_No VARCHAR(30) PRIMARY KEY,
                Name VARCHAR(30),
                Class_Name VARCHAR(10),
                Is_Active INT
            )
        """)

        # Create ATTENDANCE table
        mycur.execute("""
            CREATE TABLE IF NOT EXISTS ATTENDANCE(
                ID INT PRIMARY KEY AUTO_INCREMENT,
                Enrollment_No VARCHAR(30),
                Date DATE,
                Status VARCHAR(10),
                UNIQUE (Enrollment_No, Date)
            )
        """)

        # Create YEARLY_ATTENDANCE table
        year = year_newyear()
        new_year = year + 1
        str_year = f"Year_{year}_{new_year}"
        mycur.execute(f"""
            CREATE TABLE IF NOT EXISTS YEARLY_ATTENDANCE(
                Enrollment_No VARCHAR(30) PRIMARY KEY,
                `{str_year}` INT DEFAULT 0
            )
        """)

        # Insert dummy students only if table is empty
        mycur.execute("SELECT COUNT(*) FROM STUDENT")
        count = mycur.fetchone()[0]
        if count == 0:
            mycur.executemany("""
                INSERT INTO STUDENT (Enrollment_No, Name, Class_Name, Is_Active) VALUES (%s, %s, %s, %s)
            """, [
                ('2023001', 'Tushar', '10A', 1),
                ('2023002', 'Sneha Patel', '10A', 1),
                ('2023003', 'Rahul Singh', '10B', 1),
                ('2023004', 'Pooja Gupta', '10B', 1),
                ('2023005', 'Karan Verma', '10C', 1),
                ('2023006', 'Anjali Rao', '10C', 1),
                ('2023007', 'Vikram Joshi', '10D', 1),
                ('2023008', 'Divya Nair', '10D', 1),
                ('2023009', 'Manish Kumar', '10A', 1),
                ('2023010', 'Neha Mehta', '10B', 1)
                ('2023011', 'sargam', '10B', 1)
            ])
            print("✅ Dummy student data inserted.")

        mydb.commit()
        return True, mycur, mydb, str_year

    except mysql.connector.Error as err:
        print("Invalid Credentials or Error:", err)
        time.sleep(5)
        return False, None, None, None

if __name__ == "__main__":
    connect()
