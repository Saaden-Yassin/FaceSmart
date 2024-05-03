from Model.User import User
from Controller.ProjectCRUD import *
from Controller.DepartmentCRUD import *
from Model.ConnectionToDB import *













class Employee(User):
    def __init__(self, ID: int = 0,
                 firstName: str = "",
                 lastName: str = "",
                 age: int = 0,
                 email: str = "",
                 image: str = "",
                 departmentName: str = None,
                 projectName: str = None,
                 schedulesIDsList: list[int] = None,
                 status: str = "Inactive"):
        super().__init__(ID, firstName, lastName, age, email, image)
        self.__departmentID: int = getDepartmentIDByName(departmentName) if departmentName else None
        self.__projectID: int = getProjectIDByName(projectName) if projectName else None
        self.__schedulesIDsList: list[int] = schedulesIDsList if schedulesIDsList else []
        self.__status: str = status

    # region getters!!!
    @property
    def ID(self):
        return self._ID

    @property
    def firstName(self):
        return self._firstName

    @property
    def lastName(self):
        return self._lastName

    @property
    def age(self):
        return self._age

    @property
    def email(self):
        return self._email

    @property
    def image(self):
        return self._image

    @property
    def departmentName(self):
        return self.__departmentID

    @property
    def projectName(self):
        return self.__projectID

    @property
    def schedulesIDsList(self):
        return self.__schedulesIDsList

    @property
    def status(self):
        return self.__status

    # endregion!!

    # region setters!!!
    @firstName.setter
    def firstName(self, firstName: str):
        self._firstName = firstName

    @lastName.setter
    def lastName(self, lastName: str):
        self._lastName = lastName

    @age.setter
    def age(self, age: int):
        self._age = age

    @email.setter
    def email(self, email: str):
        self._email = email

    @image.setter
    def image(self, image: str):
        self._image = image

    @departmentName.setter
    def departmentName(self, departmentName: str):
        self.__departmentID = getDepartmentIDByName(departmentName)

    @projectName.setter
    def projectName(self, projectName: str):
        self.__projectID = getProjectIDByName(projectName)

    @schedulesIDsList.setter
    def schedulesIDsList(self, schedulesIDsList: list):
        self.__schedulesIDsList = schedulesIDsList

    @status.setter
    def status(self, status: str):
        self.__status = status

    # endregion

    @staticmethod
    def listToString(listIDs):
        str1 = ","
        return str1.join(map(str, listIDs))

    # region Methods_To_Manipulate_SchedulesList
    def addScheduleIDToSchedulesIDsList(self, scheduleID: int, employeeID: int):
        try:
            cursor.execute("""SELECT schedulesIDsList FROM EMPLOYEES WHERE ID = ?""", (employeeID,))
            result = cursor.fetchone()
            if result:
                # Fetch existing list and convert it to a Python list
                schedulesIDsList = result[0].split(',') if result[0] else []
                # Convert all elements to integers for comparison
                schedulesIDsList = list(map(int, schedulesIDsList))

                if scheduleID not in schedulesIDsList:
                    schedulesIDsList.append(scheduleID)
                    cursor.execute("""UPDATE EMPLOYEES SET schedulesIDsList = ? WHERE ID = ?""",
                                   (self.listToString(schedulesIDsList), employeeID,))
                    conn.commit()
                else:
                    print("Schedule already exists !!!")
            else:
                print("Employee not found !")
        except sqlite3.Error as e:
            print("Error while added to schedules list :", e)

    def deleteSchedulesIDFromSchedulesIDsList(self, scheduleID, employeeID):
        try:
            cursor.execute("""SELECT ID, schedulesIDsList FROM EMPLOYEES WHERE ID = ? """, (employeeID,))
            result = cursor.fetchone()
            if result is not None:
                # Fetch existing list and convert it to a Python list
                schedulesIDsList = result[1].split(',') if result[1] else []

                # Convert all elements to integers for comparison
                schedulesIDsList = list(map(int, schedulesIDsList))

                if scheduleID in schedulesIDsList:
                    schedulesIDsList.remove(scheduleID)
                    cursor.execute("""UPDATE EMPLOYEES SET schedulesIDsList = ? WHERE ID = ?""",
                                   (self.listToString(schedulesIDsList), employeeID))
                    conn.commit()
                else:
                    print("Could not find this schedule")
            else:
                print("Employee not found !")
        except sqlite3.Error as e:
            print("Error while delete from schedules list:", e)

    # endregion

    def __str__(self):
        return f"{self.ID} | {self.firstName} - {self.lastName} | {str(self.age)} | {self.email} | {self.image} | {self.departmentName} | {self.projectName}"

    # region TableCreation
    @staticmethod
    def createEmployeesTable():
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS EMPLOYEES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                age INTEGER NOT NULL,
                email VARCHAR (255) NOT NULL UNIQUE,
                image TEXT NOT NULL UNIQUE,
                departmentID INTEGER,
                projectID INTEGER,
                schedulesIDsList TEXT,
                status VARCHAR(255) NOT NULL,
                FOREIGN KEY (departmentID) REFERENCES DEPARTMENTS(ID),
                FOREIGN KEY (projectID) REFERENCES PROJECTS(ID)
            )"""
        )
        conn.commit()
    # endregion


Employee.createEmployeesTable()
