"""
Use to classify an article set with a trained model.
Maybe train a second higher level classifier?
"""


class ArticleClassifier:

    def __init__(self, model, article_set):

        self.model = model
        self.article_set = article_set