from abc import ABC


class User(ABC):
    def __init__(self, ID: int,
                 firstName: str,
                 lastName: str,
                 age: int,
                 email: str,
                 image: str):
        self._ID = ID
        self._firstName: str = firstName
        self._lastName: str = lastName
        self._age: int = age
        self._email: str = email
        self._image: str = image
