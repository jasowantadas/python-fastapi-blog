from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# for actualy connecting to the database
engine = create_engine('sqlite:///./blog.db',
                       connect_args={"check_same_thread": False})


# for making changes in the database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()  # for models
