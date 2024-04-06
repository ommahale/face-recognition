from fastapi import FastAPI, UploadFile, HTTPException
from utils.preprocessor import preprocess
from utils.custom_obj import L1Dist
from utils.dir_tree import DirTree
from fastapi.middleware.cors import CORSMiddleware
import os
from uuid import uuid4
import shutil
from keras.models import load_model

DB_PATH = 'db'
app = FastAPI()
siamese_model = load_model('siamesemodel.keras', custom_objects={'L1Dist':L1Dist})
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
db_tree.init_tree()
@app.delete('/reset')
def reset_db():
    try:
        dirs = os.listdir(DB_PATH)
        for directory in dirs:
            files=os.listdir(os.path.join(DB_PATH, directory))
            for file in files:
                os.remove(os.path.join(DB_PATH, directory, file))
            os.rmdir(os.path.join(DB_PATH, directory))
        
        db_tree.tree = {}
        db_tree.save_tree()
        return {'message':'DB reset successful'}
    except ValueError:
        print()
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
        db_tree.update_tree(name=name, file_name=file_name.split('\\')[-1])
        return {"message": "User created successfully!"}
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error!')
    
@app.post('/evaluate')
async def evaluate(photo:UploadFile):
    try:
        photo = await photo.read()
        if os.path.exists('input.jpg'):
            os.remove('input.jpg')
        with open('input.jpg', 'wb+') as buffer:
            buffer.write(photo)
        input_img = preprocess(file_path=photo, ftype='byte')
        print(db_tree.tree.items())
        prob_map = {}
        for name, files in db_tree.tree.items():
            total_probab = 0
            for file in files:
                path = os.path.join(DB_PATH, name, file)
                validation_img = preprocess(path)
                probability = siamese_model.predict([input_img, validation_img])[0][0]
                total_probab+=probability
            mean_probab = total_probab/len(files)
            prob_map[name] = mean_probab
        max_prob = 0
        person = ''
        for name, prob in prob_map.items():
            if prob>max_prob:
                max_prob = prob
                person = name
        if max_prob<0.6:
            return {'person': 'Unrecognized'}
        return {'person':person}
                    
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error!')