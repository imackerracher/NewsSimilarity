from nltk.corpus import wordnet as wn


class WordnetHandler():


    def get_synonyms(self, word):
        #print('in syns', word)
        s = wn.synsets(word)
        syns = [str(syn)[8:-7] for syn in s]
        unique_syns = list(set(syns))
        return unique_syns

    def get_hypernyms(self, word):
        """
        "domestic animal" is a hypernym of "dog"
        :return:
        """

        s = wn.synsets(word)
        #check if hypernym list is longer that 0, otherwise index out of bounds
        hypers = [str(hyper)[8:-7] for hyper in s[0].hypernyms()] if s else []
        return hypers

    def get_hyponyms(self, word):
        """
        "dalmatian" is a hyponym of "dog"
        :return:
        """
        s = wn.synsets(word)
        hypos = [str(hypo)[8:-7] for hypo in s[0].hyponyms()] if s else []
        return hypos