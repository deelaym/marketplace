from fastapi import FastAPI

from models.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

