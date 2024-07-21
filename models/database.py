from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASSWORD']
DB = os.environ['DB']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}'


engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
