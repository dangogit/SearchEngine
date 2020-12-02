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

def load_inverted_index():
    inverted_idx_files_list = ["inverted_idx_a",
                               "inverted_idx_b",
                               "inverted_idx_c",
                               "inverted_idx_d",
                               "inverted_idx_e",
                               "inverted_idx_f",
                               "inverted_idx_g",
                               "inverted_idx_h",
                               "inverted_idx_i",
                               "inverted_idx_j",
                               "inverted_idx_k",
                               "inverted_idx_l",
                               "inverted_idx_m",
                               "inverted_idx_n",
                               "inverted_idx_o",
                               "inverted_idx_p",
                               "inverted_idx_q",
                               "inverted_idx_r",
                               "inverted_idx_s",
                               "inverted_idx_t",
                               "inverted_idx_u",
                               "inverted_idx_v",
                               "inverted_idx_w",
                               "inverted_idx_x",
                               "inverted_idx_y",
                               "inverted_idx_z",
                               "inverted_idx_hashtags"]
    inverted_index = {}
    for filename in inverted_idx_files_list:
        with open('posting\\'+filename + '.json', 'r', encoding='utf-8') as f:
            dict = json.load(f)
            inverted_index.update(dict)
    return inverted_index
