from fastapi import FastAPI, UploadFile, HTTPException
from utils.preprocessor import preprocess
from utils.custom_obj import L1Dist
from utils.dir_tree import DirTree
from fastapi.middleware.cors import CORSMiddleware
import os
from uuid import uuid4
import shutil

DB_PATH = 'db'
app = FastAPI()

origins = [
    'http://localhost:5173'
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_tree = DirTree(db_path=DB_PATH)

@app.delete('/reset')
def reset_db():
    try:
        dirs = os.listdir(os.getcwd())
        for folder in dirs:
            shutil.rmtree(folder)
        db_tree.tree = {}
        db_tree.save_tree()
        return {'message':'DB reset successful'}
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error!')


@app.post('/register')
def create_user(name:str, photo:UploadFile):
    try:
        if not os.path.exists(os.path.join(DB_PATH, name)):
            os.mkdir(os.path.join(DB_PATH, name))
        file_name = os.path.join(DB_PATH, name, '{}.jpg'.format(uuid4()))
        photo.filename = file_name
        with open(file_name, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        db_tree.update_tree(name=name, file_name=file_name)
        return {"message": "User created successfully!"}
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error!')