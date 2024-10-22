from typing import Any

from sqlalchemy import Result

from inrastructure.database.models.user import User
from inrastructure.database.user_database_api import UserDatabaseAPI
from inrastructure.routers.request_models.request_user import RequestUser


class Users:

    uda = UserDatabaseAPI()
    model = User

    def add_user(self, user: RequestUser) -> Result[Any]:
        return self.uda.insert(user, [user.dict()])

    def get_user_data(self, user_id: str):
        pass