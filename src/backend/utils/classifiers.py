import os
from deepface import DeepFace
def tf_classifier(input_img, siamese_model, db_tree, preprocessor, db_path):
    prob_map = {}
    for name, files in db_tree.tree.items():
        total_probab = 0
        for file in files:
            path = os.path.join(db_path, name, file)
            validation_img = preprocessor(path)
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
    if max_prob<0.5:
        return None, max_prob
    return person, max_prob

def deepface_classifier(image, db_path, model_name):
    try:
        facenet_pred = DeepFace.find(image, db_path=db_path,model_name=model_name)[0]
        person = facenet_pred['identity'][0].split('\\')[-2]
        distance = facenet_pred['distance'][0]
    except:
        person = None
        distance = 0.69
    return person, distance