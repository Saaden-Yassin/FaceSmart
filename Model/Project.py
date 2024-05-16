from Database.ConnectionToDB import *


class Project:
    def __init__(self, ID: int = 0,
                 name: str = "",
                 startDate: str = "",
                 endDate: str = "",
                 status: str = "",
                 employeesIDsList: list[int] = None):
        self.__id: int = ID
        self.__name: str = name
        self.__startDate: str = startDate
        self.__endDate: str = endDate
        self.__status: str = status
        self.__employeesIDsList: list[int] = employeesIDsList if employeesIDsList else []

    # region getters!!!
    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def startDate(self):
        return self.__startDate

    @property
    def endDate(self):
        return self.__endDate

    @property
    def status(self):
        return self.__status

    @property
    def employeesIDsList(self):
        return self.__employeesIDsList

    # endregion!!

    # region setters!!!
    @name.setter
    def name(self, name: str):
        self.__name = name

    @startDate.setter
    def startDate(self, startDate: str):
        self.__startDate = startDate

    @endDate.setter
    def endDate(self, endDate: str):
        self.__endDate = endDate

    @status.setter
    def status(self, status: str):
        self.__status = status

    @employeesIDsList.setter
    def employeesIDsList(self, employeesIDsList: list):
        self.__employeesIDsList = employeesIDsList

    # endregion

    def __str__(self):
        return f"{self.ID} | {self.name} | {self.startDate} | {self.endDate} | {self.status} | {self.employeesIDsList}"

    # region Methods_To_Manipulate_EmployeesIdsList

    @staticmethod
    def listToString(listIds):
        str1 = ","
        return str1.join(map(str, listIds))

    def addEmployeeIdToEmployeesIdsList(self, employeeID: int, projectID: int):
        try:
            cursor.execute("""SELECT employeesIDsList FROM PROJECTS WHERE ID = ?""", (projectID,))
            result = cursor.fetchone()
            if result:
                # Fetch existing list and convert it to a Python list
                employeesIDsList = result[0].split(',') if result[0] else []
                # Convert all elements to integers for comparison
                employeesIDsList = list(map(int, employeesIDsList))

                if employeeID not in employeesIDsList:
                    employeesIDsList.append(employeeID)
                    cursor.execute("""UPDATE PROJECTS SET employeesIDsList = ? WHERE ID = ?""",
                                   (self.listToString(employeesIDsList), projectID,))
                    conn.commit()
                else:
                    print("Employee already exists !!!")
            else:
                print("Project not found !")
        except sqlite3.Error as e:
            print("Error or update employees list :", e)

    def deleteEmployeeIDFromEmployeesIDsList(self, employeeID, projectID):
        try:
            cursor.execute("""SELECT ID, employeesIDsList FROM PROJECTS WHERE ID = ? """, (projectID,))
            result = cursor.fetchone()
            if result is not None:
                # Fetch existing list and convert it to a Python list
                employeesIDsList = result[1].split(',') if result[1] else []

                # Convert all elements to integers for comparison
                employeesIDsList = list(map(int, employeesIDsList))

                if employeeID in employeesIDsList:
                    employeesIDsList.remove(employeeID)
                    cursor.execute("""UPDATE PROJECTS SET employeesIDsList = ? WHERE ID = ?""",
                                   (self.listToString(employeesIDsList), projectID))
                    conn.commit()
                else:
                    print("Could not find this employee")
            else:
                print("Project not found !")
        except sqlite3.Error as e:
            print("Error delete or update employees list:", e)

    # endregion

    # region TableCreation
    @staticmethod
    def createProjectsTable():
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS PROJECTS (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    startDate VARCHAR(255) NOT NULL,
                    endDate VARCHAR(255) NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    employeesIDsList TEXT
               )""")
        except sqlite3.Error as e:
            print("Error creating table:", e)
        conn.commit()

    # endregion


Project.createProjectsTable()
