from Model.Schedule import *
from Controller.EmployeCRUD import *













# region Create_Schedule!!!
def createSchedule(schedule: Schedule) -> bool:
    maxCheckinPerDay = 2
    maxCheckOutPerDay = 2
    try:
        cursor.execute("""SELECT COUNT(*) FROM SCHEDULES 
                              WHERE employeeID = ? AND checkDay = ? AND beginningTime IS NOT NULL""",
                       (schedule.employeeID, schedule.checkDay))
        countCheckin = cursor.fetchone()[0]
        if countCheckin >= maxCheckinPerDay:
            print("You've reached the maximum number of check-ins for today.")
            return False

        cursor.execute("""SELECT COUNT(*) FROM SCHEDULES 
                              WHERE employeeID = ? AND checkDay = ? AND endingTime IS NOT NULL""",
                       (schedule.employeeID, schedule.checkDay))
        countCheckOut = cursor.fetchone()[0]
        if countCheckOut >= maxCheckOutPerDay:
            print("You've reached the maximum number of check-outs for today.")
            return False

        cursor.execute("""INSERT INTO SCHEDULES(employeeID, checkDay, beginningTime) VALUES (?,?,?)""",
                       (schedule.employeeID, schedule.checkDay, schedule.beginningTime))
        conn.commit()
        print(f"Welcome {getEmployeeNameByID(schedule.employeeID)}!\nIt's a new day, meaning new challenges!")
        return True
    except Exception as e:
        print(f"An error occurred while creating schedule: {e}")
        return False


# endregion

# region Retrieve_Schedules!!!
def getSchedules() -> list | None:
    try:
        cursor.execute("""SELECT * FROM SCHEDULES""")
        schedulesList = []
        schedules = cursor.fetchall()
        if schedules:
            for scdl in schedules:
                schedule = Schedule(scdl[0], scdl[1], scdl[2], scdl[3], scdl[4])
                schedulesList.append(schedule)
            return schedulesList
        else:
            return None
    except Exception as e:
        print(f"An error occurred while retrieving schedules: {e}")
        return None


# endregion

# region Update_Schedule!!!
def updateSchedule(employeeID: int):
    try:
        cursor.execute("""SELECT * FROM SCHEDULES WHERE employeeID = ? AND endingTime IS NULL""", (employeeID,))
        schedule = cursor.fetchone()
        currentDay = datetime.now().strftime("%Y-%m-%d")
        if schedule:
            if currentDay != schedule[3]:
                cursor.execute("""UPDATE SCHEDULES SET endingTime = ?""", (datetime.now().strftime("%H:%M:%S"),))
                cursor.execute("""UPDATE EMPLOYEES SET status = 'Inactive' WHERE ID = ?""", (employeeID,))
                print(f"Nice work for today {getEmployeeNameByID(employeeID)}!\nBYE BYE!")
                conn.commit()
                return True
            else:
                print("You already checked out!")
                return False
        else:
            print("Error! Maybe you didn't check in")
            return False
    except Exception as e:
        print(f"An error occurred while updating schedule: {e}")
        return False


# endregion

# region Delete_Schedule!!!
def deleteSchedule(ID: int):
    try:
        cursor.execute("DELETE FROM SCHEDULES WHERE ID = ?", (ID,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while deleting schedule: {e}")


# endregion

# region checkIn
def checkIn(image: str) -> bool:
    try:
        if verifyEmployeeExistenceByImage(image):
            if createSchedule(Schedule(employeeImage=image, checkDay=datetime.now().strftime("%Y-%m-%d"))):
                cursor.execute("""UPDATE EMPLOYEES SET status = 'Active' WHERE ID = ?""",
                               (getEmployeeIDByImage(image),))
                print("Checking success!")
                conn.commit()
                return True
            else:
                print("Checking failure")
                return False
        else:
            print("Unknown person!")
            return False
    except Exception as e:
        print(f"An error occurred while checking in: {e}")
        return False


# endregion

# region checkOut
def checkOut(image: str) -> bool:
    try:
        if verifyEmployeeExistenceByImage(image):
            employeeID = getEmployeeIDByImage(image)
            if updateSchedule(employeeID=employeeID):
                print("Check out success!")
                return True
            else:
                print("Check out failure")
                return False
        else:
            print("Unknown person!")
            return False
    except Exception as e:
        print(f"An error occurred while checking out: {e}")
        return False
# endregion
