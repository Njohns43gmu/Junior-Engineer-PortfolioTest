from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db
import os, sys

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve the static folder whether running normally or as a PyInstaller exe
_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
_static = os.path.join(_base, 'static')

if os.path.exists(_static):
    app.mount('/assets', StaticFiles(directory=os.path.join(_static, 'assets')), name='assets')

    @app.get('/', response_class=FileResponse)
    def serve_frontend():
        return os.path.join(_static, 'index.html')
else:
    @app.get('/')
    def read_root():
        return {'message': 'Welcome to the FastAPI + PostgreSQL CRUD API'}

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, order: str = "asc", db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit, order=order)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item