from newssimilarity.definitions import slash, saved_models_path
from keras.models import model_from_json



def load(name):
    #path = project_root + '/saved_models/'
    path = slash.join(saved_models_path + [name, name])
    with open(path + '.json', 'r') as g:
        file = g.read()

    model = model_from_json(file)
    model.load_weights(path + '.h5')
    return model