from fastapi import FastAPI, Depends
import models, schemas, notes, user
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.userapp)
app.include_router(notes.notesapp)