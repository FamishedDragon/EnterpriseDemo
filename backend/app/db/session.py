from collections.abc import Generator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    # connect_args={"connect_timeout": 5,},
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

print(f"Database host configuration: {settings.database_url.split('@')[-1]}")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()