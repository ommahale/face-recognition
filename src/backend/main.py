import time
from fastapi import FastAPI, UploadFile, HTTPException
from utils.preprocessor import preprocess
from utils.custom_obj import L1Dist
from utils.dir_tree import DirTree
from fastapi.middleware.cors import CORSMiddleware
import os
from uuid import uuid4
import shutil
from keras.models import load_model
from utils.classifiers import tf_classifier, deepface_classifier
from concurrent.futures import ThreadPoolExecutor
DB_PATH = 'db'
app = FastAPI()
models = {
    'siamese':load_model('models/siamesemodel.keras', custom_objects={'L1Dist':L1Dist}),
    'vgg': load_model('models/vgg_model.keras', custom_objects={'L1Dist':L1Dist}),
    'mbnv2': load_model('models/mbnv2_model.keras', custom_objects={'L1Dist':L1Dist}),
}
if not os.path.exists(DB_PATH):
    os.mkdir(DB_PATH)

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
print('Building Databse tree')
db_tree.make_tree()
db_tree.init_tree()
@app.delete('/reset')
def reset_db():
    try:
        dirs = os.listdir(DB_PATH)
        for directory in dirs:
            try:
                files=os.listdir(os.path.join(DB_PATH, directory))
                for file in files:
                    os.remove(os.path.join(DB_PATH, directory, file))
                os.rmdir(os.path.join(DB_PATH, directory))
            except:
                continue
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
    start_time = time.time()
    photo = await photo.read()
    if os.path.exists('input.jpg'):
        os.remove('input.jpg')
    with open('input.jpg', 'wb+') as buffer:
        buffer.write(photo)
    input_img = preprocess(file_path=photo, ftype='byte')
    person_siamese, conf_siamese = tf_classifier(input_img, models['siamese'], db_tree,preprocess, DB_PATH)
    person_vgg, conf_vgg = tf_classifier(input_img, models['vgg'], db_tree,preprocess, DB_PATH)
    person_mbnv2, conf_mbnv2 = tf_classifier(input_img, models['mbnv2'], db_tree,preprocess, DB_PATH)
    person_facenet, person_facenet_distance = deepface_classifier(image='input.jpg',db_path='./db',model_name='Facenet')
    person_facenet512, person_facenet512_distance = deepface_classifier(image='input.jpg',db_path='./db',model_name='Facenet512')
    end_time = time.time()
    response_time = end_time - start_time
    print(f"Response time: {response_time:.3f} seconds")
    return {
        "siamese":{
            "prediction":person_siamese,
            "confidence":conf_siamese
        },
        "vgg":{
            "prediction":person_vgg,
            "confidence":conf_vgg
        },
        "mobilenetV2":{
            "prediction":person_mbnv2,
            "confidence":conf_mbnv2
        },
        "facenet":{
            "prediction":person_facenet,
            "distance":person_facenet_distance
        },
        "facenet512":{
            "prediction":person_facenet512,
            "distance":person_facenet512_distance
        }
    }
'''
Following is the implementation of API route using threads for performace optimization
'''
@app.post('/thread-evaluate')
async def evaluate(photo:UploadFile):
    start_time = time.time()
    photo = await photo.read()
    if os.path.exists('input.jpg'):
        os.remove('input.jpg')
    with open('input.jpg', 'wb+') as buffer:
        buffer.write(photo)
    input_img = preprocess(file_path=photo, ftype='byte')
    with ThreadPoolExecutor(max_workers=5) as executor:
        f1= executor.submit(tf_classifier,input_img, models['siamese'], db_tree,preprocess, DB_PATH)
        f2= executor.submit(tf_classifier,input_img, models['vgg'], db_tree,preprocess, DB_PATH)
        f3= executor.submit(tf_classifier,input_img, models['mbnv2'], db_tree,preprocess, DB_PATH)
        f4= executor.submit(deepface_classifier,image='input.jpg',db_path='./db',model_name='Facenet')
        f5= executor.submit(deepface_classifier,image='input.jpg',db_path='./db',model_name='Facenet512')
    person_siamese, conf_siamese = f1.result()
    person_vgg, conf_vgg = f2.result()
    person_mbnv2, conf_mbnv2 = f3.result()
    person_facenet, person_facenet_distance = f4.result()
    person_facenet512, person_facenet512_distance = f5.result()
    end_time = time.time()
    response_time = end_time - start_time
    print(f"Response time: {response_time:.3f} seconds")
    return {
        "siamese":{
            "prediction":person_siamese,
            "confidence":conf_siamese
        },
        "vgg":{
            "prediction":person_vgg,
            "confidence":conf_vgg
        },
        "mobilenetV2":{
            "prediction":person_mbnv2,
            "confidence":conf_mbnv2
        },
        "facenet":{
            "prediction":person_facenet,
            "distance":person_facenet_distance
        },
        "facenet512":{
            "prediction":person_facenet512,
            "distance":person_facenet512_distance
        }
    }
                    
