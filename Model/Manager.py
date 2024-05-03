from Model.User import User

from Model.ConnectionToDB import *


class Manager(User):
    def __init__(self, ID: int = 0,
                 firstName: str = "",
                 lastName: str = "",
                 username: str = "",
                 age: int = "",
                 email: str = "",
                 image: str = "",
                 password: str = ""):
        super().__init__(ID, firstName, lastName, age, email, image)
        self.__userName: str = username
        self.__password: str = str(hash(password))

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
    def username(self):
        return self.__userName

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
    def password(self):
        return self.__password

    # endregion!!

    # region setters!!!
    @firstName.setter
    def firstName(self, firstName: str):
        self._firstName = firstName

    @lastName.setter
    def lastName(self, lastName: str):
        self._lastName = lastName

    @username.setter
    def username(self, username: str):
        self.__userName = username

    @age.setter
    def age(self, age: int):
        self._age = age

    @email.setter
    def email(self, email: str):
        self._email = email

    @image.setter
    def image(self, image: str):
        self._image = image

    @password.setter
    def password(self, password: str):
        self.__password = str(hash(password))

    # endregion
    def __str__(self):
        return f"{self.ID} | {self.firstName} - {self.lastName} | {self.username} | {self.age} | {self.email} | {self.image} | {self.password}"

    # region TableCreation
    @staticmethod
    def createManagersTable():
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS MANAGERS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255)NOT NULL UNIQUE,
                username VARCHAR(255) NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                image TEXT NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )"""
        )
        conn.commit()
    # endregion


Manager.createManagersTable()
