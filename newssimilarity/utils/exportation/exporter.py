from abc import ABCMeta, abstractmethod


class Exporter(object, metaclass=ABCMeta):

    @abstractmethod
    def export(self):
        """
        Write an object to a file
        :return:
        """

        raise NotImplementedError('this method must be implemented')

