# repositories.py

from typing import List

from models import User

class UsersRepository:

    @staticmethod
    def get_users() -> List[User]:
        return [
            User(name="Juan Pérez", email="juan.perez@example.com"),
            User(name="María López", email="maria.lopez@example.com"),
        ]

    @staticmethod
    def capturatorRedbanc() -> List[User]:
        return [
            User(name="Juan Pérez", email="juan.perez@example.com"),
            User(name="María López", email="maria.lopez@example.com"),
        ]
