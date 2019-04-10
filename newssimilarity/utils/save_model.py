import json
import os
from newssimilarity.definitions import slash, saved_models_path
"""
Use to save learned models
"""


"""def save(model, name):
    path = slash.join(saved_models_path + [name])

    #p = slash.join(saved_models_path)
    #print(os.listdir(p))


    model_json = model.to_json()
    with open(path + '.json', 'w') as f:
        f.write(model_json)
    model.save_weights(path + '.h5')"""


def save(model, modelnum):

    #create directory
    os.makedirs(slash.join(saved_models_path + [modelnum]))
    path = slash.join(saved_models_path + [modelnum, modelnum])

    #p = slash.join(saved_models_path)
    #print(os.listdir(p))

    model_json = model.to_json()
    with open(path + '.json', 'w') as f:
        f.write(model_json)
    model.save_weights(path + '.h5')
