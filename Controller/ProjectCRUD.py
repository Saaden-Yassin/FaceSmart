from Model.Project import *
from datetime import datetime


def listToString(listIds):
    str1 = ","
    return str1.join(map(str, listIds))


# region Create_Project!!!
def createProject(project: Project) -> bool:
    try:
        Project()
        cursor.execute(
            """INSERT INTO PROJECTS (name, startDate, endDate, status, employeesIdsList)
               VALUES (?, ?, ?, ?, ?)""",
            (project.name, project.startDate, project.endDate, project.status,
             Project.listToString(project.employeesIDsList))
        )
        conn.commit()
        print("Project inserted successfully.")
        return True
    except sqlite3.Error as sqlerror:
        print("Error inserting project:", sqlerror)
        return False


# endregion

# region Retrieve_Projects!!!
def getProjects() -> list[Project] | None:
    cursor.execute("""SELECT * FROM PROJECTS""")
    projectsList = []
    projects = cursor.fetchall()
    if projects:
        for prjct in projects:
            projectsList.append(Project(prjct[0], prjct[1], prjct[2], prjct[3], prjct[4], prjct[5]))
        return projectsList
    else:
        return None


# endregion

# region Update_Projects!!!
def updateProject(ID: int,
                  name: str = None,
                  startDate: str = None,
                  endDate: str = None,
                  status: str = None,
                  employeesIDsList: list = None):
    sql: str = "UPDATE PROJECTS SET "
    parameters = []
    try:
        if name:
            sql += "name = ?, "
            parameters.append(name)
        if startDate:
            sql += "startDate = ?, "
            parameters.append(startDate)
        if endDate:
            sql += "endDate = ?, "
            parameters.append(endDate)
        if status:
            sql += "status = ?, "
            parameters.append(status)
        if employeesIDsList is not None:
            for empID in employeesIDsList:
                try:
                    cursor.execute("""SELECT COUNT(*) FROM Employees WHERE ID = ?""", (empID,))
                    result = cursor.fetchone()
                    if result[0] == 0:
                        print(f"Employee with ID {empID} does not exist.")
                except Exception as e:
                    print(f"Error while checking employee ID {empID}: {e}")

            cursor.execute("""SELECT employeesIDsList FROM PROJECTS WHERE ID = ?""", (ID,))
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
    except Exception as e:
        print(f"Error occurred while updating project: {e}")
        conn.rollback()


# endregion

# region Delete_Project!!!
def deleteProject(ID: int):
    cursor.execute("DELETE FROM PROJECTS WHERE ID = ?", (ID,))
    conn.commit()


# endregion

# region getProjectIDByName
def getProjectIDByName(projectName: str) -> int | None:
    try:
        cursor.execute("""SELECT ID FROM PROJECTS WHERE name = ?""", (projectName,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print("Error while fetching results : {0}", format(e))


# endregion

# region verifyProjectExistenceByName
def verifyProjectExistenceByName(projectName: str):
    try:
        cursor.execute("""SELECT COUNT(*) FROM PROJECTS WHERE name = ?""", (projectName,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error verifying project existence by name :", e)
        return False


# endregion

# region getTimeLeftForDeadline
def getTimeLeftForDeadline(project: Project) -> int | None:
    try:
        endDate = datetime.strptime(project.endDate, "%Y-%m-%d")
        currentDate = datetime.now()
        timeLeft = endDate - currentDate
        daysLeft = timeLeft.days
        print(f"Days left for project '{project.name}' deadline: {daysLeft}")
        return daysLeft
    except Exception as e:
        print(f"An error occurred while calculating time left for deadline: {e}")
        return None


# endregion

# region getProjectNameByID
def getProjectNameByID(ID: int) -> str | None:
    try:
        cursor.execute("""SELECT name FROM PROJECTS WHERE ID = ?""", (ID,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Project with given ID not found")
            return None
    except sqlite3.Error as e:
        print("Error fetching project name by ID:", e)
        return None


# endregion

# region getProjectsTableSorted
def getProjectsTableSorted(criteria: str = "ID", sortMode: str = "ASC") -> list[Project] | None:
    try:
        cursor.execute(f"SELECT * FROM PROJECTS ORDER BY {criteria} {sortMode}")
        projectsList = []
        projects = cursor.fetchall()
        if projects:
            for prjct in projects:
                projectsList.append(Project(prjct[0], prjct[1], prjct[2], prjct[3], prjct[4], prjct[5]))
            return projectsList
        else:
            return None
    except sqlite3.Error as e:
        print("Error retrieving sorted projects:", e)
        return None

# endregion
