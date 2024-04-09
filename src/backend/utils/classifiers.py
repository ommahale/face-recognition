import os

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
