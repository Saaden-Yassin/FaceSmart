from Model.Department import *


def listToString(listIds):
    str1 = ","
    return str1.join(map(str, listIds))


# region Create_Department!!!
def createDepartment(department: Department):
    try:
        cursor.execute(
            """INSERT INTO DEPARTMENTS (name, employeesIdsList)
               VALUES (?, ?)""",
            (department.name, Department.listToString(department.employeesIDsList))
        )
        conn.commit()
        print("Department inserted successfully.")
    except sqlite3.Error as sqlerror:
        print("Error inserting department:", sqlerror)


# endregion

# region Retrieve_Departments!!!
def getDepartment() -> list | None:
    cursor.execute("""SELECT * FROM DEPARTMENTS""")
    departmentsList = []
    departments = cursor.fetchall()
    if departments:
        for dep in departments:
            department = Department(dep[0], dep[1], dep[2])
            departmentsList.append(department)
        return departmentsList
    else:
        return None


# endregion

# region Update_Departments!!!
def updateDepartment(ID: int,
                     name: str = None,
                     employeesIDsList: str = None):
    sql: str = "UPDATE DEPARTMENTS SET "
    parameters = []
    if name:
        sql += "name = ?, "
        parameters.append(name)
    if employeesIDsList is not None:
        for empID in employeesIDsList:
            try:
                cursor.execute("""SELECT COUNT(*) FROM Employees WHERE ID = ?""", (empID,))
                result = cursor.fetchone()
                if result[0] == 0:
                    print(f"Employee with ID {empID} does not exist.")
            except Exception as e:
                print(f"Error while checking employee ID {empID}: {e}")

        cursor.execute("""SELECT employeesIDsList FROM DEPARTMENTS WHERE ID = ?""", (ID,))
        result = cursor.fetchone()
        if result:
            existingIDs = result[0].split(',') if result[0] else []
            existingIDs = list(map(int, existingIDs))
            for empID in employeesIDsList:
                if empID not in existingIDs:
                    existingIDs.append(empID)
            employeesIDsList = listToString(existingIDs)

        sql += "employeesIDsList = ?, "
        parameters.append(employeesIDsList)
    sql = sql[:-2]
    sql += " WHERE ID = ?"
    parameters.append(ID)
    cursor.execute(sql, tuple(parameters))
    conn.commit()


# endregion

# region Delete_Department!!!
def deleteDepartment(ID: int):
    cursor.execute("DELETE FROM DEPARTMENTS WHERE ID = ?", (ID,))
    conn.commit()


# endregion

# region getDepartmentIDByName
def getDepartmentIDByName(departmentName: str):
    try:
        cursor.execute("""SELECT ID FROM DEPARTMENTS WHERE name = ?""", (departmentName,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print("Error while fetching results : {0}", format(e))


# endregion

# region verifyDepartmentExistenceByName
def verifyDepartmentExistenceByName(departmentName: str):
    try:
        cursor.execute("""SELECT COUNT(*) FROM DEPARTMENTS WHERE name = ?""", (departmentName,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error verifying DEPARTMENT existence by name :", e)
        return False
# endregion
