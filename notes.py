from fastapi import APIRouter, Depends, HTTPException, status
import models, schemas, auth
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


notesapp = APIRouter(tags=['Notes'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@notesapp.get('/notes/' , response_model= List[schemas.NoteResponse])
async def get_all_notes(db : Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    s = db.query(models.Note).filter(models.Note.user_id == current_user['id']).all()
    return s

@notesapp.post('/notes/', response_model=schemas.NoteResponse)
async def create_note(data : schemas.NoteSchema, db : Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    s = models.Note(title = data.title, content = data.content , user_id = int(current_user['id']))
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@notesapp.get('/notes/{id}', response_model=schemas.NoteResponse)
async def get_single_note(id : int, db : Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    s = db.query(models.Note).filter(models.Note.id == id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No data is present for the id {id}")
    if s.user_id != int(current_user['id']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No data is present for the id {id}")
    return s

@notesapp.put('/notes/{id}', response_model=schemas.NoteResponse)
async def update_note(id : int, data : schemas.NoteSchema, db : Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):

    note = db.query(models.Note).filter(models.Note.id == id).first()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No data is present for the id {id}")
    
    if note.user_id != int(current_user['id']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No data is present for the id {id}")

    

    note.title = data.title
    note.content = data.content

    db.commit()

    return note

@notesapp.delete('/notes/{id}')
async def delete_note(id : int, db : Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    s = db.query(models.Note).filter(models.Note.id == id).first()

    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No data is present for the id {id}")
    
    if s.user_id != int(current_user['id']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No data is present for the id {id}")
    
    db.delete(s)
    db.commit()
    return {"Deleted!"}