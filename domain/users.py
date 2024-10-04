from typing import Any

from sqlalchemy import Result

from database.models.user import User
from database.user_database_api import UserDatabaseAPI
from routers.request_models.request_user import RequestUser, Token


class Users:

    uda = UserDatabaseAPI()
    model = User

    def add_user(self, user: RequestUser) -> Result[Any]:
        return self.uda.insert(user, [user.dict()])

    def get_user_data(self, user_id: str):
        pass