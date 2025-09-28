import database 
import datetime as dt,time
flag,mycur,mydb=database.connect()

import datetime as dt

def year_newyear():
    year=dt.datetime.now().year
    return year

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



alter_Table(mydb,mycur)