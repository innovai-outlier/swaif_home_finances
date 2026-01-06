from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"

    # Default is intentionally safe for tests/imports; real runs should set DATABASE_URL.
    database_url: str = "sqlite+pysqlite:///:memory:"

    seed_patriarch_cpf: str = "00000000000"
    seed_patriarch_password: str = "admin123"


settings = Settings()
