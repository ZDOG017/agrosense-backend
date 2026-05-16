from functools import lru_cache

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://your-frontend-domain.onrender.com",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:
        missing_fields = []
        for error in exc.errors():
            location = error.get("loc", ())
            if location:
                missing_fields.append(str(location[0]))

        details = ", ".join(missing_fields) if missing_fields else "DATABASE_URL, SECRET_KEY"
        raise RuntimeError(
            "Missing required environment variables for AgroSense. "
            "Create a .env file in the project root based on .env.example and set: "
            f"{details}."
        ) from exc
