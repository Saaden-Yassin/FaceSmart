from Model.Manager import *

# region Create_Managers!!!
def createManager(manager: Manager):
    try:
        cursor.execute(
            """
            INSERT INTO Managers(firstName, lastName, username, age, email, image, password) VALUES (?,?,?,?,?,?,?)
            """,
            (manager.firstName, manager.lastName, manager.username, manager.age, manager.email, manager.image,
             manager.password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# endregion

# region Retrieve_Manager!!!
def getAllManagers() -> list | None:
    cursor.execute("""SELECT * FROM Managers""")
    managersList = []
    managers = cursor.fetchall()
    if managers:
        for mng in managers:
            manager = Manager(mng[0], mng[1], mng[2], mng[3], mng[4], mng[5], mng[6], mng[7])
            managersList.append(manager)
        return managersList
    else:
        return None


# endregion

# region Update_Manager!!!
def updateManager(ID: int, firstName: str = None, lastName: str = None, username: str = None, age: int = None,
                  email: str = None, image: str = None,
                  password: str = None):
    sql = "UPDATE MANAGERS SET "
    parameters = []
    if firstName:
        sql += "firstName = ?, "
        parameters.append(firstName)
    if lastName:
        sql += "lastName = ?, "
        parameters.append(lastName)
    if username:
        sql += "username = ?, "
        parameters.append(username)
    if age:
        sql += "age = ?, "
        parameters.append(age)
    if email:
        sql += "email = ?, "
        parameters.append(email)
    if image:
        sql += "image = ?, "
        parameters.append(image)
    if password:
        sql += "password = ?, "
        parameters.append(password)
    sql = sql[:-2]
    sql += " WHERE ID = ?"
    parameters.append(ID)
    cursor.execute(sql, tuple(parameters))
    conn.commit()


# endregion

# region Delete_Manager!!!
def deleteManager(ID: int):
    cursor.execute("""DELETE FROM Managers WHERE ID = ?""", (ID,))
    conn.commit()


# endregion

# region signin!!!
def getManager(username: str = None, password: str = None, image: str = None):
    if not (username and password):
        print("Invalid parameters provided.")
        return False

    if image:
        cursor.execute("SELECT image FROM managers WHERE image = ?", (image,))
        result = cursor.fetchone()
        if result:
            print("Manager found by image.")
            return True
        else:
            print("Manager not found by image.")
            return False

    if username and password:
        cursor.execute("SELECT username, password FROM managers WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            if result[1] == password:
                print("Manager logged in successfully.")
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("Invalid username.")
            return False


# endregion

# region getEmployeesImages
def getEmployeesImages() -> list[dict] | None:
    try:
        cursor.execute("""SELECT ID, image FROM EMPLOYEES""")
        employeesImagesAndIDs = []
        rows = cursor.fetchall()
        for row in rows:
            employeesImagesAndIDs.append({"id": row[0], "image": row[1]})
        return employeesImagesAndIDs
    except sqlite3.Error as e:
        print("Error retrieving employees' images:", e)
        return None
# endregion
