from Controller.EmployeCRUD import *
from Model.Schedule import Schedule


# region Create_Schedule
def createSchedule(schedule: Schedule) -> bool:
    maxCheckinPerDay = 2
    try:
        # Check if there's an existing check-in without a corresponding check-out
        cursor.execute("""SELECT COUNT(*) FROM SCHEDULES 
                              WHERE employeeID = ? AND checkDay = ? AND beginningTime IS NOT NULL AND endingTime IS NULL""",
                       (schedule.employeeID, schedule.checkDay))
        pendingCheckinCount = cursor.fetchone()[0]
        if pendingCheckinCount > 0:
            print("You must check out before you can check in again.")
            return False

        # Check the number of check-ins for the day
        cursor.execute("""SELECT COUNT(*) FROM SCHEDULES 
                              WHERE employeeID = ? AND checkDay = ? AND beginningTime IS NOT NULL""",
                       (schedule.employeeID, schedule.checkDay))
        countCheckin = cursor.fetchone()[0]
        if countCheckin >= maxCheckinPerDay:
            print("You've reached the maximum number of check-ins for today.")
            return False

        # Insert new schedule entry for check-in
        cursor.execute("""INSERT INTO SCHEDULES(employeeID, checkDay, beginningTime) VALUES (?,?,?)""",
                       (schedule.employeeID, schedule.checkDay, schedule.beginningTime))
        conn.commit()
        print(f"Welcome {getEmployeeNameByID(schedule.employeeID)}!\nIt's a new day, meaning new challenges!")
        return True
    except Exception as e:
        print(f"An error occurred while creating schedule: {e}")
        return False


# endregion

# region Update_Schedule
def updateSchedule(employeeID: int):
    try:
        # Find the most recent check-in without a check-out
        cursor.execute(
            """SELECT * FROM SCHEDULES WHERE employeeID = ? AND endingTime IS NULL ORDER BY beginningTime DESC""",
            (employeeID,))
        schedule = cursor.fetchone()
        currentDay = datetime.now().strftime("%Y-%m-%d")
        if schedule:
            checkDay = schedule[4]
            if currentDay == checkDay:
                # Update the schedule with the check-out time
                cursor.execute("""UPDATE SCHEDULES SET endingTime = ? WHERE ID = ?""",
                               (datetime.now().strftime("%H:%M:%S"), schedule[0]))
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

# region Retrieve_Schedules
def getSchedules() -> list | None:
    try:
        cursor.execute("""SELECT * FROM SCHEDULES""")
        schedulesList = []
        schedules = cursor.fetchall()
        if schedules:
            for scdl in schedules:
                schedule = Schedule(ID=scdl[0], employeeID=scdl[1], beginningTime=scdl[2],
                                    endingTime=scdl[3], checkDay=scdl[4])
                schedulesList.append(schedule)
            return schedulesList
        else:
            return None
    except Exception as e:
        print(f"An error occurred while retrieving schedules: {e}")
        return None


# endregion

# region Delete_Schedule
def deleteSchedule(ID: int):
    try:
        cursor.execute("DELETE FROM SCHEDULES WHERE ID = ?", (ID,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while deleting schedule: {e}")


# endregion

# region Check_In
def scheduleCheckIn(ID) -> bool:
    try:
        if createSchedule(Schedule(employeeID=ID, beginningTime=datetime.now().strftime("%H:%M:%S"),
                                   checkDay=datetime.now().strftime("%Y-%m-%d"))):
            cursor.execute("""UPDATE EMPLOYEES SET status = 'Active' WHERE ID = ?""", (ID,))
            print("Check-in success!")
            conn.commit()
            return True
        else:
            print("Check-in failure")
            return False
    except Exception as e:
        print(f"An error occurred while checking in: {e}")
        return False


# endregion

# region Check_Out
def scheduleCheckOut(ID) -> bool:
    try:
        if updateSchedule(employeeID=ID):
            print("Check out success!")
            return True
        else:
            print("Check out failure")
            return False
    except Exception as e:
        print(f"An error occurred while checking out: {e}")
        return False


# endregion

# region Get_Last_Checkin_Or_Checkout
def getLastCheckinOrLastCheckout() -> list[str]:
    schedules = getSchedules()
    if schedules:
        lastSchedule: Schedule = schedules[-1]
        empID = lastSchedule.employeeID
        empImage = getEmployeeImageByID(empID)
        empName = getEmployeeNameByID(empID)
        endingTime = lastSchedule.endingTime
        beginningTime = lastSchedule.beginningTime

        lastCheck = [empID, empImage, empName]
        if lastSchedule.ID:
            if lastSchedule.endingTime:
                status = "CheckOut"
                lastCheck.append(endingTime)
                lastCheck.append(status)
                return lastCheck
            else:
                status = "CheckIn"
                lastCheck.append(beginningTime)
                lastCheck.append(status)
                return lastCheck
    return ["", "", "", "", ""]


# endregion
