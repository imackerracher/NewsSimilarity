from abc import ABCMeta, abstractmethod


class Parser(object, metaclass=ABCMeta):

    @abstractmethod
    def parse_topic(self):
        """
        Parse a single article
        :return:
        """

        raise NotImplementedError('this method must be implemented')

