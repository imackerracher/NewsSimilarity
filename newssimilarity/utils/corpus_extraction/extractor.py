from nltk.corpus import stopwords
import nltk

"""
Use this to extract all the tokens in the corpus once, for tf-idf
"""


class Extractor:
    def __init__(self, topics):
        self.topics = topics


    def run(self):



        article_list = []
        sentence_list = []
        def contains(token, dict):
            if token in dict:
                return True
            else:
                return False


        stop = set(stopwords.words('english'))
        corpus_tokens_dict = {}
        for topic in self.topics:
            for article in topic:
                article_tokens_dict = {}
                #article_tokens = nltk.word_tokenize(article.head + ' ' + article.lead + ' ' + article.body)
                for sentence in nltk.sent_tokenize(article.head + ' ' + article.lead + ' ' + article.body):
                    sentence_token_dict = {}
                    for token in nltk.word_tokenize(sentence):
                        if token not in stop:
                            if token in sentence_token_dict:
                                sentence_token_dict[token] += 1
                            else:
                                sentence_token_dict[token] = 1
                            if token in article_tokens_dict:
                                article_tokens_dict[token] += 1
                            else:
                                article_tokens_dict[token] = 1
                            if token in corpus_tokens_dict:
                                corpus_tokens_dict[token] += 1
                            else:
                                corpus_tokens_dict[token] = 1
                    sentence_list.append(sentence_token_dict)
                article_list.append(article_tokens_dict)

        return (corpus_tokens_dict, article_list, sentence_list)




    def run2(self):
        """
        :return: token_dict: a dictionary with all the tokens and their frequencies for the entire corpus;
                 article_list: list of tuples with the publisher for each topic and article and a dictionary with all the tokens and their frequencies in the article
        """
        article_list = []
        sentence_list = []
        token_dict = {}
        for topic in self.topics:
            for article in topic:
                article_token_dict = {}
                for instance in article.get_instances('part_of_speech'):
                    token = instance.content[0].lower()
                    stop = set(stopwords.words('english'))
                    if token not in stop:
                        if token in token_dict:
                            token_dict[token] += 1
                        else:
                            token_dict[token] = 1

                        if token in article_token_dict:
                            article_token_dict[token] += 1
                        else:
                            article_token_dict[token] = 1

                article_list.append(article_token_dict)

        return (token_dict, article_list)
