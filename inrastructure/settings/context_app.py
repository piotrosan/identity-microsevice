from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Identity service"
    admin_email: str | None = None
    base_link: str | None = None
    host: str | None = None
    http_secure: bool | None = None


settings = Settings()


