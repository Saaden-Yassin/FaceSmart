import base64
from threading import Thread

import cv2
import face_recognition
import numpy as np

from Controller.EmployeCRUD import *
from Model.Schedule import *


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

# region Retrieve_Schedules!!!
def getSchedules() -> list | None:
    try:
        cursor.execute("""SELECT * FROM SCHEDULES""")
        schedulesList = []
        schedules = cursor.fetchall()
        if schedules:
            for scdl in schedules:
                schedule = Schedule(ID=scdl[0], employeeID=scdl[1], beginningTime=scdl[2],
                                    endingTime=scdl[3],
                                    checkDay=scdl[4])
                schedulesList.append(schedule)
            return schedulesList
        else:
            return None
    except Exception as e:
        print(f"An error occurred while retrieving schedules: {e}")
        return None


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
def scheduleCheckIn(ID) -> bool:
    try:
        if createSchedule(Schedule(employeeID=ID, beginningTime=datetime.now().strftime("%H:%M:%S"),
                                   checkDay=datetime.now().strftime("%Y-%m-%d"))):
            cursor.execute("""UPDATE EMPLOYEES SET status = 'Active' WHERE ID = ?""",
                           (id,))
            print("Checking success!")
            conn.commit()
            return True
        else:
            print("Checking failure")
            return False
    except Exception as e:
        print(f"An error occurred while checking in: {e}")
        return False


# endregion

# region checkOut
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

# region getLastCheckinOrLastCheckout
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


def loadEmployeesFaceEncodings():
    employeeImages = getEmployeesImages()
    employeesFaceEncodings = []
    employeeIds = []
    for data in employeeImages:
        # Decode the base64 encoded image
        imageData = base64.b64decode(data["image"])
        # Convert bytes to numpy array
        npArray = np.frombuffer(imageData, np.uint8)
        # Decode numpy array to image
        employeeImage = cv2.imdecode(npArray, cv2.IMREAD_COLOR)
        # Get face encodings if a face is detected
        face_encodings = face_recognition.face_encodings(employeeImage)
        if face_encodings:
            faceEncoding = face_encodings[0]  # Take the first detected face
            employeesFaceEncodings.append(faceEncoding)
            employeeIds.append(data["id"])
        else:
            print("No face detected for employee with ID:", data["id"])
    return employeesFaceEncodings, employeeIds


# Function to recognize faces and return existence status, employee ID, and date
def recognize_faces(rgb_image, image, known_face_encodings, employee_ids):
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face encoding with the known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # If there is a match
        if True in matches:
            # Find the index of the matched face
            match_index = matches.index(True)
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            # Get employee ID and current date
            employee_id = employee_ids[match_index]
            return True, employee_id
        else:
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    # If no match found
    return False, None
