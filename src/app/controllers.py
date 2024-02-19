# controllers.py
import os
from fastapi import APIRouter

from service import UsersService

class UsersController:

    router = APIRouter()

    @router.get("/users")
    def get_users(self):
        """
        Devuelve una lista de usuarios.
        Args:
            None
        Returns:
            Lista de usuarios.
        """

        return UsersService.get_users(self)

    @router.get("/capturator-ripley")
    def capturatorRedbanc():
        """
        Devuelve una lista de usuarios.
        Args:
            None
        Returns:
            Lista de usuarios.
        """
        return UsersService.capturatorRedbanc()