import json

import utils


class Indexer:

    def __init__(self, config):

        self.config = config

        self.a_inverted_idx = {}
        self.bc_inverted_idx = {}
        self.d_inverted_idx = {}
        self.e_inverted_idx = {}
        self.fg_inverted_idx = {}
        self.h_inverted_idx = {}
        self.i_inverted_idx = {}
        self.jm_inverted_idx = {}
        self.n_inverted_idx = {}
        self.o_inverted_idx = {}
        self.pq_inverted_idx = {}
        self.r_inverted_idx = {}
        self.s_inverted_idx = {}
        self.t_inverted_idx = {}
        self.u_inverted_idx = {}
        self.vz_inverted_idx = {}
        self.else_inverted_idx = {}

        self.a_post_dict = {}
        self.bc_post_dict = {}
        self.d_post_dict = {}
        self.e_post_dict = {}
        self.fg_post_dict = {}
        self.h_post_dict = {}
        self.i_post_dict = {}
        self.jm_post_dict = {}
        self.n_post_dict = {}
        self.o_post_dict = {}
        self.pq_post_dict = {}
        self.r_post_dict = {}
        self.s_post_dict = {}
        self.t_post_dict = {}
        self.u_post_dict = {}
        self.vz_post_dict = {}
        self.else_post_dict = {}



    def load_dict(self, name, type):
        dict = {}
        file_name = "inv_and_post_dicts\\" + name + '_' + type + '.json'
        try:
            with open(file_name) as infile:
                dict = json.load(infile)
        except:
            return None
        return dict

    def load_curr_dict(self, name, type):
        if (name == 'a'):
            if (type == 'inverted'):
                return self.a_inverted_idx
            return self.a_post_dict
        elif (name == 'bc'):
            if (type == 'inverted'):
                return self.bc_inverted_idx
            return self.bc_post_dict
        elif (name == 'd'):
            if (type == 'inverted'):
                return self.d_inverted_idx
            return self.d_post_dict
        elif (name == 'e'):
            if (type == 'inverted'):
                return self.e_inverted_idx
            return self.e_post_dict
        elif (name == 'fg'):
            if (type == 'inverted'):
                return self.fg_inverted_idx
            return self.fg_post_dict
        elif (name == 'h'):
            if (type == 'inverted'):
                return self.h_inverted_idx
            return self.h_post_dict
        elif (name == 'i'):
            if (type == 'inverted'):
                return self.i_inverted_idx
            return self.i_post_dict
        elif (name == 'jm'):
            if (type == 'inverted'):
                return self.jm_inverted_idx
            return self.jm_post_dict
        elif (name == 'n'):
            if (type == 'inverted'):
                return self.n_inverted_idx
            return self.n_post_dict
        elif (name == 'o'):
            if (type == 'inverted'):
                return self.o_inverted_idx
            return self.o_post_dict
        elif (name == 'pq'):
            if (type == 'inverted'):
                return self.pq_inverted_idx
            return self.pq_post_dict
        elif (name == 'r'):
            if (type == 'inverted'):
                return self.r_inverted_idx
            return self.r_post_dict
        elif (name == 's'):
            if (type == 'inverted'):
                return self.s_inverted_idx
            return self.s_post_dict
        elif (name == 't'):
            if (type == 'inverted'):
                return self.t_inverted_idx
            return self.t_post_dict
        elif (name == 'u'):
            if (type == 'inverted'):
                return self.u_inverted_idx
            return self.u_post_dict
        elif (name == 'vz'):
            if (type == 'inverted'):
                return self.vz_inverted_idx
            return self.vz_post_dict
        elif (name == 'else'):
            if (type == 'inverted'):
                return self.else_inverted_idx
            return self.else_post_dict

    def update_global_inverted_dict(self, name):
        '''
        this function get some terms and save data about the terms in inverted index
        :param dict: dictionary with limited number of terms
        :return:
        '''
        inv_dict = self.load_dict(name, "inverted_idx")
        local_dict = self.load_curr_dict(name, "inverted")
        file_name = "inv_and_post_dicts\\" + name + '_inverted_idx.json'
        if (inv_dict == None):
            if len(local_dict) < 1:
                return
            with open(file_name, 'w') as outfile:
                json.dump(local_dict, outfile)
            local_dict.clear()
            return

        for term in local_dict:
            if (term.isalpha()):
                if term in inv_dict:
                    if term[0].isupper():
                        if term.lower() in inv_dict:
                            inv_dict[term.lower()][0] += local_dict[term][0]
                            inv_dict[term.lower()][1] += local_dict[term][1]
                        elif term.upper() in inv_dict:
                            inv_dict[term.upper()][0] += local_dict[term][0]
                            inv_dict[term.upper()][1] += local_dict[term][1]
                    else:
                        if term.upper() in inv_dict:
                            inv_dict[term.lower()][0] = inv_dict[term.upper()][0] + local_dict[term][0]
                            inv_dict[term.lower()][1] = inv_dict[term.upper()][1] + local_dict[term][1]
                            del inv_dict[term.upper()]
                        else:
                            inv_dict[term.lower()][0] = inv_dict[term.lower()][0] + local_dict[term][0]
                            inv_dict[term.lower()][1] += local_dict[term][1]
                else:
                    if term[0].isupper():
                        inv_dict[term.upper()] = local_dict[term]
                    else:
                        inv_dict[term.lower()] = local_dict[term]

            else:
                if term not in inv_dict:
                    inv_dict[term] = local_dict[term]
                else:
                    inv_dict[term][0] = inv_dict[term][0] + local_dict[term][0]
                    inv_dict[term][1] = inv_dict[term][1] + local_dict[term][1]
        with open(file_name, 'w') as outfile:
            json.dump(inv_dict, outfile)
        local_dict.clear()

    def update_locals_inverted_dicts(self, dict):
        for dict_term in dict:
            if len(dict_term) < 1:
                continue
            if (dict_term.isalpha() == False):
                self.else_inverted_idx[dict_term] = dict[dict_term]
                continue
            if 'a' == dict_term[0].lower():
                inv_dict = self.a_inverted_idx
            elif 'b' <= dict_term[0].lower() <= 'c':
                inv_dict = self.bc_inverted_idx
            elif 'd' == dict_term[0].lower():
                inv_dict = self.d_inverted_idx
            elif 'e' == dict_term[0].lower():
                inv_dict = self.e_inverted_idx
            elif 'f' <= dict_term[0].lower() <= 'g':
                inv_dict = self.fg_inverted_idx
            elif 'h' == dict_term[0].lower():
                inv_dict = self.h_inverted_idx
            elif 'i' == dict_term[0].lower():
                inv_dict = self.i_inverted_idx
            elif 'j' <= dict_term[0].lower() <= 'm':
                inv_dict = self.jm_inverted_idx
            elif 'n' == dict_term[0].lower():
                inv_dict = self.n_inverted_idx
            elif 'o' == dict_term[0].lower():
                inv_dict = self.o_inverted_idx
            elif 'p' <= dict_term[0].lower() <= 'q':
                inv_dict = self.pq_inverted_idx
            elif 'r' <= dict_term[0].lower():
                inv_dict = self.r_inverted_idx
            elif 's' <= dict_term[0].lower():
                inv_dict = self.s_inverted_idx
            elif 't' <= dict_term[0].lower():
                inv_dict = self.t_inverted_idx
            elif 'u' == dict_term[0].lower():
                inv_dict = self.u_inverted_idx
            elif 'v' <= dict_term[0].lower() <= 'z':
                inv_dict = self.vz_inverted_idx

            term = dict_term
            if str.isupper(dict_term[0]):
                inv_dict[term.upper()] = dict[dict_term]
            else:
                inv_dict[term.lower()] = dict[dict_term]

    def update_locals_posting_dicts(self, dict):
        for dict_term in dict:
            if len(dict_term) < 1:
                continue
            if (dict_term.isalpha() == False):
                self.else_post_dict[dict_term.lower()] = dict[dict_term]
                continue
            if 'a' == dict_term[0].lower():
                post_dict = self.a_post_dict
            elif 'b' <= dict_term[0].lower() <= 'c':
                post_dict = self.bc_post_dict
            elif 'd' == dict_term[0].lower():
                post_dict = self.d_post_dict
            elif 'e' == dict_term[0].lower():
                post_dict = self.e_post_dict
            elif 'f' <= dict_term[0].lower() <= 'g':
                post_dict = self.fg_post_dict
            elif 'h' == dict_term[0].lower():
                post_dict = self.h_post_dict
            elif 'i' == dict_term[0].lower():
                post_dict = self.i_post_dict
            elif 'j' <= dict_term[0].lower() <= 'm':
                post_dict = self.jm_post_dict
            elif 'n' == dict_term[0].lower():
                post_dict = self.n_post_dict
            elif 'o' == dict_term[0].lower():
                post_dict = self.o_post_dict
            elif 'p' <= dict_term[0].lower() <= 'q':
                post_dict = self.pq_post_dict
            elif 'r' <= dict_term[0].lower():
                post_dict = self.r_post_dict
            elif 's' <= dict_term[0].lower():
                post_dict = self.s_post_dict
            elif 't' <= dict_term[0].lower():
                post_dict = self.t_post_dict
            elif 'u' == dict_term[0].lower():
                post_dict = self.u_post_dict
            elif 'v' <= dict_term[0].lower() <= 'z':
                post_dict = self.vz_post_dict

            post_dict[dict_term.lower()] = dict[dict_term]

    def update_global_posting_dicts(self, name):

        post_dict = self.load_dict(name, "posting_dict")
        local_dict = self.load_curr_dict(name, "post")
        file_name = "inv_and_post_dicts\\" + name + '_posting_dict.json'
        if (post_dict == None):
            if len(local_dict) < 1:
                return
            with open(file_name, 'w') as outfile:
                json.dump(local_dict, outfile)
            local_dict.clear()
            return

        for word in local_dict:
            if word.lower() in post_dict:
                post_dict[word.lower()] += local_dict[word.lower()]
            else:
                post_dict[word.lower()] = local_dict[word.lower()]

        with open(file_name, 'w') as outfile:
            json.dump(post_dict, outfile)
        post_dict.clear()

    def update_index_data(self, invert_dict, post_dict):
        if len(invert_dict) > 0:
            self.update_locals_inverted_dicts(invert_dict)
        if len(post_dict) > 0:
            self.update_locals_posting_dicts(post_dict)
        letter_lst = ["a", "bc", "d", "e", "fg", "h", "i", "jm", "n", "o", "pq", "r", "s", "t", "u", "vz", "else"]
        for letter in letter_lst:
            self.update_global_inverted_dict(letter)
            self.update_global_posting_dicts(letter)













