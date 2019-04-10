"""
This class gets used by all the different methods for preprocessing
"""

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import LancasterStemmer
import nltk


class Preprocessor2:
    def __init__(self, tokens, lower_case=False, stopword_removal=False, stemming=False,
                 stemmer=False, lemmatization=False, synonyms=False, ne_disambiguation=False):
        """

        :param tokens: List of tokens from the article that is being preprocessed
        :param lower_case: Turns all tokens to lower case
        :param stopword_removal: Removes all stopwords
        :param stemming: Performs stemming (a stemmer has to be chose in addition)
        :param stemmer: Lancaster, snowball or porter stemmer can be chosen
        :param lemmatization: Performs lemmatization
        :param synonyms: Check for synonyms
        :param ne_disambiguation: Disambiguate the named entities
        """
        self.tokens = tokens
        self.lower_case = lower_case
        self.stopword_removal = stopword_removal
        self.stemming = stemming
        self.stemmer = stemmer
        self.lemmatization = lemmatization
        self.synonyms = synonyms
        self.ne_disambiguation = ne_disambiguation

    def case(self, token):
        """
        Helper function to set lower case or not
        :return: Token, in lower case, if specified.
        """
        if self.lower_case:
            # also cut out &quot;
            return token.lower()  # .replace('&quot;', '\"')
        else:
            return token

    def process(self):
        """
        Apply all the specified preprocessing steps to the tokens from a segment
        :return: Tokens, with preprocessing steps applied to them
        """

        processed_tokens = self.tokens

        if self.stopword_removal:
            stop = set(stopwords.words('english'))
            processed_tokens = [self.case(token[0]) for token in processed_tokens if token[0] not in stop]

        if self.stemming:
            if self.stemmer == 'lancaster':
                ls = LancasterStemmer()
                processed_tokens = [self.case(ls.stem(token[0])) for token in processed_tokens]
            elif self.stemmer == 'snowball':
                ss = SnowballStemmer('english')
                processed_tokens = [self.case(ss.stem(token[0])) for token in processed_tokens]

            else:
                ps = PorterStemmer()
                processed_tokens = [self.case(ps.stem(token[0])) for token in processed_tokens]

        if self.lemmatization:
            lemma = nltk.wordnet.WordNetLemmatizer()
            processed_tokens = [self.case(lemma.lemmatize(token[0], token[1])) for token in processed_tokens]

        # no preprocessing method was selected, return only [Bagdad, car,...] instead of [[Bagdad, NNP], [car, NN], [..]..]
        if not self.stopword_removal and not self.stemming and not self.lemmatization:
            processed_tokens = [self.case(token[0]) for token in processed_tokens]

        return processed_tokens