from Controller.EmployeCRUD import *


class Schedule:
    def __init__(self, ID: int = 0,
                 employeeID: int = 0,
                 checkDay: str = datetime.now().strftime("%Y-%m-%d"),
                 beginningTime: str = datetime.now().strftime("%H:%M:%S"),
                 endingTime: str = None):
        self.__ID: int = ID
        self.__employeeID: int = employeeID
        self.__checkDay: str = checkDay
        self.__beginningTime: str = beginningTime
        self.__endingTime: str = endingTime

    # region getters!!!
    @property
    def ID(self):
        return self.__ID

    @property
    def employeeID(self):
        return self.employeeID

    @property
    def checkDay(self):
        return self.__checkDay

    @property
    def beginningTime(self):
        return self.__beginningTime

    @property
    def endingTime(self):
        return self.__endingTime

    # endregion!!

    # region setters!!!

    @employeeID.setter
    def employeeID(self, employeeID: str):
        self.__employeeID = employeeID

    @checkDay.setter
    def checkDay(self, checkDay: str):
        self.__checkDay = checkDay

    @beginningTime.setter
    def beginningTime(self, beginningTime: str):
        self.__beginningTime = beginningTime

    @endingTime.setter
    def endingTime(self, endingTime: str):
        self.__endingTime = endingTime

    # endregion

    def __str__(self):
        return (f"{self.ID} | {getEmployeeIDByImage(self.employeeID)} | {self.checkDay} "
                f"| {self.beginningTime} "
                f"| {self.endingTime}")

    # region Methods_To_Manipulate_Schedule

    def check_in(self):
        if self.__beginningTime is None:
            self.__beginningTime = datetime.now().strftime("%H:%M:%S")

    def check_out(self):
        self.__endingTime = datetime.now().strftime("%H:%M:%S")

    # endregion

    # region TableCreation
    @staticmethod
    def createSchedulesTable():
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS SCHEDULES (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    employeeId INTEGER NOT NULL,
                    beginningTime VARCHAR(255),
                    endingTime VARCHAR(255),
                    checkDay VARCHAR(255),
                    FOREIGN KEY (employeeId) REFERENCES EMPLOYEES(ID) ON DELETE CASCADE
               )""")
        except sqlite3.Error as e:
            print("Error creating table:", e)
        conn.commit()

    # endregion


Schedule.createSchedulesTable()
