"""
Article object, read in from json
"""


class Article(object):
    def __init__(self, head, lead, body,
                 date, time, writers,
                 publisher, source_outlet,
                 additional_information, annotation_list,
                 feature_list, raw_article):
        """
        :param head: Headline of the article
        :param lead: Lead paragraph of the article
        :param body: Rest of the article
        :param date: Publishing date of the article. If article was modified, the latest date
        :param time: Publishing time of the article. If article was modified, the latest time
        :param writers: The writers that contributed to the article
        :param publisher: The news outlet that published the article
        :param source_outlet: If the publisher took the article from a different source, it will be contained in this
                              variable
        :param additional_information: E.g.: "...contributed to this report"
        :param annotation_list: A list containing all the annotations as annotation objects
        :param feature_list: A list containing all the features, as feature objects
        :param raw_article: The raw article without any processing, etc. (contains the annotations as well)
        """

        self.head = head
        self.lead = lead
        self.body = body
        self.date = date
        self.time = time
        self.writers = writers
        self.publisher = publisher
        self.source_outlet = source_outlet
        self.additional_information = additional_information
        self.annotation_list = annotation_list
        self.feature_list = feature_list
        self.raw_article = raw_article

    def get_instances(self, instance_type):
        """
        Utility function to return a list of instances
        :param instance_type: Type of instance (e.g. part of speech)
        :return: List with instances
        """

        instances = [instance
                     for feature in self.feature_list
                     if feature.feature_name == instance_type
                     for instance in feature.feature_instance_list]

        return instances
