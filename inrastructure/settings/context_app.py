from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Identity service"
    admin_email: str | None = None
    base_link: str | None = None
    host: str | None = None
    http_secure: bool | None = None


settings = Settings()


class AppRegister:
    storage = {}

    @classmethod
    def check_app(cls, app_id: str) -> bool:
        return bool(
            cls.storage.get(
                app_id.strip()
            )
        )

    @classmethod
    def set_app(cls, app_id: str):
        cls.storage[app_id.strip()] = app_id
