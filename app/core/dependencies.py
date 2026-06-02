from sqlalchemy.orm import sessionmaker
from app.database.models import db

def create_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()