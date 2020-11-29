import pickle
import json

def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.json','r', encoding='utf-8' ) as f:
        return json.load(f)
