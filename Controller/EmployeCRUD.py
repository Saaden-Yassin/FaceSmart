from Model.Employe import *
from Controller.DepartmentCRUD import *


def listToString(listIds):
    str1 = ","
    return str1.join(map(str, listIds))


# region Create_Employees!!!
def createEmployee(employee: Employee):
    departmentID = None
    projectID = None

    if employee.departmentName is not None:
        if not verifyDepartmentExistenceByName(employee.departmentName):
            print("Department doesn't exist!")
            return False
        departmentID = getDepartmentIDByName(employee.departmentName)

    if employee.projectName is not None:
        if not verifyProjectExistenceByName(employee.projectName):
            print("Project doesn't exist!")
            return False
        projectID = getProjectIDByName(employee.projectName)

    try:
        cursor.execute(
            """
            INSERT INTO EMPLOYEES(firstName, lastName, age, email, image, departmentID, projectID, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (employee.firstName, employee.lastName, employee.age, employee.email, employee.image,
             departmentID, projectID, "Inactive")
        )
        conn.commit()
        print("Employee created successfully!")
        return True
    except sqlite3.Error as e:
        print("Error creating employee:", e)
        return False


# endregion

# region Retrieve_Employees!!!
def getEmployees() -> list | None:
    cursor.execute("""SELECT * FROM EMPLOYEES""")
    employeesList = []
    employees = cursor.fetchall()
    if employees:
        for emp in employees:
            employee = Employee(ID=emp[0], firstName=emp[1], lastName=emp[2], age=emp[3], email=emp[4],
                                image=emp[5], departmentName=emp[6], projectName=emp[7], status=emp[9])
            employeesList.append(employee)
        return employeesList
    else:
        return None


# endregion

# region Update_Employee!!!
def updateEmployee(ID: int, firstName: str = None, lastName: str = None, age: int = None, email: str = None,
                   image: str = None, departmentName: str = None, projectName: str = None) -> bool:
    # region update EmployeesTable
    sql: str = "UPDATE EMPLOYEES SET "
    parameters = []
    if firstName:
        sql += "firstName = ?, "
        parameters.append(firstName)
    if lastName:
        sql += "lastName = ?, "
        parameters.append(lastName)
    if age:
        sql += "age = ?, "
        parameters.append(age)
    if email:
        sql += "email = ?, "
        parameters.append(email)
    if image:
        sql += "image = ?, "
        parameters.append(image)
    if departmentName:
        sql += "departmentName = ?, "
        parameters.append(departmentName)
    if projectName:
        sql += "projectName = ?, "
        parameters.append(projectName)
    sql = sql[:-2]
    sql += " WHERE ID = ?"
    parameters.append(ID)
    if cursor.execute(sql, tuple(parameters)):
        conn.commit()
        return True
    else:
        return False
    # endregion


# endregion

# region Delete_Employee!!!
def deleteEmployee(ID: int):
    try:
        # region Delete the employee's schedules
        cursor.execute("""SELECT * FROM SCHEDULES WHERE employeeID = ?""", (ID,))
        result = cursor.fetchall()
        if result:
            cursor.execute("DELETE FROM SCHEDULES WHERE employeeID = ?", (ID,))
        # endregion

        # region Delete_Employee_From_EmployeesList_In_ProjectsTable
        cursor.execute("""SELECT ID FROM PROJECTS WHERE employeesIDsList LIKE ?""", ('%' + str(ID) + '%',))
        projects = cursor.fetchall()
        for project in projects:
            cursor.execute("""SELECT employeesIDsList FROM PROJECTS WHERE ID = ?""", (project[0],))
            result = cursor.fetchone()
            if result:
                employeesIDsList = result[0].split(',') if result[0] else []
                employeesIDsList = [int(emp_id) for emp_id in employeesIDsList if int(emp_id) != ID]
                cursor.execute("""UPDATE PROJECTS SET employeesIDsList = ? WHERE ID = ?""",
                               (Project.listToString(employeesIDsList), project[0]))
        # endregion

        # region Delete_Employee_From_EmployeesList_In_DepartmentsTable
        cursor.execute("""SELECT ID FROM DEPARTMENTS WHERE employeesIDsList LIKE ?""", ('%' + str(ID) + '%',))
        departments = cursor.fetchall()
        for department in departments:
            cursor.execute("""SELECT employeesIDsList FROM DEPARTMENTS WHERE ID = ?""", (department[0],))
            result = cursor.fetchone()
            if result:
                employeesIDsList = result[0].split(',') if result[0] else []
                employeesIDsList = [int(emp_id) for emp_id in employeesIDsList if int(emp_id) != ID]
                cursor.execute("""UPDATE DEPARTMENTS SET employeesIDsList = ? WHERE ID = ?""",
                               (Department.listToString(employeesIDsList), department[0]))
        # endregion

        # region Delete_From_EmployeesTable
        cursor.execute("DELETE FROM Employees WHERE ID = ?", (ID,))
        # endregion

        conn.commit()
    except sqlite3.Error as e:
        print("Error deleting employee:", e)


# endregion

# region getEmployeeById
def getEmployeeById(ID: int) -> list | None:
    try:
        cursor.execute("""SELECT * FROM EMPLOYEES WHERE ID = ?""", (ID,))
        employee = cursor.fetchone()
        if employee:
            return [Employee(ID=employee[0], firstName=employee[1], lastName=employee[2], age=employee[3],
                             email=employee[4], image=employee[5])]
        else:
            print("Employee Not Found")
            return None
    except sqlite3.Error as e:
        print("Error fetching employee:", e)
        return None


# endregion

# region getEmployeeIDByImage
def getEmployeeIDByImage(image: str) -> int | None:
    try:
        cursor.execute("""SELECT ID FROM EMPLOYEES WHERE image = ?""", (image,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Employee with given image not found")
            return None
    except sqlite3.Error as e:
        print("Error fetching employee ID by image:", e)
        return None


# endregion

# region getEmployeeNameByID
def getEmployeeNameByID(ID: int) -> str | None:
    try:
        cursor.execute("""SELECT firstName, lastName FROM EMPLOYEES WHERE ID = ?""", (ID,))
        result = cursor.fetchone()
        if result:
            return f"{result[0]} {result[1]}"
        else:
            print("Employee with given ID not found")
            return None
    except sqlite3.Error as e:
        print("Error fetching employee name by ID:", e)
        return None


# endregion

# region verifyEmployeeExistenceByImage
def verifyEmployeeExistenceByImage(image: str) -> bool:
    try:
        cursor.execute("""SELECT COUNT(*) FROM EMPLOYEES WHERE image = ?""", (image,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error verifying employee existence by image:", e)
        return False


# endregion

# region getTotalNumberOfEmployees
def getTotalNumberOfEmployees() -> int:
    try:
        cursor.execute("SELECT COUNT(*) FROM EMPLOYEES")
        total_employees = cursor.fetchone()[0]
        return total_employees
    except sqlite3.Error as e:
        print("Error retrieving total number of employees:", e)
        return 0


# endregion

# region getNumberEmployeesActive
def getNumberEmployeesActive() -> int:
    try:
        cursor.execute("SELECT COUNT(*) FROM EMPLOYEES WHERE status = 'Active'")
        active_employees = cursor.fetchone()[0]
        return active_employees
    except sqlite3.Error as e:
        print("Error retrieving number of active employees:", e)
        return 0


# endregion

# region getNumberEmployeesInactive
def getNumberEmployeesInactive() -> int:
    try:
        cursor.execute("SELECT COUNT(*) FROM EMPLOYEES WHERE status = 'Inactive'")
        inactive_employees = cursor.fetchone()[0]
        return inactive_employees
    except sqlite3.Error as e:
        print("Error retrieving number of inactive employees:", e)
        return 0


# endregion

# region getEmployeesTableSorted
def getEmployeesTableSorted(criteria: str = "ID", sortMode: str = "ASC"):
    try:
        cursor.execute(f"SELECT * FROM EMPLOYEES ORDER BY {criteria} {sortMode}")
        employeesList = []
        employees = cursor.fetchall()
        if employees:
            for emp in employees:
                employee = Employee(ID=emp[0], firstName=emp[1], lastName=emp[2], age=emp[3], email=emp[4],
                                    image=emp[5], departmentName=emp[6], projectName=emp[7], status=emp[8])
                employeesList.append(employee)
            return employeesList
        else:
            return None
    except sqlite3.Error as e:
        print("Error retrieving sorted employees:", e)
        return None


# endregion

# region getEmployeeImageByID
def getEmployeeImageByID(ID: int) -> str | None:
    try:
        cursor.execute("""SELECT image FROM EMPLOYEES WHERE ID = ?""", (ID,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Employee with given ID not found")
            return None
    except sqlite3.Error as e:
        print("Error fetching employee image by ID:", e)
        return None
# endregion
