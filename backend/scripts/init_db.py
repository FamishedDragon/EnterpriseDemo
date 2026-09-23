from app.db.base import Base
from app.db.session import engine
from app.models.project import Project # noqa: F401

def main():
    Base.metadata.create_all(bind=engine)
    print("Database tables created")

if __name__ == "__main__":
    main()