from Model.Manager import *



















# region Create_Managers!!!
def createManager(manager: Manager):
    if cursor.execute(
            """
        INSERT INTO Managers(firstName, lastName, username, age, email, image, password) VALUES (?,?,?,?,?,?,?)
        """,
            (manager.firstName, manager.lastName, manager.username, manager.age, manager.email, manager.image,
             manager.password)
    ):
        conn.commit()
        return True
    else:
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
    sql: str = "UPDATE EMPLOYEES SET "
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
    if image is not None:
        cursor.execute("SELECT image FROM MANAGERS WHERE image = ?", (image,))
        result = cursor.fetchone()
        if result:
            print("logged successfully")
        else:
            print("Manager not found !!!")
    elif username is not None and password is not None:
        hash_password = str(hash(password))
        cursor.execute("SELECT username, password FROM MANAGERS WHERE username = ? AND password = ?",
                       (username, hash_password))
        result = cursor.fetchone()
        if result:
            print("logged successfully")
        else:
            print("invalid user name or password")
    else:
        print("try again !!!")
# endregion